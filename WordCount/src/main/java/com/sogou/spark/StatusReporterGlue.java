package com.sogou.spark;

import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapreduce.StatusReporter;

public class StatusReporterGlue extends StatusReporter {

	Reporter	reporter	= null;

	public StatusReporterGlue(Reporter reporter) {
		this.reporter = reporter;
	}

	@Override
	public org.apache.hadoop.mapreduce.Counter getCounter(Enum<?> name) {
		return reporter.getCounter(name);
	}

	@Override
	public org.apache.hadoop.mapreduce.Counter getCounter(String group, String name) {
		return reporter.getCounter(group, name);
	}

	@Override
	public void progress() {
	}

	@Override
	public float getProgress() {
		return reporter.getProgress();
	}

	@Override
	public void setStatus(String status) {
		reporter.setStatus(status);
	}

}