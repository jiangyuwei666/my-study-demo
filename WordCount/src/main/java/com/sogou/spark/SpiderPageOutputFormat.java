package com.sogou.spark;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.nio.charset.Charset;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.mapreduce.RecordWriter;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import com.sogou.spark.SpiderPageInputFormatV3.SpiderPageRecordReader;
import com.sogou.spark.SpiderPageWritable.Attribute;

public class SpiderPageOutputFormat extends FileOutputFormat<BytesWritable, SpiderPageWritable> {

	private static class SpiderPageRecordWriter extends RecordWriter<BytesWritable, SpiderPageWritable> {

		private static final String		utf8	= "UTF-8";
		private static final Charset	CHARSET_ASCII;
		private static final byte[]		BYTES_NEWLINE;
		static {
			try {
				BYTES_NEWLINE = "\r\n".getBytes("UTF-8");
				CHARSET_ASCII = Charset.forName("US-ASCII");
			} catch (UnsupportedEncodingException e) {
				throw new IllegalArgumentException("can't find " + utf8 + " encoding");
			}
		}

		protected OutputStream			out;

		public SpiderPageRecordWriter(OutputStream out) {
			this.out = out;
		}

		@Override
		public synchronized void write(BytesWritable key, SpiderPageWritable value) throws IOException {
			//ignore key

			out.write(value.url.toString().getBytes(CHARSET_ASCII));
			out.write(BYTES_NEWLINE);
			for (int i = 0; i < value.attributesCount; i++) {
				Attribute attr = value.attributes.get(i);
				out.write(attr.key.getBytes(), 0, attr.key.getLength());
				if (attr.val.getLength() > 0) {
					out.write(Attribute.SEP_TEXT.getBytes(), 0, Attribute.SEP_TEXT.getLength());
					out.write(attr.val.getBytes(), 0, attr.val.getLength());
				}

				out.write(BYTES_NEWLINE);
			}
			out.write(BYTES_NEWLINE);

			//deleted page has neither header nor content 
			Attribute typeAttr = value.getAttribute("Type");
			if (typeAttr == null)
				throw new IOException("NEED Type in Attributes");

			if (typeAttr.val.toString().equals("deleted"))
				return;

			for (Attribute header : value.headers) {
				out.write(header.key.toString().getBytes(CHARSET_ASCII));
				if (header.val.getLength() > 0) {
					out.write(Attribute.SEP_TEXT.getBytes(), 0, Attribute.SEP_TEXT.getLength());
					out.write(header.val.getBytes(), 0, header.val.getLength());

				}
				out.write(BYTES_NEWLINE);
			}

			out.write(BYTES_NEWLINE);

			//write value
			out.write(value.body.getBytes(), 0, value.body.getLength());

			out.write(BYTES_NEWLINE);

		}

		@Override
		public synchronized void close(TaskAttemptContext context) throws IOException, InterruptedException {
			out.close();
		}

	}

	@Override
	public RecordWriter<BytesWritable, SpiderPageWritable> getRecordWriter(TaskAttemptContext job) throws IOException,
			InterruptedException {
		Path file = getDefaultWorkFile(job, "");
		FileSystem fs = file.getFileSystem(job.getConfiguration());
		FSDataOutputStream fileOut = fs.create(file, false);

		return new SpiderPageRecordWriter(fileOut);
	}

	/**
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub

		SpiderPageRecordWriter writer = new SpiderPageRecordWriter(System.out);

		SpiderPageRecordReader reader = new SpiderPageRecordReader();
		FileSystem fs = FileSystem.getLocal(new Configuration());
		FSDataInputStream fdis = fs.open(new Path("/home/liyi/gfs/update/pages_consumer/data/service/last_20130127/pages0"));
		File file = new File("/home/liyi/gfs/update/pages_consumer/data/service/last_20130127/pages9");

		int avail = fdis.available();
		reader.dis = fdis;
		reader.fileLength = file.length();
		reader.end = file.length();
		int progress = 0;
		while (reader.nextKeyValue()) {
			progress++;
			if (progress % 1000 == 0)
				System.err.println("Progress: " + progress);
			BytesWritable key = reader.getCurrentKey();
			SpiderPageWritable value = reader.getCurrentValue();
			if (key == null)
				continue;

			writer.write(key, value);
			//System.out.println(opw.getUrl() + "\t" + bw.getLength());
		}
	}

}
