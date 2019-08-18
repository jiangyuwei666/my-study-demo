package com.sogou.spark;

import java.util.Map;
import java.util.Iterator;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class NativeAdapter {
	protected byte[] arbeiter;
	private static final Log LOG = LogFactory.getLog(NativeAdapter.class.getName());

	public static String[] buildConfigurationArray(Configuration inputConf) {
		Configuration conf = new Configuration(inputConf);
		//conf.setDeprecatedProperties();
		Iterator it = conf.iterator();
		String[] a = new String[conf.size() * 2];
		int i = 0;
		while (it.hasNext()) {
			Map.Entry en = (Map.Entry) it.next();
			String name = (String) en.getKey();
			String value = conf.get(name);
			a[i] = name;
			++ i;
			a[i] = value;
			++ i;
		}
		return a;
	}

	public void setup(Configuration conf, String build, String library) {
		String buildLibraryCommand = String.format("%s %s", build, library);
		LOG.info(String.format("execute: %s", buildLibraryCommand));
		try {
			Process process = Runtime.getRuntime().exec(buildLibraryCommand);
			process.waitFor();
		} catch (Exception e) {
			System.exit(1);
		}
		String currentFolder = System.getenv("PWD");
		String absoluteLibraryPath = String.format("%s/%s", currentFolder, library);
		LOG.info(String.format("load: %s", absoluteLibraryPath));
		System.load(absoluteLibraryPath);

		String[] configArray = buildConfigurationArray(conf);

		arbeiter = nativeSetup(configArray);
	}
	protected native byte[] nativeSetup(String[] libconf);
	public void map(byte[] rowkey, String[] fieldnames, byte[][] fieldarray, int[] fieldoffset, int[] fieldlength, byte[][] outkeyvalue) {
		nativeMap(arbeiter, rowkey, fieldnames, fieldarray, fieldoffset, fieldlength, outkeyvalue);
	}
	protected native void nativeMap(byte[] arbeiter, byte[] rowkey, String[] fieldnames, byte[][] fieldarray, int[] fieldoffset, int[] fieldlength, byte[][] outkeyvalue);
	public void cleanup() {
		nativeCleanup(arbeiter);
	}
	protected native void nativeCleanup(byte[] arbeiter);

	public static class Test extends Configured implements Tool {
		static protected void writeKeyValueLine(byte[] buffer, int begin, int end) {
			int i;
			for (i = begin; i < end; ++ i) {
				if (buffer[i] == '\t') {
					byte[] key = new byte[i -  begin];
					byte[] value = new byte[end - i - 1];
					System.arraycopy(buffer, begin, key, 0, i - begin);
					System.arraycopy(buffer, i + 1, value, 0, end - i - 1);
					System.out.println(String.format("%s\t%s", new String(key), new String(value)));
					break;
				}
			}
		}
		static protected void writeKeyValueLineList(byte[] buffer) {
			int i;
			int k = 0;
			for (i = 0; i < buffer.length; ++ i) {
				if (buffer[i] == '\n') {
					if (k < i) {
						writeKeyValueLine(buffer, k, i);
					}
					k = i + 1;
				}
			}
		}
		public int run(String[] args) throws IOException, InterruptedException, Exception {
			Configuration conf = getConf();
			NativeAdapter adapter = new NativeAdapter();
			adapter.setup(conf, "sh build.sh", args[0]);
			byte[] key = args[1].getBytes();
			int nf = args.length - 2;
			String[] names = new String[nf];
			byte[][] fields = new byte[nf][];
			int [] offsets = new int[nf];
			int [] lengths = new int[nf];
			for (int i = 2; i < args.length; ++ i) {
				int j = i - 2;
				names[j] = "field" + j;
				fields[j] = args[i].getBytes();
				offsets[j] = 0;
				lengths[j] = fields[j].length;
			}
			byte[][] outkeyvalue = new byte[2][];
			adapter.map(key, names, fields, offsets, lengths, outkeyvalue);
			byte[] outkey = outkeyvalue[0];
			byte[] outvalue = outkeyvalue[1];
			if (outvalue != null) {
				if (outkey == null || outkey.length == 0 || (outkey.length == 1 && outkey[0] == 0)) {
					writeKeyValueLineList(outvalue);
				} else {
					System.out.println(String.format("%s\t%s\n", new String(outkey), new String(outvalue)));
				}
			}
			adapter.cleanup();

			return 0;
		}
	}
	public static void main(String[] args) throws IOException, Exception {
		Tool tool = new Test();
		ToolRunner.run(new Configuration(), tool, args);
	}
}

