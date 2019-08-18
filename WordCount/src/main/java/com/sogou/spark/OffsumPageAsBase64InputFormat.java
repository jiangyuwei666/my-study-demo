package com.sogou.spark;

import java.io.IOException;
import java.util.Arrays;

import org.apache.commons.codec.binary.Base64;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.DataOutputBuffer;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.InputSplit;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.RecordReader;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapreduce.TaskAttemptID;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.task.TaskAttemptContextImpl;

public class OffsumPageAsBase64InputFormat extends FileInputFormat<Text, Text> {

	private static class OffsumPageAsBase64RecordReader implements RecordReader<Text, Text> {

		org.apache.hadoop.mapreduce.RecordReader<BytesWritable, OffsumPageWritableV2>	recordReaderV2	= null;

		public OffsumPageAsBase64RecordReader(org.apache.hadoop.mapred.FileSplit split, JobConf jobConf, Reporter reporter) throws IOException,
				InterruptedException {
			OffsumPageInputFormatV2 offsumPageInputFormat = new OffsumPageInputFormatV2();
			FileSplit fileSplit = new FileSplit(split.getPath(), split.getStart(), split.getLength(), split.getLocations());
			recordReaderV2 = offsumPageInputFormat.createRecordReader(fileSplit, null);
			recordReaderV2
					.initialize(fileSplit, new TaskAttemptContextImpl(jobConf, new TaskAttemptID(), new StatusReporterGlue(reporter)));
		}

		@Override
		public boolean next(Text key, Text value) throws IOException {
			try {
				if (recordReaderV2.nextKeyValue() == false)
					return false;
				OffsumPageWritableV2 opw = recordReaderV2.getCurrentValue();
				key.set(opw.url);
				DataOutputBuffer dob = new DataOutputBuffer();
				OffsumPageRecordWriter recordWriter = new OffsumPageRecordWriter(dob);
				recordWriter.write(recordReaderV2.getCurrentKey(), recordReaderV2.getCurrentValue());

				Base64 base64 = new Base64(0);
				value.set(base64.encode(Arrays.copyOf(dob.getData(), dob.getLength())));
				return true;

			} catch (InterruptedException e) {
				return false;
			}
		}

		@Override
		public Text createKey() {
			return new Text();
		}

		@Override
		public Text createValue() {
			return new Text();
		}

		@Override
		public long getPos() throws IOException {
			return 0;
		}

		@Override
		public void close() throws IOException {
			recordReaderV2.close();
		}

		@Override
		public float getProgress() throws IOException {
			try {
				return recordReaderV2.getProgress();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			return 0;
		}

	}

	@Override
	public RecordReader<Text, Text> getRecordReader(InputSplit split, JobConf job, Reporter reporter) throws IOException {
		OffsumPageAsBase64RecordReader recordReader = null;
		try {
			recordReader = new OffsumPageAsBase64RecordReader((org.apache.hadoop.mapred.FileSplit) split, job, reporter);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		return recordReader;
	}
}
