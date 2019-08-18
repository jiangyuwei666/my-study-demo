package com.sogou.spark;

import java.io.File;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

import com.sogou.spark.DocId256;
import com.sogou.spark.SpiderPageWritable.Attribute;
import com.sogou.spark.SpiderPageWritable.PageType;

public class SpiderPageInputFormatV3 extends FileInputFormat<BytesWritable, SpiderPageWritable> {

	@Override
	protected boolean isSplitable(JobContext context, Path file) {
		return context.getConfiguration().getBoolean("SpiderPageRecordReader.splittable", false);
	}

	@Override
	protected long getFormatMinSplitSize() {
		return 128 * 1024 * 1024;
	}

	@Override
	public RecordReader<BytesWritable, SpiderPageWritable> createRecordReader(InputSplit arg0, TaskAttemptContext arg1) throws IOException,
			InterruptedException {
		return new SpiderPageRecordReader();
	}

	static class SpiderPageRecordReader extends RecordReader<BytesWritable, SpiderPageWritable> {

		FSDataInputStream	dis;
		private BytesWritable		key				= new BytesWritable();
		private SpiderPageWritable	value			= new SpiderPageWritable();
		private boolean				more			= true;
		private Configuration		conf;

		private BytesWritable		content			= new BytesWritable();

		private long				start			= 0;
		long						end				= 0;
		private long				curr_pos		= 0;
		private long				len				= 0;
		long						fileLength		= 0;

		MessageDigest				md5				= null;

		TaskAttemptContext			context			= null;

		boolean						permissiveMode	= false;

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

		public SpiderPageRecordReader() {
			more = true;
			try {
				md5 = MessageDigest.getInstance("MD5");
			} catch (NoSuchAlgorithmException e) {
				md5 = null;
			}
		}

		@Override
		public void close() throws IOException {
			if (dis != null) {
				dis.close();
			}
		}

		@Override
		public BytesWritable getCurrentKey() throws IOException {
			return key;
		}

		@Override
		public SpiderPageWritable getCurrentValue() throws IOException {
			return value;
		}

		public float getProgress() {
			return more ? (curr_pos - start) / (float) len : 1.0f;
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
				throw new IOException(split.getPath() + " file length error. can not skip " + start + " bytes to read, the file length is "
						+ fileLength);
			}

			long skipLen = 0;
			skipLen = dis.skip(start);
			if (skipLen != start) {
				throw new IOException("skip error when split-read.");
			}

			curr_pos = start;
			len = end - start;

			key = new BytesWritable();
			value = new SpiderPageWritable();

			permissiveMode = conf.getBoolean("SpiderPageRecordReader.permissiveMode", false);
			if (permissiveMode) {
				System.err.println("PERMISSIVE MODE ENABLED, USE WITH CARE");
			}
			String keyFormatLiteral = conf.get("SpiderPageRecordReader.keyFormat", "URL");
			keyFormat = keyFormatFromLiteral(keyFormatLiteral);
		}

		@Override
		public boolean nextKeyValue() throws IOException {
			if (dis != null && PageParseUtil.available(dis, fileLength) != 0 && curr_pos < end) {
				System.err.println("CURRENT POS " + dis.getPos());
				boolean readSucc = false;
				if (key.getLength() == 0) {
					//handle specific case for first record
					while (readSucc == false && PageParseUtil.available(dis, end) > 0) {
						try {
							readSucc = readSpiderPage(dis);
						} catch (IOException e) {
							this.context.getCounter("SpiderPageInputFormatV3", "FIRST-RECORD-RETRY").increment(1);
							e.printStackTrace();
						}
					}
				} else {
					do {
						try {
							readSucc = readSpiderPage(dis);
							break;
						} catch (IOException e) {
							if (permissiveMode) {
								e.printStackTrace();
								this.context.getCounter("SpiderPageInputFormatV3", "PERMISSIVE-SKIP").increment(1);
								continue;
							} else {
								throw e;
							}
						}
					} while (true);
				}
				if (readSucc) {
					if (keyFormat == KeyFormat.URL) {
						key.set(value.url.getBytes(), 0, value.url.getLength());
					} else if (keyFormat == KeyFormat.DOCID256) {
						key.set(new DocId256(value.url.toString()).getDocId256Bytes(), 0, DocId256.BYTE_DOCID_LENGTH);
					} else if (keyFormat == KeyFormat.URLID) {
						key.set(new DocId256(value.url.toString()).getUrlIdBytes(), 0, DocId256.BYTE_URLID_LENGTH);
					}
				}
				else
					return false;
				curr_pos = dis.getPos();

				return true;
			} else {

				more = false;
				return false;
			}
		}

		private boolean readSpiderPage(FSDataInputStream dis) throws IOException {
			clear();

			long pos = dis.getPos();
			String line = null;
			while (PageParseUtil.available(dis, fileLength) > 0) {
				line = PageParseUtil.readLine(dis, fileLength);
				pos = dis.getPos();
				if (pos >= end)
					return false;
				if (line.startsWith("http"))
					break;
			}

			if (line == null || line.startsWith("http") == false)
				return false;

			value.url.set(line);

			boolean metEmptyLine = false;
			while (PageParseUtil.available(dis, fileLength) > 0) {
				line = PageParseUtil.readLine(dis, fileLength);
				if (line.length() == 0) {
					metEmptyLine = true;
					break;
				}
				int attrIdx = value.attributesCount;
				if (attrIdx == value.attributes.size())
					value.attributes.add(new Attribute());
				value.attributesCount++;

				Attribute attr = value.attributes.get(attrIdx);
				int sepIdx = line.indexOf(Attribute.SEP_STRING);
				if (sepIdx != -1) {
					attr.key.set(line.substring(0, sepIdx));
					attr.val.set(line.substring(sepIdx + Attribute.SEP_STRING.length()));
					attr.hasSep = true;
				} else {
					attr.key.set(line);
					attr.val.clear();
					attr.hasSep = false;
				}
			}

			if (!metEmptyLine) {
				if (PageParseUtil.available(dis, fileLength) == 0)
					return false;
				else
					throw new IOException("Premature EOF when reading attributes");
			}

			/*if (!checkPageAttributesMeta(attributes)) {
				return false;
			}*/

			//String type = null;
			//type = PageParseUtil.getValueByKeyName(attributes, "Type", ":");

			Attribute typeAttr = value.getAttribute("Type");
			if (typeAttr == null) {
				if (PageParseUtil.available(dis, fileLength) == 0)
					return false;
				else
					throw new IOException("NO Type Attribute");
			}

			boolean is_compressed = false;
			boolean is_deleted = false;
			boolean is_canceled = false;
			if (typeAttr.val.find("compressed") == 0) {
				is_compressed = true;
			} else if (typeAttr.val.find("normal") == 0) {
				is_compressed = false;
			} else if (typeAttr.val.find("deleted") == 0) {
				is_deleted = true;
			} else if (typeAttr.val.find("canceled") == 0) {
				is_canceled = true;
			} else {
				if (PageParseUtil.available(dis, fileLength) == 0)
					return false;
				else
					throw new IOException("UNKNOWN Type val: " + typeAttr.val);
			}

			if (is_deleted) {
				//page of type deleted has no header nor body
				value.type = PageType.DELETED;
				return true;
			}

			metEmptyLine = false;
			while (PageParseUtil.available(dis, fileLength) != 0) {
				line = PageParseUtil.readLine(dis, fileLength);
				if (line.length() == 0) {
					metEmptyLine = true;
					break;
				}
				int headerIdx = value.headersCount;
				if (headerIdx == value.headers.size())
					value.headers.add(new Attribute());
				value.headersCount++;

				Attribute attr = value.headers.get(headerIdx);
				int sepIdx = line.indexOf(Attribute.SEP_STRING);
				if (sepIdx != -1) {
					attr.key.set(line.substring(0, sepIdx));
					attr.val.set(line.substring(sepIdx + Attribute.SEP_STRING.length()));
					attr.hasSep = true;
				} else {
					attr.key.set(line);
					attr.val.clear();
					attr.hasSep = false;
				}
			}

			if (!metEmptyLine) {
				if (PageParseUtil.available(dis, fileLength) == 0)
					return false;
				else
					throw new IOException("Premature EOF when reading headers");
			}

			if (is_canceled) {
				//page of type canceled has no body
				value.type = PageType.CANCELED;
				return true;
			}

			Attribute storeSizeAttr = value.getAttribute("Store-Size");
			if (storeSizeAttr == null) {
				if (PageParseUtil.available(dis, fileLength) == 0)
					return false;
				else
					throw new IOException("NO Type Store-Size");
			}

			int storeSize = Integer.parseInt(storeSizeAttr.val.toString());

			//content = new byte[store_size];
			content.setSize(storeSize);

			int size = PageParseUtil.readBytes(dis, content.getBytes(), storeSize, fileLength);

			if (size != storeSize) {
				if (PageParseUtil.available(dis, fileLength) == 0)
					return false;
				else
					throw new IOException("Failed to read content of Store-Size");
			}

			value.type = PageType.NORMAL;
			value.isBodyCompressed = is_compressed;
			value.body.set(content.getBytes(), 0, content.getLength());

			return true;
		}

		private void clear() {
			/*url = "";
			is_deleted = false;
			is_compressed = false;
			attributes.clear();
			headers.clear();
			redirects.clear();
			flag = 0;

			key = null;
			value = null;
			content.setSize(0);*/

			value.url.clear();
			value.type = PageType.UNDEFINED;
			value.isBodyCompressed = false;
			value.attributesCount = 0;
			value.headersCount = 0;
			value.redirectsCount = 0;
			value.body.setSize(0);
		}

		private boolean checkPageAttributesMeta(List<String> attributes) {

			String line = "";
			for (int i = 0; i < attributes.size(); i++) {
				line = attributes.get(i);

				if (!line.contains(":")) {
					System.err.println("Bad page meta data, invalid line.");
					return false;
				}
			}

			String version = null;
			if ((version = PageParseUtil.getValueByKeyName(attributes, "Version", ":")) == null) {
				System.err.println("Bad page meta data, missing Version.");
				return false;
			}

			String fetchTime = null;
			if ((fetchTime = PageParseUtil.getValueByKeyName(attributes, "Fetch-Time", ":")) == null) {
				System.err.println("Bad page meta data, missing Fetch-Time.");
				return false;
			}

			String type = null;
			if ((type = PageParseUtil.getValueByKeyName(attributes, "Type", ":")) == null) {
				System.err.println("Bad page meta data, missing Version.");
				return false;
			}

			if (!type.equals("deleted")) {

				String value;
				if ((value = PageParseUtil.getValueByKeyName(attributes, "IP-Address", ":")) == null) {
					System.err.println("Bad page meta data, missing IP-Address.");
					return false;
				}

				if ((value = PageParseUtil.getValueByKeyName(attributes, "Digest", ":")) == null) {
					System.err.println("Bad page meta data, missing Digest.");
					return false;
				}
				if (value.length() != 32) {
					System.err.println("Bad page meta data, invalid digest.");
					return false;
				}

				if ((value = PageParseUtil.getValueByKeyName(attributes, "Store-Size", ":")) == null) {
					System.err.println("Bad page meta data, missing Store-Size.");
					return false;
				}

				if (type == "compressed") {
					if ((value = PageParseUtil.getValueByKeyName(attributes, "Original-Size", ":")) == null) {
						System.err.println("Bad page meta data, missing Original-Size.");
						return false;
					}
				} else {
					line = "Original-size:" + value;
					//this.attributes.add(line);
				}
			}

			return true;
		}
	}

	public static void main(String[] args) throws IOException, InterruptedException {
		SpiderPageRecordReader reader = new SpiderPageRecordReader();
		FileSystem fs = FileSystem.getLocal(new Configuration());
		FSDataInputStream fdis = fs.open(new Path("/home/liyi/gfs/update/pages_consumer/data/service/pages9"));
		File file = new File("/home/liyi/gfs/update/pages_consumer/data/service/pages9");

		int avail = fdis.available();
		reader.dis = fdis;
		reader.fileLength = file.length();
		reader.end = file.length();
		int progress = 0;
		while (reader.nextKeyValue()) {
			progress++;
			if (progress % 1000 == 0)
				System.err.println("Progress: " + progress);
			BytesWritable docId = reader.getCurrentKey();
			SpiderPageWritable opw = reader.getCurrentValue();
			if (opw == null)
				continue;

			//System.out.println(opw.url.toString() + "\t" + opw.body.getLength());
		}
	}
}
