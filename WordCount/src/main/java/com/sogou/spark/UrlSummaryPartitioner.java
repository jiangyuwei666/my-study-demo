package com.sogou.spark;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.*;
//import org.apache.hadoop.mapred.*;

import java.util.Arrays;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

import org.apache.commons.codec.DecoderException;
import org.apache.commons.codec.binary.Hex;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.Partitioner;

public class UrlSummaryPartitioner<K2, V2> implements Partitioner<K2, V2> {
	private static final Log LOG = LogFactory.getLog(UrlSummaryPartitioner.class.getName());
	private int baseIndex = 0;
	private boolean byHostId = false;

	private static final Pattern DOCID = Pattern.compile("^[0-9a-f]{16}-[0-9a-f]{16}-[0-9a-f]{32}$");
	private static final Pattern URLID = Pattern.compile("^[0-9a-f]{32}$");
	private static final Pattern HTTPURL = Pattern.compile("^http://.*$");
	private static final Pattern HTTPSURL = Pattern.compile("^https://.*$");
	private static final Pattern HOSTID = Pattern.compile("^[0-9a-f]{16}$");

	private long[] byUrlIdSiteSet = null;

	public static boolean isDocId(String s) {
		return DOCID.matcher(s).matches();
	}

	public static boolean isUrlId(String s) {
		return URLID.matcher(s).matches();
	}

	public static boolean isHttpUrl(String s) {
		return HTTPURL.matcher(s).matches();
	}

	public static boolean isHttpsUrl(String s) {
		return HTTPSURL.matcher(s).matches();
	}

	public static boolean isHostId(String s) {
		return HOSTID.matcher(s).matches();
	}

	static byte[] getStringUTF8Bytes(String s) {
		try {
				return s.getBytes("UTF-8");
		} catch (UnsupportedEncodingException e) {
			throw new RuntimeException("The current system does not support UTF-8 encoding!", e);
		}
	}

	static private byte[] getObjectBytes(Object o) {
		if (o instanceof Text) {
			Text to = (Text) o;
			return to.copyBytes();
		} else if (o instanceof BytesWritable) {
			BytesWritable bytes = (BytesWritable) o;        
			return bytes.copyBytes();
		} else {
			return getStringUTF8Bytes(o.toString());
		}
	}

	static protected byte[] calculateMD5(byte[] b) {
		try {
			MessageDigest messageDigest = MessageDigest.getInstance("MD5"); 
			messageDigest.update(b);
			return messageDigest.digest();
		} catch (NoSuchAlgorithmException e) {
			throw new RuntimeException("The current system does not support MD5!", e);
		}
	}

	static protected byte[] decodeId(String id) {
		try {
			Hex decoder = new Hex("UTF-8");
			return decoder.decode(id.getBytes("UTF-8"));
		} catch (DecoderException e) {
			throw new RuntimeException("The current system does not support HEX encoding!", e);
		} catch (UnsupportedEncodingException e) {
			throw new RuntimeException("The current system does not support UTF-8 encoding!", e);
		}
	}

	static protected long getRangeLong(byte[] md, int start, int n) {
		//long hashNumber = (md[i] & 0xFFL) | ( (md[i + 1] & 0xFFL) << 8) | ( (md[i + 2] & 0xFFL) << 16) | ( (md[i + 3] & 0xFFL) << 24);
		long res = 0;
		if (md != null) {
			int i = start;
			int j = 0;
			while (i < md.length && j < n) {
				res |= ((md[i] & 0xFFL) << (j * 8));
				++ i;
				++ j;
			}
		}
		return res;
	}

	static protected long hashUrl(byte[] b) {
		byte[] md = calculateMD5(b);
		return getRangeLong(md, 1, 4);
	}

	static protected long hashHost(byte[] b) {
		byte[] md = calculateMD5(b);
		return getRangeLong(md, 0, 4);
	}

	static protected long extractUrlIdHash(String id) {
		byte[] md = decodeId(id);
		return getRangeLong(md, 1, 4);
	}

	static protected long extractHostIdHash(String id) {
		byte[] md = decodeId(id);
		return getRangeLong(md, 0, 4);
	}

	static protected long getHashNumber(String key, boolean byHostId) {
		long hashNumber;
		if (isDocId(key)) {
			//System.err.println("DOCID: " + key);
			if (byHostId) {
				hashNumber = extractHostIdHash(key.substring(17,33));
			} else {
				hashNumber = extractUrlIdHash(key.substring(34));
			}
		} else if (isUrlId(key)) {
			//System.err.println("URLID: " + key);
			hashNumber = extractUrlIdHash(key);
		} else {
			if (byHostId) {
				int p = -1;
				if (isHttpUrl(key)) {
					//System.err.println("HTTP: " + key);
					p = key.indexOf('/', 7);
				} else if (isHttpsUrl(key)) {
					//System.err.println("HTTPS: " + key);
					p = key.indexOf('/', 8);
				}
				//System.err.println(p);
				if (p == -1) {
					p = key.length();
				}
				String host = key.substring(0, p);
				//System.err.println(strHost);
				hashNumber = hashHost(getObjectBytes(host));
			} else {
				hashNumber = hashUrl(getObjectBytes(key));
			}
		}
		return hashNumber;
	}

	static protected int getHashNumberPartition(long hashNumber, int numReduceTasks, int baseIndex) {
		return (int)((hashNumber * (long)(numReduceTasks - baseIndex)) >> 32) + baseIndex;
	}

	static protected long calculateHostKey(String host) {
		byte[] md = calculateMD5(getStringUTF8Bytes(host));
		return getRangeLong(md, 0, 8);
	}

	static protected long extractHostKey(String hostId) {
		byte[] md = decodeId(hostId);
		return getRangeLong(md, 0, 8);
	}

	static public final long EMPTYHOSTKEY = calculateHostKey("");

	static long getHostKey(String site) {
		String host = "";
		String hostId = "";
		if (isHttpUrl(site)) {
			int p = site.indexOf('/', 7);
			if (p != -1) {
				host = site.substring(0, p);
			} else {
				host = site;
			}
		} else if (isHttpsUrl(site)) {
			int p = site.indexOf('/', 8);
			if (p != -1) {
				host = site.substring(0, p);
			} else {
				host = site;
			}
		} else if (isHostId(site)) {
			hostId = site;
		} else if (isDocId(site)) {
			hostId = site.substring(17, 33);
		}
		if (!hostId.isEmpty()) {
			return extractHostKey(hostId);
		} else if (!host.isEmpty()) {
			return calculateHostKey(host);
		}
		return EMPTYHOSTKEY;
	}

	static protected int addHostKey(String site, long[] longset, int i) {
		long key = getHostKey(site);
		if (key == EMPTYHOSTKEY) {
			String host;
			host = "http://";
			host += site;
			longset[i] = calculateHostKey(host);
			LOG.info(String.format("addHostKey %s %d", host, longset[i]));
			i ++;
			host = "https://";
			host += site;
			longset[i] = calculateHostKey(host);
			LOG.info(String.format("addHostKey %s %d", host, longset[i]));
			i ++;
			return i;
		} else {
			longset[i] = key;
			LOG.info(String.format("addHostKey %s %d", site, longset[i]));
			i ++;
		}
		return i;
	}

	static public long[] buildUrlIdSites(String byUrlIdSites) {
		String[] sites = byUrlIdSites.split(",");
		long[] longset = new long[sites.length * 2];
		int n = 0;
		for (String site : sites) {
			n = addHostKey(site, longset, n);
		}
		long[] ret = new long[n];
		System.arraycopy(longset, 0, ret, 0, n);
		Arrays.sort(ret);
		return ret;
	}

	public void setByUrlIdSites(String byUrlIdSites) {
		byUrlIdSiteSet = buildUrlIdSites(byUrlIdSites);
	}

	public void configure(JobConf job) {
		baseIndex = job.getInt("summarypartition.baseindex", 0);
		byHostId = job.getBoolean("summarypartition.byhostid", false);
		String byUrlIdSites = job.get("summarypartition.byurlidsite", "");
		if (byUrlIdSites.length() > 0) {
			setByUrlIdSites(byUrlIdSites);
		}
	}

	static public int getKeyPartition(Object objectKey, int numReduceTasks, int baseIndex, boolean byHostId, long[] byUrlIdSiteSet) {
		String key = objectKey.toString();
		if (byHostId && null != byUrlIdSiteSet) {
			long hostKey = getHostKey(key);
			//System.out.println(String.format("%s %s", key, hostKey));
			byHostId = (!(Arrays.binarySearch(byUrlIdSiteSet, hostKey) >= 0));
			//System.out.println(String.format("URL %s key %s byHostId %s", key, hostKey, byHostId));
		}
		long hashNumber = getHashNumber(key, byHostId);
		return getHashNumberPartition(hashNumber, numReduceTasks, baseIndex);
	}

	public int getPartition(K2 key, V2 value, int numReduceTasks) {
		return getKeyPartition(key, numReduceTasks, baseIndex, byHostId, byUrlIdSiteSet);
	}

	public static void main(String[] args) {
		int i = 0;
		int cc = 65536;
		int baseIndex = 0;
		boolean byHostId = false;
		long[] byUrlIdSiteSet = null;
		for (i = 0; i + 1 < args.length; i += 2) {
			String option = args[i];
			String value = args[i + 1];
			if (option.equals("-n")) {
				cc = Integer.parseInt(value);
			} else if (option.equals("-b")) {
				baseIndex = Integer.parseInt(value);
			} else if (option.equals("--byhostid")) {
				byHostId = (value.equals("true") || value.equals("yes"));
			} else if (option.equals("--byurlidsite")) {
				byUrlIdSiteSet = buildUrlIdSites(value);
			}
		}
		try {
			BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
			String key;
			while ((key = reader.readLine()) != null) {
				System.out.println(key + "\t" + getKeyPartition(key, cc, baseIndex, byHostId, byUrlIdSiteSet));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
