package com.sogou.spark;

import java.io.IOException;
import java.io.OutputStream;

import org.apache.commons.codec.binary.Base64;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DataOutputBuffer;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.RecordWriter;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.util.Progressable;
import org.apache.log4j.Logger;

public class OffsumPageAsBase64OutputFormat extends FileOutputFormat<Text, Text> {

	private static class OffsumPageAsBase64RecordWriter implements RecordWriter<Text, Text> {
		OutputStream	out	= null;
		Logger LOG = Logger.getLogger(OffsumPageAsBase64RecordWriter.class);

		public OffsumPageAsBase64RecordWriter(FSDataOutputStream fileOut) {
			this.out = fileOut;
		}

		@Override
		public void write(Text key, Text value) throws IOException {
			Base64 base64 = new Base64(0);
			byte[] decoded = base64.decode(value.copyBytes());
			OffsumPageWritableV2 opw = new OffsumPageWritableV2();
			int rc = opw.buildFromBytes(decoded, false);
			if( rc != 0 ) {
				LOG.warn("Wrong format for record url: " + key);
			} else {
				DataOutputBuffer dob = new DataOutputBuffer();
				//opw.writeSpiderPage(dob);
				OffsumPageRecordWriter writer = new OffsumPageRecordWriter(dob);
				writer.write(null, opw);
				out.write(dob.getData(), 0, dob.getLength());
			}
		}

		@Override
		public void close(Reporter reporter) throws IOException {
			this.out.close();
		}

	}

	@Override
	public RecordWriter<Text, Text> getRecordWriter(FileSystem ignored, JobConf job, String name, Progressable progress) throws IOException {
		OffsumPageAsBase64RecordWriter recordWriter = null;
		Path file = FileOutputFormat.getTaskOutputPath(job, name);
		FileSystem fs = file.getFileSystem(job);
		FSDataOutputStream fileOut = fs.create(file, progress);
		recordWriter = new OffsumPageAsBase64RecordWriter(fileOut);
		return recordWriter;
	}

}
