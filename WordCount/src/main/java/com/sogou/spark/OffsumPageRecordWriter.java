package com.sogou.spark;

import java.io.IOException;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.nio.charset.Charset;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.mapreduce.RecordWriter;
import org.apache.hadoop.mapreduce.TaskAttemptContext;

public class OffsumPageRecordWriter extends RecordWriter<BytesWritable, OffsumPageWritableV2> {

	private static final String		utf8	= "UTF-8";
	private static final Charset	CHARSET_ASCII;
	private static final byte[]		BYTES_NEWLINE;
	static {
		try {
			BYTES_NEWLINE = "\n".getBytes("UTF-8");
			CHARSET_ASCII = Charset.forName("US-ASCII");
		} catch (UnsupportedEncodingException e) {
			throw new IllegalArgumentException("can't find " + utf8 + " encoding");
		}
	}

	protected OutputStream			out;

	public OffsumPageRecordWriter(OutputStream out) {
		this.out = out;
	}

	@Override
	public synchronized void write(BytesWritable key, OffsumPageWritableV2 value) throws IOException {
		//ignore key

		out.write(value.url.toString().getBytes(CHARSET_ASCII));
		out.write(BYTES_NEWLINE);
		for (String attribute : value.attributes) {
			if (attribute.startsWith("Content-Type") == false && attribute.startsWith("Original-Size") == false) {
				out.write(attribute.getBytes(CHARSET_ASCII));
				out.write(BYTES_NEWLINE);
			}
		}
		StringBuilder contentType = new StringBuilder("Content-Type: ");
		StringBuilder originalSize = new StringBuilder("Original-Size: ");
		for (OffsumPageWritableV2.ContentItem contentItem : value.contentItems) {
			contentType.append(contentItem.type).append(", ").append(contentItem.storeSize).append(';');
			originalSize.append(contentItem.type).append(", ").append(contentItem.originalSize).append(';');
		}
		out.write(contentType.toString().getBytes(CHARSET_ASCII));
		out.write(BYTES_NEWLINE);
		out.write(originalSize.toString().getBytes(CHARSET_ASCII));
		out.write(BYTES_NEWLINE);

		out.write(BYTES_NEWLINE);

		for (OffsumPageWritableV2.ContentItem contentItem : value.contentItems) {
			out.write(contentItem.content, 0, contentItem.storeSize);
		}

		out.write(BYTES_NEWLINE);
	}

	@Override
	public synchronized void close(TaskAttemptContext context) throws IOException, InterruptedException {
		out.close();
	}

}