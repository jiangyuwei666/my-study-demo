package com.sogou.spark;

import java.io.ByteArrayInputStream;
import java.io.DataInput;
import java.io.DataInputStream;
import java.io.DataOutput;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.WritableUtils;

public class SpiderPageWritable implements Writable {
    public static Pattern PAT_LINE = Pattern.compile("\r?\n");
    public static Text lineSep = new Text("\r\n");

    public static enum PageType {
        UNDEFINED, NORMAL, DELETED, CANCELED,
    }

    public static class Attribute implements Writable {

        public static Text SEP_TEXT = new Text(": ");
        public static String SEP_STRING = new String(": ");

        public Text key = new Text();
        public Text val = new Text();
        public boolean hasSep = false;

        @Override
        public void write(DataOutput out) throws IOException {
            out.writeBoolean(hasSep);
            key.write(out);
            val.write(out);
        }

        @Override
        public void readFields(DataInput in) throws IOException {
            hasSep = in.readBoolean();
            key.readFields(in);
            val.readFields(in);
        }

        public void set(Attribute attr) {
            this.hasSep = attr.hasSep;
            key.set(attr.key);
            val.set(attr.val);
        }

    }

    public Text url = new Text();
    public PageType type = PageType.UNDEFINED;

    public boolean isBodyCompressed = false;

    public ArrayList<Attribute> attributes = new ArrayList<Attribute>();
    public int attributesCount = 0;

    public ArrayList<Attribute> headers = new ArrayList<Attribute>();
    public int headersCount = 0;

    public ArrayList<Text> redirects = new ArrayList<Text>();
    public int redirectsCount = 0;

    public BytesWritable body = new BytesWritable();

    public List<Text> getRedirects() {
        return redirects;
    }

    public SpiderPageWritable() {
    }

    public SpiderPageWritable(SpiderPage opage) {
        setSpiderPage(opage);
    }

    public void setSpiderPage(SpiderPage opage) {
        this.url.set(opage.url);
        String[] fetchInfoLines = PAT_LINE.split(opage.fetching_info);
        for (String fetchInfoLine : fetchInfoLines) {
            //TODO
        }
    }

    public SpiderPageWritable(Text url, boolean isBodyompressed, List<Attribute> attributes, int attributesCount, List<Attribute> headers,
                              int headersCount, List<Text> redirects, int redirectsCount, BytesWritable body) {
        this.url.set(url);
        this.isBodyCompressed = isBodyompressed;

        this.attributesCount = attributesCount;
        this.attributes.ensureCapacity(attributesCount);
        while (this.attributes.size() < this.attributesCount)
            this.attributes.add(new Attribute());

        int idx = 0;
        for (Attribute attr : attributes) {
            this.attributes.get(idx).set(attr);
            idx++;
            if (idx == attributesCount)
                break;
        }

        this.headersCount = headersCount;
        this.headers.ensureCapacity(headersCount);
        while (this.headers.size() < this.headersCount)
            this.headers.add(new Attribute());
        idx = 0;
        for (Attribute attr : headers) {
            this.headers.get(idx).set(attr);
            idx++;
            if (idx == headersCount)
                break;
        }

        this.redirectsCount = redirectsCount;
        this.redirects.ensureCapacity(redirectsCount);
        while (this.redirects.size() < this.redirectsCount)
            this.redirects.add(new Text());
        idx = 0;
        for (Text redr : redirects) {
            this.redirects.get(idx).set(redr);
            idx++;
            if (idx == redirectsCount)
                break;
        }

        this.body.set(body.getBytes(), 0, body.getLength());
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        url.readFields(in);
        isBodyCompressed = in.readBoolean();

        this.attributesCount = WritableUtils.readVInt(in);
        this.attributes.ensureCapacity(attributesCount);
        while (attributes.size() < attributesCount)
            attributes.add(new Attribute());
        for (int i = 0; i < attributesCount; i++)
            attributes.get(i).readFields(in);

        this.headersCount = WritableUtils.readVInt(in);
        this.headers.ensureCapacity(headersCount);
        while (headers.size() < headersCount)
            this.headers.add(new Attribute());
        for (int i = 0; i < headersCount; i++)
            attributes.get(i).readFields(in);

        this.redirectsCount = WritableUtils.readVInt(in);
        this.redirects.ensureCapacity(redirectsCount);
        while (redirects.size() < redirectsCount)
            redirects.add(new Text());
        for (int i = 0; i < redirectsCount; i++)
            redirects.get(i).readFields(in);

        type = PageType.values()[WritableUtils.readVInt(in)];

        body.readFields(in);
    }

    @Override
    public void write(DataOutput out) throws IOException {
        url.write(out);
        out.writeBoolean(isBodyCompressed);

        WritableUtils.writeVInt(out, attributesCount);
        for (int i = 0; i < attributesCount; i++)
            attributes.get(i).write(out);

        WritableUtils.writeVInt(out, headersCount);
        for (int i = 0; i < headersCount; i++)
            headers.get(i).write(out);

        WritableUtils.writeVInt(out, redirectsCount);
        for (int i = 0; i < redirectsCount; i++)
            redirects.get(i).write(out);

        WritableUtils.writeVInt(out, type.ordinal());

        body.write(out);
    }

    public void writeSpiderPage(DataOutput out) throws IOException {
        out.write(url.getBytes(), 0, url.getLength());
        out.write(lineSep.getBytes(), 0, lineSep.getLength());

        for (int i = 0; i < attributesCount; i++) {
            Attribute attr = attributes.get(i);
            out.write(attr.key.getBytes(), 0, attr.key.getLength());
            if (attr.hasSep) {
                out.write(Attribute.SEP_TEXT.getBytes(), 0, Attribute.SEP_TEXT.getLength());
                out.write(attr.val.getBytes(), 0, attr.val.getLength());
            }
            out.write(lineSep.getBytes(), 0, lineSep.getLength());
        }
        out.write(lineSep.getBytes(), 0, lineSep.getLength());

        for (int i = 0; i < headersCount; i++) {
            Attribute attr = headers.get(i);
            out.write(attr.key.getBytes(), 0, attr.key.getLength());
            if (attr.hasSep) {
                out.write(Attribute.SEP_TEXT.getBytes(), 0, Attribute.SEP_TEXT.getLength());
                out.write(attr.val.getBytes(), 0, attr.val.getLength());
            }
            out.write(lineSep.getBytes(), 0, lineSep.getLength());
        }
        out.write(lineSep.getBytes(), 0, lineSep.getLength());

        if (this.body.getLength() > 0) {
            out.write(this.body.getBytes(), 0, this.body.getLength());
            out.write(lineSep.getBytes(), 0, lineSep.getLength());
        }
    }

    public Attribute getAttribute(String key) {
        for (int i = 0; i < attributesCount; i++) {
            Attribute attr = attributes.get(i);
            if (attr.key.toString().equals(key))
                return attr;
        }

        return null;
    }

    public int buildFromBytes(byte[] bytes, boolean verbose) {
        url.clear();
        type = PageType.UNDEFINED;
        isBodyCompressed = false;
        attributesCount = 0;
        headersCount = 0;
        redirectsCount = 0;
        body.setSize(0);

        try {
            ByteArrayInputStream dais = new ByteArrayInputStream(bytes);
            DataInputStream dis = new DataInputStream(dais);

            String line = null;
            while (dis.available() > 0) {
                line = PageParseUtil.readLine(dis);
                if (line.startsWith("http"))
                    break;
            }

            if (line == null || line.startsWith("http") == false)
                return -1;

            url.set(line);

            boolean metEmptyLine = false;
            while (dis.available() > 0) {
                line = PageParseUtil.readLine(dis);
                if (line.length() == 0) {
                    metEmptyLine = true;
                    break;
                }
                int attrIdx = attributesCount;
                if (attrIdx == attributes.size())
                    attributes.add(new Attribute());
                attributesCount++;

                Attribute attr = attributes.get(attrIdx);
                int sepIdx = line.indexOf(Attribute.SEP_STRING);
                if (sepIdx != -1) {
                    attr.key.set(line.substring(0, sepIdx));
                    attr.val.set(line.substring(sepIdx + Attribute.SEP_STRING.length()));
                    attr.hasSep = true;
                } else {
                    attr.key.set(line);
                    attr.val.clear();
                    attr.hasSep = false;
                }
            }

            if (!metEmptyLine) {
                if (dis.available() == 0)
                    return -2;
                else
                    throw new IOException("Premature EOF when reading attributes");
            }

			/*if (!checkPageAttributesMeta(attributes)) {
				return false;
			}*/

            //String type = null;
            //type = PageParseUtil.getValueByKeyName(attributes, "Type", ":");

            Attribute typeAttr = getAttribute("Type");
            if (typeAttr == null)
                throw new IOException("NO Type Attribute");

            boolean is_compressed = false;
            boolean is_deleted = false;
            boolean is_canceled = false;
            if (typeAttr.val.find("compressed") == 0) {
                is_compressed = true;
            } else if (typeAttr.val.find("normal") == 0) {
                is_compressed = false;
            } else if (typeAttr.val.find("deleted") == 0) {
                is_deleted = true;
            } else if (typeAttr.val.find("canceled") == 0) {
                is_canceled = true;
            } else {
                throw new IOException("UNKNOWN Type val: " + typeAttr.val);
            }

            if (is_deleted) {
                //page of type deleted has no header nor body
                type = PageType.DELETED;
                return 0;
            }

            metEmptyLine = false;
            while (dis.available() != 0) {
                line = PageParseUtil.readLine(dis);
                if (line.length() == 0) {
                    metEmptyLine = true;
                    break;
                }
                int headerIdx = headersCount;
                if (headerIdx == headers.size())
                    headers.add(new Attribute());
                headersCount++;

                Attribute attr = headers.get(headerIdx);
                int sepIdx = line.indexOf(Attribute.SEP_STRING);
                if (sepIdx != -1) {
                    attr.key.set(line.substring(0, sepIdx));
                    attr.val.set(line.substring(sepIdx + Attribute.SEP_STRING.length()));
                    attr.hasSep = true;
                } else {
                    attr.key.set(line);
                    attr.val.clear();
                    attr.hasSep = false;
                }
            }

            if (!metEmptyLine) {
                if (dis.available() == 0)
                    return -3;
                else
                    throw new IOException("Premature EOF when reading headers");
            }

            if (is_canceled) {
                //page of type canceled has no body
                type = PageType.CANCELED;
                return 0;
            }

            Attribute storeSizeAttr = getAttribute("Store-Size");
            if (storeSizeAttr == null)
                throw new IOException("NO Type Store-Size");

            int storeSize = Integer.parseInt(storeSizeAttr.val.toString());

            //content = new byte[store_size];
            this.body.setSize(storeSize);

            int size = PageParseUtil.readBytes(dis, body.getBytes(), storeSize);

            if (size != storeSize) {
                if (dis.available() == 0)
                    return -4;
                else
                    throw new IOException("Failed to read content of Store-Size");
            }

            type = PageType.NORMAL;
            isBodyCompressed = is_compressed;
        } catch (Exception ex) {
            if (verbose)
                System.err.println(ex.getMessage());
            return -100;
        }

        return 0;
    }
}
