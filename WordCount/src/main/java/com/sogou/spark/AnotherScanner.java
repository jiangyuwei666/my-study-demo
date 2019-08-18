package com.sogou.spark;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;
import java.util.Vector;

import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.MapContext;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.sogou.spark.SpiderPageInputFormatV3;
import com.sogou.spark.SpiderPageWritable;
import com.sogou.spark.SpiderPageWritable.Attribute;
import com.sogou.spark.OffsumPageInputFormatV2;
import com.sogou.spark.OffsumPageWritableV2;
import com.sogou.spark.OffsumPageWritableV2.ContentItem;

import com.sogou.spark.NativeAdapter;

public class AnotherScanner extends Configured implements Tool {
	private static final Log LOG = LogFactory.getLog(AnotherScanner.class.getName());

	static protected void writeKeyValueLine(byte[] buffer, int begin, int end, MapContext context) throws IOException, InterruptedException {
		int i;
		for (i = begin; i < end; ++ i) {
			if (buffer[i] == '\t') {
				Text key = new Text();
				Text value = new Text();
				key.set(buffer, begin, i - begin);
				value.set(buffer, i + 1, end - i - 1);
				context.write(key, value);
				break;
			}
		}
	}

	static protected void writeKeyValueLineList(byte[] buffer, MapContext context) throws IOException, InterruptedException {
		int i;
		int k = 0;
		for (i = 0; i < buffer.length; ++ i) {
			if (buffer[i] == '\n') {
				if (k < i) {
					writeKeyValueLine(buffer, k, i, context);
				}
				k = i + 1;
			}
		}
	}

	static protected void outputKeyValue(byte[] outkey, byte[] outvalue, MapContext context) throws IOException, InterruptedException {
		if (outvalue != null) {
			if (outkey == null || outkey.length == 0 || (outkey.length == 1 && outkey[0] == 0)) {
				writeKeyValueLineList(outvalue, context);
			} else {
				Text key = new Text();
				Text value = new Text();
				key.set(outkey);
				value.set(outvalue);
				context.write(key, value);
			}
		}
	}

	public static String getInputSplitFileName(InputSplit split) {
		Class<? extends InputSplit> splitClass = split.getClass();
		FileSplit fileSplit = null;
		if (splitClass.equals(FileSplit.class)) {
			fileSplit = (FileSplit) split;
		} else if (splitClass.getName().equals("org.apache.hadoop.mapreduce.lib.input.TaggedInputSplit")) {
			try {
				Method getInputSplitMethod = splitClass.getDeclaredMethod("getInputSplit");
				getInputSplitMethod.setAccessible(true);
				fileSplit = (FileSplit) getInputSplitMethod.invoke(split);
			} catch (NoSuchMethodException e) {
				return "";
			} catch (IllegalAccessException e) {
				return "";
			} catch (InvocationTargetException e) {
				return "";
			}
		} else {
			return "";
		}
		return fileSplit.getPath().toString();
	}

	public static String getLibraryNameOfPath(Configuration conf, String inputPathLiteral) {
		LOG.info(String.format("inputPathLiteral %s", inputPathLiteral));
		int n = conf.getInt("AnotherScanner.mapper.count", 0);
		LOG.info(String.format("count %d", n));
		for (int i = 1; i <= n; ++ i) {
			MapperSetting setting = new MapperSetting();
			setting.fromString(conf.get("AnotherScanner.mapper." + i));
			if (inputPathLiteral.indexOf(setting.pathPattern) >= 0) {
					return setting.name;
			}
		}
		return "";
	}

	public static enum MapperType {
		UNKNOWN, CLASS, NATIVE, COMMAND
	}

	public static String literalFromMapperType(MapperType type) {
		if (type == MapperType.UNKNOWN) {
			return "";
		} else if (type == MapperType.CLASS) {
			return "CLASS";
		} else if (type == MapperType.NATIVE) {
			return "NATIVE";
		} else if (type == MapperType.COMMAND) {
			return "COMMAND";
		}
		return "";
	}

	public static MapperType mapperTypeFromLiteral(String literal) {
		if (literal.equalsIgnoreCase("command")) {
			return MapperType.COMMAND;
		} else if (literal.equalsIgnoreCase("native")) {
			return MapperType.NATIVE;
		} else if (literal.equalsIgnoreCase("class")) {
			return MapperType.CLASS;
		}
		return MapperType.UNKNOWN;
	}

	public static class MapperSetting {
		public MapperType type;
		public String name;
		public String pathPattern;
		public String format;
		public String stringify() {
			String s = literalFromMapperType(type);
			s += "#"; s += name;
			s += "#"; s += pathPattern;
			s += "#"; s += format;
			return s;
		}
		public void fromString(String s) {
			String[] parts = s.split("#");
			type = mapperTypeFromLiteral(parts[0]);
			name = parts[1];
			pathPattern = parts[2];
			format = parts[3];
		}
	}

	public static class SpiderPageMapper extends Mapper<BytesWritable, SpiderPageWritable, Text, Text> {

		final static int SpiderPageFieldCount = 4;

		String[] fieldnames_ = new String[SpiderPageFieldCount];
		byte[][] fieldarray_ = new byte[SpiderPageFieldCount][];
		int[] fieldoffset_ = new int[SpiderPageFieldCount];
		int[] fieldlength_ = new int[SpiderPageFieldCount];

		byte[][] outkeyvalue_ = new byte[2][];

		NativeAdapter adapter = new NativeAdapter();

		@Override
		protected void setup(Context context) throws IOException, InterruptedException {
			Configuration conf = context.getConfiguration();
			InputSplit split = context.getInputSplit();
			String inputPathLiteral = getInputSplitFileName(split);
			String library = getLibraryNameOfPath(conf, inputPathLiteral);
			String build = conf.get("AnotherScanner.native.build", "sh build.sh");
			adapter.setup(context.getConfiguration(), build, library);
		}

		@Override
		protected void map(BytesWritable key, SpiderPageWritable value, Context context) throws IOException, InterruptedException {
			if (key == null) {
				context.getCounter("ERROR", "NULL-KEY").increment(1);
				return;
			}
			if (value == null) {
				context.getCounter("ERROR", "NULL-VALUE").increment(1);
				return;
			}

			fieldnames_[0] = "url";
			fieldarray_[0] = value.url.getBytes();
			fieldoffset_[0] = 0;
			fieldlength_[0] = value.url.getLength();

			fieldnames_[1] = "fetch-header";
			fieldarray_[1] = null; // TODO
			fieldoffset_[1] = 0;
			fieldlength_[1] = 0;

			fieldnames_[2] = "http-header";
			fieldarray_[2] = null; // TODO
			fieldoffset_[2] = 0;
			fieldlength_[2] = 0;

			if (value.isBodyCompressed) {
				fieldnames_[3] = "compressed-html";
			} else {
				fieldnames_[3] = "html";
			}
			fieldarray_[3] = value.body.getBytes();
			fieldoffset_[3] = 0;
			fieldlength_[3] = value.body.getLength();

			outkeyvalue_[0] = null;
			outkeyvalue_[1] = null;

			adapter.map(key.getBytes(), fieldnames_, fieldarray_, fieldoffset_, fieldlength_, outkeyvalue_);

			byte[] outkey = outkeyvalue_[0];
			byte[] outvalue = outkeyvalue_[1];

			outputKeyValue(outkey, outvalue, context);
		}

		@Override
		protected void cleanup(Context context) throws IOException, InterruptedException {
			adapter.cleanup();
		}
	}

	public static class OffsumPageMapper extends Mapper<BytesWritable, OffsumPageWritableV2, Text, Text> {

		protected byte[][] outkeyvalue_ = new byte[2][];

		NativeAdapter adapter = new NativeAdapter();

		@Override
		protected void setup(Context context) throws IOException, InterruptedException {
			Configuration conf = context.getConfiguration();
			InputSplit split = context.getInputSplit();
			String inputPathLiteral = getInputSplitFileName(split);
			String library = getLibraryNameOfPath(conf, inputPathLiteral);
			String build = conf.get("AnotherScanner.native.build", "sh build.sh");
			adapter.setup(context.getConfiguration(), build, library);
		}

		@Override
		protected void map(BytesWritable key, OffsumPageWritableV2 value, Context context) throws IOException, InterruptedException {
			if (key == null) {
				context.getCounter("ERROR", "NULL-KEY").increment(1);
				return;
			}
			if (value == null) {
				context.getCounter("ERROR", "NULL-VALUE").increment(1);
				return;
			}

			int fieldCount = value.contentItems.size() + 2;
			String[] fieldnames = new String[fieldCount];
			byte[][] fieldarray = new byte[fieldCount][];
			int[] fieldoffset = new int[fieldCount];
			int[] fieldlength = new int[fieldCount];

			fieldnames[0] = "url";
			byte[] url = value.url.getBytes();
			fieldarray[0] = url;
			fieldoffset[0] = 0;
			fieldlength[0] = url.length;

			fieldnames[1] = "header";
			fieldarray[1] = null; // TODO
			fieldoffset[1] = 0;
			fieldlength[1] = 0;

			for (int i = 0; i < value.contentItems.size(); ++ i) {
				int j = i + 2;
				ContentItem ci = value.contentItems.get(i);
				fieldnames[j] = ci.type;
				fieldarray[j] = ci.content;
				fieldoffset[j] = 0;
				fieldlength[j] = ci.content.length;
			}

			outkeyvalue_[0] = null;
			outkeyvalue_[1] = null;

			adapter.map(key.getBytes(), fieldnames, fieldarray, fieldoffset, fieldlength, outkeyvalue_);

			byte[] outkey = outkeyvalue_[0];
			byte[] outvalue = outkeyvalue_[1];

			outputKeyValue(outkey, outvalue, context);
		}

		@Override
		protected void cleanup(Context context) throws IOException, InterruptedException {
			adapter.cleanup();
		}
	}

	public static class TsvMapper extends Mapper<LongWritable, Text, Text, Text> {

		protected byte seperator = '\t';

		byte[][] outkeyvalue_ = new byte[2][];

		NativeAdapter adapter = new NativeAdapter();

		public static int countFields(byte[] line, int length, byte seperator) {
			int i;
			int n = 1;
			for (i = 0; i < length; ++ i) {
				if (line[i] == seperator) {
					++ n;
				}
			}
			return n;
		}

		@Override
		protected void setup(Context context) throws IOException, InterruptedException {
			Configuration conf = context.getConfiguration();
			InputSplit split = context.getInputSplit();
			String inputPathLiteral = getInputSplitFileName(split);
			String library = getLibraryNameOfPath(conf, inputPathLiteral);
			String build = conf.get("AnotherScanner.native.build", "sh build.sh");
			adapter.setup(context.getConfiguration(), build, library);
		}

		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			//LOG.info("TsvMapper.map");

			byte[] line = value.getBytes();
			int length = value.getLength();

			int fieldCount = countFields(line, length, seperator);

			String[] fieldnames = new String[fieldCount];
			byte[][] fieldarray = new byte[fieldCount][];
			int[] fieldoffset = new int[fieldCount];
			int[] fieldlength = new int[fieldCount];

			int f = 0;
			int start = 0;
			for (int i = 0; i < length; ++ i) {
				if (line[i] == seperator) {
					fieldnames[f] = String.format("$%d", f + 1);
					fieldarray[f] = line;
					fieldoffset[f] = start;
					fieldlength[f] = i - start;
					start = i + 1;
					++ f;
				}
			}
			fieldnames[f] = String.format("$%d", f + 1);
			fieldarray[f] = line;
			fieldoffset[f] = start;
			fieldlength[f] = length - start;

			outkeyvalue_[0] = null;
			outkeyvalue_[1] = null;

			adapter.map(key.toString().getBytes(), fieldnames, fieldarray, fieldoffset, fieldlength, outkeyvalue_);

			byte[] outkey = outkeyvalue_[0];
			byte[] outvalue = outkeyvalue_[1];

			outputKeyValue(outkey, outvalue, context);
		}

		@Override
		protected void cleanup(Context context) throws IOException, InterruptedException {
			LOG.info("TsvMapper.cleanup");
			adapter.cleanup();
		}
	}

	protected static MapperSetting matchSetting(String pathLiteral, ArrayList<MapperSetting> mapperSettings) {
		for (int i = 0; i < mapperSettings.size(); ++ i) {
			MapperSetting setting = mapperSettings.get(i);
			if (pathLiteral.indexOf(setting.pathPattern) >= 0) {
				return setting;
			}
		}
		return null;
	}
	protected static void configJob(Job job, Configuration conf, String[] args) throws IOException {
		ArrayList<String> collectedPaths = new ArrayList<String>(args.length);
		ArrayList<MapperSetting> mapperSettings = new ArrayList<MapperSetting>(args.length);
		int i = 0;
		while (i < args.length) {
			String option = args[i];
			if (option.equals("-input")) {
				i ++;
				while (i < args.length && args[i].charAt(0) != '-' ) {
					String pathLiteral = args[i];
					collectedPaths.add(pathLiteral);
					i ++;
				}
			} else if (option.equals("-mapper")) {
				i ++;
				int j = i;
				while (i < args.length && args[i].charAt(0) != '-') {
					++ i;
				}
				MapperSetting setting = new MapperSetting();
				if (j < i) {
					setting.type = mapperTypeFromLiteral(args[j]);
					if (setting.type == MapperType.UNKNOWN) {
						LOG.error(String.format("Unknown mapper type %s", args[j]));
						System.exit(1);
					}
				}
				if (j + 1 < i) {
					setting.name = args[j + 1];
				}
				if (j + 2 < i) {
					setting.pathPattern = args[j + 2];
				}
				if (j + 3 < i) {
					setting.format = args[j + 3];
				}
				mapperSettings.add(setting);
				job.getConfiguration().set("AnotherScanner.mapper." + mapperSettings.size(), setting.stringify());
			} else if (option.equals("-output")) {
				i ++;
				String outputPathLiteral = args[i];
				FileOutputFormat.setOutputPath(job, new Path(outputPathLiteral));
				i ++;
			}
		}
		if (mapperSettings.size() == 0) {
			LOG.error("No mapper");
			System.exit(1);
		}
		FileSystem hdfs = FileSystem.get(conf);
		for (i = 0; i < collectedPaths.size(); ++ i) {
			String pathLiteral = collectedPaths.get(i);
			Path path = new Path(pathLiteral);
			hdfs.exists(path);

			MapperSetting setting = matchSetting(pathLiteral, mapperSettings);
			if (setting == null) {
				setting = mapperSettings.get(0);
			}
			if (setting.format == null) {
				MultipleInputs.addInputPath(job, path, TextInputFormat.class, TsvMapper.class);
			} else if (setting.format.equals("SpiderPage")) {
				MultipleInputs.addInputPath(job, path, SpiderPageInputFormatV3.class, SpiderPageMapper.class);
			} else if (setting.format.equals("OffsumPage")) {
				MultipleInputs.addInputPath(job, path, OffsumPageInputFormatV2.class, OffsumPageMapper.class);
			} else {
				LOG.error(String.format("unknown data format %s", setting.format));
				System.exit(1);
			}
		}
		int mapperCount = mapperSettings.size();
		job.getConfiguration().setInt("AnotherScanner.mapper.count", mapperCount);

		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
	}
	@Override
	public int run(String[] args) throws IOException, InterruptedException, Exception {
		Configuration conf = getConf();
		String jobName = conf.get("mapreduce.job.name", "AnotherScanner");
		Job job = new Job(conf, jobName);

		job.setJarByClass(AnotherScanner.class);
		configJob(job, conf, args);
		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws IOException, Exception {
		Tool tool = new AnotherScanner();
		ToolRunner.run(new Configuration(), tool, args);
	}
}
