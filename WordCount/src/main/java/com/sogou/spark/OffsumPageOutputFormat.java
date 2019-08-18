package com.sogou.spark;

import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.nio.charset.Charset;
import java.util.Iterator;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.mapreduce.RecordWriter;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import com.sogou.spark.OffsumPageInputFormatV2.OffsumPageRecordReader;

public class OffsumPageOutputFormat extends FileOutputFormat<BytesWritable, OffsumPageWritableV2> {

	@Override
	public RecordWriter<BytesWritable, OffsumPageWritableV2> getRecordWriter(TaskAttemptContext job) throws IOException,
			InterruptedException {
		Path file = getDefaultWorkFile(job, "");
		FileSystem fs = file.getFileSystem(job.getConfiguration());
		FSDataOutputStream fileOut = fs.create(file, false);

		return new OffsumPageRecordWriter(fileOut);
	}

	/**
	 * @param args
	 * @throws IOException
	 * @throws InterruptedException
	 */
	public static void main(String[] args) throws IOException, InterruptedException {
		// TODO Auto-generated method stub

		OffsumPageRecordWriter writer = new OffsumPageRecordWriter(System.out);

		OffsumPageRecordReader reader = new OffsumPageRecordReader();
		FileSystem fs = FileSystem.getLocal(new Configuration());
		FSDataInputStream fdis = fs.open(new Path(args[0]));
		File file = new File(args[0]);

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
			OffsumPageWritableV2 value = reader.getCurrentValue();
			if (key == null) {
				System.err.println("ERROR READING KEY");
				continue;
			}

			Iterator<OffsumPageWritableV2.ContentItem> iter = value.contentItems.iterator();
			while (iter.hasNext()) {
				OffsumPageWritableV2.ContentItem ci = iter.next();
				if (ci.type.equals("xmlpage") == false && ci.type.equals("snapshot") == false)
					iter.remove();
				else {
					byte[] output = new byte[ci.originalSize];
					Inflater decompresser = new Inflater();
					decompresser.setInput(ci.content);
					int resultLength;
					try {
						resultLength = decompresser.inflate(output);
						if (resultLength != ci.originalSize)
							throw new DataFormatException();
					} catch (DataFormatException e) {
						System.err.println("ERROR DECOMPRESS " + ci.type + " OF " + value.url);
					}
					decompresser.end();
				}
			}

			writer.write(key, value);
			//System.out.println(opw.getUrl() + "\t" + bw.getLength());
		}
	}

}
