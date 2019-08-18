package com.sogou.spark;

import java.io.ByteArrayInputStream;
import java.io.DataInput;
import java.io.DataInputStream;
import java.io.DataOutput;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.Inflater;

import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.WritableComparable;

public class OffsumPageWritableV2 implements Writable, WritableComparable<OffsumPageWritableV2> {

	public static class ContentItem implements Writable {
		public String type = "";
		public int storeSize = 0;
		public int originalSize = 0;
		public byte[] content = new byte[0];

		@Override
		public void write(DataOutput out) throws IOException {
			out.writeUTF(type);
			out.writeInt(storeSize);
			out.writeInt(originalSize);
			out.writeInt(content.length);
			out.write(content);
		}

		@Override
		public void readFields(DataInput in) throws IOException {
			type = in.readUTF();
			storeSize = in.readInt();
			originalSize = in.readInt();
			content = new byte[in.readInt()];
			in.readFully(content);
		}
	};
	
    @Override
	public int compareTo(OffsumPageWritableV2 o) {
		return url.compareTo(o.url);
	}

	public String url = null;
	public boolean isDeleted = false;
	public List<String> attributes = new ArrayList<String>();
	public List<ContentItem> contentItems = new ArrayList<ContentItem>(4);

	/*private List<String> contenttype = new ArrayList<String>();

	public List<String> getContenttype() {
		return contenttype;
	}

	private List<String> originalsize = new ArrayList<String>();

	public List<byte[]> contents = new ArrayList<byte[]>();

	public List<String> getOriginalsize() {
		return originalsize;
	}*/

	public OffsumPageWritableV2() {
	}

	public OffsumPageWritableV2(String url, boolean is_deleted, List<String> attributes) {
		this.url = url;
		this.isDeleted = is_deleted;
		this.attributes = attributes;
	}

	@Override
	public void readFields(DataInput in) throws IOException {
		url = in.readUTF();
		isDeleted = in.readBoolean();
		int attributes_size = in.readInt();
		attributes.clear();
		for (int i = 0; i < attributes_size; i++) {
			attributes.add(in.readUTF());
		}
		contentItems.clear();
		int content_count = in.readInt();
		while (contentItems.size() < content_count) {
			ContentItem ci = new ContentItem();
			ci.readFields(in);
			contentItems.add(ci);
		}
	}

	@Override
	public void write(DataOutput out) throws IOException {

		out.writeUTF(url);
		out.writeBoolean(isDeleted);
		out.writeInt(attributes.size());
		for (int i = 0; i < attributes.size(); i++) {
			out.writeUTF(attributes.get(i));
		}
		out.writeInt(contentItems.size());
		for (ContentItem ci : contentItems) {
			ci.write(out);
		}
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
				//System.out.println(line);
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
					//contenttype.add(ctSize[i]);

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
    public byte[] getOffsumPageBytes(){
    	String head=url;
    	head+="\n";
    	for(String attr : attributes){
    		head+=attr;
    		head+="\n";
    	}
    	head+="\n";
    	byte []head_byte=head.getBytes();
    	
    	int storeSizeFull = 0;
    	int content_offset=head_byte.length;
    	for(ContentItem ci : contentItems)
    		storeSizeFull+=ci.storeSize;
    	byte []result=new byte[content_offset+storeSizeFull];
    	System.arraycopy(head_byte, 0, result, 0, content_offset);
    	
    	for(ContentItem ci : contentItems){
    		System.arraycopy(ci.content,0, result, content_offset, ci.storeSize);
			content_offset+=ci.storeSize;
		}
    	return result;
    }
}
