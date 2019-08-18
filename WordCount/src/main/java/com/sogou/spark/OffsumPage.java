package com.sogou.spark;

import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

public class OffsumPage implements Comparable<OffsumPage> {

	public static class ContentItem {
		public String type = "";
		public int storeSize = 0;
		public int originalSize = 0;
		public byte[] content = new byte[0];

	};

	public int compareTo(OffsumPage o) {
		return url.compareTo(o.url);
	}

	public String url = null;

	public boolean isDeleted = false;

	public List<String> attributes = new ArrayList<String>();

	public List<ContentItem> contentItems = new ArrayList<ContentItem>(4);

	public OffsumPage() {
	}

	public OffsumPage(String url, boolean is_deleted, List<String> attributes, List<ContentItem> contentItems) {
		this.url = url;
		this.isDeleted = is_deleted;
		this.attributes = attributes;
		this.contentItems = contentItems;
	}

	    public byte[] getContent(String contentTypeLiteral)
	    {
	        for(Iterator<ContentItem> iterator = contentItems.iterator(); iterator.hasNext();) {
	            ContentItem ci = (ContentItem)iterator.next();
	            if (ci.type.equals(contentTypeLiteral)) {
	                byte content[] = new byte[ci.originalSize];
	                Inflater decompresser = new Inflater();
	                decompresser.setInput(ci.content);
	                int resultLength;
	                try {
	                    resultLength = decompresser.inflate(content);
	                } catch(DataFormatException e) {
	                    e.printStackTrace();
	                    return null;
	                }
	                decompresser.end();
	                return content;
	            }
	        }

	        return null;
	    }
	
	public byte[] formatToBytes() {
		throw new RuntimeException("not support yet");
	}

	public int buildFromBytes(byte[] bytes, boolean verbose) {
		this.attributes.clear();
		this.contentItems.clear();
		this.isDeleted = false;
		this.url = null;

		try {

			ByteArrayInputStream dais = new ByteArrayInputStream(bytes);
			DataInputStream dis = new DataInputStream(dais);

			url = null;

			while (dis.available() > 0 && (url = PageParseUtil.readLine(dis)) != null) {
				if (url.startsWith("http")) {
					break;
				}
			}

			if (url == null || url.trim().length() == 0) {
				return -1;
			}

			int ret = -1;
			String line = "";
			while (dis.available() > 0 && (line = PageParseUtil.readLine(dis)) != null) {
				if (line.length() == 0) {
					ret = 0;
					break;
				}
				attributes.add(line);
			}

			if (ret != 0) {
				System.err.println("Read attributes error." + url);
				return -3;
			}

			String type;
			if ((type = PageParseUtil.getValueByKeyName(attributes, "Type", ":")) != null) {
				if (type == "deleted") {
					this.isDeleted = true;
					return -4;
				}
			}

			int storeSizeFull = 0;
			if ((type = PageParseUtil.getValueByKeyName(attributes, "Content-Type", ":")) != null) {
				String[] ctSize = type.split(";");
				for (int i = 0; i < ctSize.length; i++) {
					// contenttype.add(ctSize[i]);

					int pos_comma = ctSize[i].indexOf(',');
					if (pos_comma < 0)
						throw new IOException("NO COMMA IN Content-Type: " + ctSize[i]);

					ContentItem ci = new ContentItem();
					ci.type = ctSize[i].substring(0, pos_comma);
					ci.storeSize = Integer.parseInt(ctSize[i].substring(pos_comma + 1).trim());

					this.contentItems.add(ci);

					storeSizeFull += ci.storeSize;
				}
			} else {
				throw new IOException("Read Content-Type error." + url);
			}

			if ((type = PageParseUtil.getValueByKeyName(attributes, "Original-Size", ":")) != null) {
				String[] oSize = type.split(";");
				for (int i = 0; i < oSize.length; i++) {
					int pos_comma = oSize[i].indexOf(',');
					if (pos_comma < 0)
						throw new IOException("NO COMMA IN Original-Size: " + oSize[i]);

					ContentItem ci = this.contentItems.get(i);
					if (ci.type.equals(oSize[i].substring(0, pos_comma)) == false)
						throw new IOException("CONFLICING Content-Type and Original-Size");

					ci.originalSize = Integer.parseInt(oSize[i].substring(pos_comma + 1).trim());
				}
			} else {
				throw new IOException("Read Original-Size error." + url);
			}

			byte[] content_full = new byte[storeSizeFull];

			int size = PageParseUtil.readBytes(dis, content_full, storeSizeFull);

			if (size != storeSizeFull) {
				System.err.println("Content-Type and Content cann't match." + url);
				return -8;
			}

			int content_offset = 0;
			for (ContentItem ci : this.contentItems) {
				ci.content = new byte[ci.storeSize];
				System.arraycopy(content_full, content_offset, ci.content, 0, ci.storeSize);
				content_offset += ci.storeSize;
			}
		} catch (Exception ex) {
			if (verbose)
				System.err.println(ex.getMessage());
			return -100;
		}
		return 0;
	}
}
