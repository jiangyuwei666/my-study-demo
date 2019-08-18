package com.sogou.spark;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.compress.CompressionCodec;
import org.apache.hadoop.io.compress.CompressionCodecFactory;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.TaskAttemptID;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.task.TaskAttemptContextImpl;

import com.sogou.spark.DocId256;
import com.sogou.spark.OffsumPageWritableV2.ContentItem;

public class OffsumPageInputFormatV2 extends FileInputFormat<BytesWritable, OffsumPageWritableV2> {

	@Override
	protected boolean isSplitable(JobContext context, Path file) {

		CompressionCodec codec = new CompressionCodecFactory(context.getConfiguration()).getCodec(file);

		return codec == null;
	}

	@Override
	public RecordReader<BytesWritable, OffsumPageWritableV2> createRecordReader(InputSplit arg0, TaskAttemptContext arg1)
			throws IOException, InterruptedException {

		return new OffsumPageRecordReader();
	}

	public static class OffsumPageRecordReader extends RecordReader<BytesWritable, OffsumPageWritableV2> {

		private TaskAttemptContext context = null;

		public FSDataInputStream dis;
		private BytesWritable key;
		private OffsumPageWritableV2 value;
		private boolean more = false;
		private Configuration conf;

		private String url;
		private boolean is_deleted = false;
		private List<String> attributes = new ArrayList<String>();
		private List<String> contenttype = new ArrayList<String>();
		private List<String> originalsize = new ArrayList<String>();
		private List<ContentItem> contentItems = new ArrayList<ContentItem>(4);

		private long start = 0;
		public long end = 0;
		private long curr_pos = 0;
		private long len = 0;
		public long fileLength = 0;

		public enum KeyFormat {
			URL, DOCID256, URLID
		}

		KeyFormat keyFormat;

		public KeyFormat keyFormatFromLiteral(String keyFormatLiteral) {
			if (keyFormatLiteral.equals("URL")) {
				return KeyFormat.URL;
			} else if (keyFormatLiteral.equals("DOCID") || keyFormatLiteral.equals("DOCID256")) {
				return KeyFormat.DOCID256;
			} else if (keyFormatLiteral.equals("URLID")) {
				return KeyFormat.URLID;
			}
			return KeyFormat.URL;
		}

		public OffsumPageRecordReader() {

			more = true;
		}

		@Override
		public void close() throws IOException {

			if (dis != null) {
				dis.close();
			}
		}

		@Override
		public BytesWritable getCurrentKey() throws IOException, InterruptedException {

			return key;
		}

		@Override
		public OffsumPageWritableV2 getCurrentValue() throws IOException, InterruptedException {

			return value;
		}

		@Override
		public float getProgress() throws IOException, InterruptedException {
			return more ? (float) ((curr_pos - start) / (double) len) : 1.0f;
		}

		@Override
		public void initialize(InputSplit gensplit, TaskAttemptContext context) throws IOException, InterruptedException {
			this.context = context;

			FileSplit split = (FileSplit) gensplit;

			start = split.getStart();
			end = split.getLength() + start;

			conf = context.getConfiguration();
			Path file = split.getPath();
			FileSystem fs = file.getFileSystem(conf);
			fileLength = PageParseUtil.getFileLength(fs, file);
			dis = fs.open(file);

			if (fileLength < start) {
				throw new IOException("file length error. can not skip " + start + " bytes to read, the file length is " + fileLength);
			}

			long skipLen = 0;
			skipLen = dis.skip(start);
			if (skipLen != start) {
				throw new IOException("skip error when split-read.");
			}

			curr_pos = start;
			len = end - start;

			String keyFormatLiteral = conf.get("SpiderPageRecordReader.keyFormat", "URL");
			keyFormat = keyFormatFromLiteral(keyFormatLiteral);
		}

		@Override
		public boolean nextKeyValue() throws IOException, InterruptedException {

			if (dis != null && PageParseUtil.available(dis, fileLength) != 0 && curr_pos < end) {
				long startTime = System.nanoTime();
				if (readOffsumPage(dis)) {
					value = new OffsumPageWritableV2(url, is_deleted, attributes);
					value.contentItems = this.contentItems;

					//, originalsize, contenttype);
					key = new BytesWritable();
					if (keyFormat == KeyFormat.URL) {
						key.set(value.url.getBytes(), 0, value.url.length());
					} else if (keyFormat == KeyFormat.DOCID256) {
						key.set(new DocId256(value.url.toString()).getDocId256Bytes(), 0, DocId256.BYTE_DOCID_LENGTH);
					} else if (keyFormat == KeyFormat.URLID) {
						key.set(new DocId256(value.url.toString()).getUrlIdBytes(), 0, DocId256.BYTE_URLID_LENGTH);
					}
				} else {
					return false;
				}

				curr_pos = dis.getPos();
				long endTime = System.nanoTime();

				this.context.getCounter("PERFORMANCE", "OPIF-READPAGE-COST").increment((endTime - startTime) / 1000);

				return true;
			} else {
				more = false;
				return false;
			}
		}

		private boolean readOffsumPage(FSDataInputStream dis) {

			clear();
			try {
				long startTime = System.nanoTime();
				url = null;
				long pos = dis.getPos();
				while (PageParseUtil.available(dis, fileLength) != 0 && (url = PageParseUtil.readLine(dis, fileLength)) != null) {
					if (url.startsWith("http")) {
						break;
					}
					pos = dis.getPos();
				}

				if (url == null || url.trim().length() == 0) {
					return false;
				}

				if (url.startsWith("http") && pos >= end) { // record start position out of range
					return false;
				}

				int ret = -1;
				String line = "";
				while (PageParseUtil.available(dis, fileLength) != 0 && (line = PageParseUtil.readLine(dis, fileLength)) != null) {
					if (line.length() == 0) {
						ret = 0;
						break;
					}
					attributes.add(line);
				}
				long endTime = System.nanoTime();
				this.context.getCounter("PERFORMANCE", "OPIF-READPAGE-READATTR-COST").increment((endTime - startTime) / 1000);

				if (ret != 0) {
					System.err.println("Read attributes error." + url);
					return false;
				}

				startTime = System.nanoTime();
				String type;
				if ((type = PageParseUtil.getValueByKeyName(attributes, "Type", ":")) != null) {
					if (type == "deleted") {
						this.is_deleted = true;
						return true;
					}
				}

				int storeSizeFull = 0;
				if ((type = PageParseUtil.getValueByKeyName(attributes, "Content-Type", ":")) != null) {
					String[] ctSize = type.split(";");
					for (int i = 0; i < ctSize.length; i++) {
						//contenttype.add(ctSize[i]);

						int pos_comma = ctSize[i].indexOf(',');
						if (pos_comma < 0)
							throw new IOException("NO COMMA IN Content-Type: " + ctSize[i]);

						ContentItem ci = new ContentItem();
						ci.type = ctSize[i].substring(0, pos_comma);
						ci.storeSize = Integer.parseInt(ctSize[i].substring(pos_comma + 1).trim());

						this.contentItems.add(ci);

						storeSizeFull += ci.storeSize;
					}
				} else {
					throw new IOException("Read Content-Type error." + url);
				}

				if ((type = PageParseUtil.getValueByKeyName(attributes, "Original-Size", ":")) != null) {
					String[] oSize = type.split(";");
					for (int i = 0; i < oSize.length; i++) {
						int pos_comma = oSize[i].indexOf(',');
						if (pos_comma < 0)
							throw new IOException("NO COMMA IN Original-Size: " + oSize[i]);

						ContentItem ci = this.contentItems.get(i);
						if (ci.type.equals(oSize[i].substring(0, pos_comma)) == false)
							throw new IOException("CONFLICING Content-Type and Original-Size");

						ci.originalSize = Integer.parseInt(oSize[i].substring(pos_comma + 1).trim());
					}
				} else {
					throw new IOException("Read Original-Size error." + url);
				}
				endTime = System.nanoTime();
				this.context.getCounter("PERFORMANCE", "OPIF-READPAGE-PARSEATTR-COST").increment((endTime - startTime) / 1000);

				byte[] content_full = new byte[storeSizeFull];

				startTime = System.nanoTime();
				int size = PageParseUtil.readBytesV2(dis, content_full, storeSizeFull, fileLength);
				endTime = System.nanoTime();
				this.context.getCounter("PERFORMANCE", "OPIF-READPAGE-READCON-COST").increment((endTime - startTime) / 1000);

				if (size != storeSizeFull) {
					System.err.println("Content-Type and Content cann't match." + url);
					return false;
				}

				int content_offset = 0;
				for (ContentItem ci : this.contentItems) {
					ci.content = new byte[ci.storeSize];
					System.arraycopy(content_full, content_offset, ci.content, 0, ci.storeSize);
					content_offset += ci.storeSize;
				}

			} catch (Exception ex) {
				System.err.println(ex.getMessage());
				return false;
			}

			return true;
		}

		private void clear() {
			url = "";
			is_deleted = false;
			attributes.clear();
			contenttype.clear();
			originalsize.clear();
			contentItems.clear();

			key = null;
			value = null;
		}
	}

	public static Set<String> test(OffsumPageWritableV2 opw) {
		TreeSet<String> results = new TreeSet<String>();
		for (ContentItem ci : opw.contentItems) {
			if (ci.type.equals("snapshot") == false)
				continue;
			byte[] output = new byte[ci.originalSize];
			Inflater decompresser = new Inflater();
			decompresser.setInput(ci.content);
			int resultLength;
			try {
				resultLength = decompresser.inflate(output);
			} catch (DataFormatException e) {
				System.err.println("ERROR DECOMPRESSING");
				return null;
			}
			decompresser.end();

			String snapshot = new String(output, 0, resultLength, Charset.forName("ASCII"));//ASCII
			//System.out.println(snapshot);
			if (snapshot
					.contains("<!DOCTYPE html PUBLIC \"-//WAPFORUM//DTD XHTML Mobile 1.0//EN\" \"http://www.wapforum.org/DTD/xhtml-mobile10.dtd\">")) {
				//results.add("WAP1");
			}
			if (snapshot.contains(" name=\"viewport\" ") && snapshot.contains(" initial-scale=1.")) {
				results.add("WAP2");
			}
		}
		return results;
	}

	public static void main(String[] args) throws IOException, InterruptedException {
		Configuration conf = new Configuration();
		OffsumPageRecordReader reader = new OffsumPageRecordReader();
		FileSystem fs = FileSystem.getLocal(conf);
		Path filePath = new Path("/search/liyi/part-m-07961");
		//FSDataInputStream fdis = fs.open(filePath);
		File file = new File("/search/liyi/part-m-07961");
		//reader.dis = fdis;
		//reader.fileLength = file.length();
		//reader.end = file.length();
		reader.initialize(new FileSplit(filePath, 0, file.length(), new String[0]), new TaskAttemptContextImpl(conf, new TaskAttemptID()));
		int progress = 0;
		while (reader.nextKeyValue()) {
			progress++;
			if (progress % 1000 == 0)
				System.err.println("Progress: " + progress);
			OffsumPageWritableV2 opw = reader.getCurrentValue();
			System.out.println(opw.url);
			//opw.getOffsumPageBytes();
			//break;
		}
	}
}
/*
 * Set<String> results = test(opw); if(results.isEmpty()) continue;
 * StringBuilder sb = new StringBuilder(); for(String s : results){
 * sb.append('\t').append(s); } System.out.println(opw.url + sb.toString());
 */
