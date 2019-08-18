package com.sogou.spark;

import java.io.DataInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class PageParseUtil {

	public static String getValueByKeyName(List<String> attributes, String name, String flag) {

		String value = null;
		String key = null;

		for (int i = 0; i < attributes.size(); i++) {

			String line = attributes.get(i);
			int pos = -1;
			if ((pos = line.indexOf(flag)) != -1) {
				key = line.substring(0, pos).trim();

				if (key.equals(name)) {
					++pos;
					value = line.substring(pos, (line.length())).trim();
					break;
				}
			}
		}

		return value;
	}

	public static long getFileLength(FileSystem fs, Path filePath) {
		long result = 0;
		try {
			FileStatus fStatus = fs.getFileStatus(filePath);
			result = fStatus.getLen();
		} catch (Exception ex) {
			System.err.println("get file length error:" + ex.getMessage());
		}
		return result;
	}

	public static long available(FSDataInputStream dis, long fileLength) {

		long result = 0;

		if (dis != null) {

			try {
				long currentPosition = dis.getPos();

				if (fileLength > currentPosition) {
					result = fileLength - currentPosition;
				}
			} catch (Exception ex) {
				System.err.println("get file available status error:" + ex.getMessage());
			}
		}

		return result;
	}

	public static int readBytesV2(FSDataInputStream dis, byte[] content, int size, long fileLength) {
		int off = 0;
		if (dis == null)
			return -1;
		if (size == 0)
			return 0;
		if (size < 0)
			return -1;
		long avail = PageParseUtil.available(dis, fileLength);
		if (avail < size)
			return -1;

		try {
			while (off < size) {
				int read = dis.read(content, off, size - off);
				if (read < 0)
					throw new IOException("EOF");
				off += read;
			}
		} catch (IOException ex) {
			System.err.println("read file failed:" + ex.getMessage());
			return -1;
		}

		return off;
	}

	public static int readBytes(FSDataInputStream dis, byte[] content, int size, long fileLength) {
		int p = 0;
		try {
			if (dis != null && PageParseUtil.available(dis, fileLength) != 0 && size > 0) {
				while (PageParseUtil.available(dis, fileLength) != 0 && p < size) {
					content[p] = dis.readByte();
					p++;
				}
			}
		} catch (IOException ex) {
			System.err.println("read file failed:" + ex.getMessage());
		}

		return p;
	}

	public static int readBytes(DataInputStream dis, byte[] content, int size) {

		int p = 0;
		try {
			if (dis != null && dis.available() > 0 && size > 0) {

				while (dis.available() > 0 && p < size) {

					content[p] = dis.readByte();
					p++;
				}
			}
		} catch (IOException ex) {
			System.err.println("read file failed:" + ex.getMessage());
		}

		return p;
	}

	public static String readLine(FSDataInputStream dis, long fileLength) throws IOException {
		String result = null;

		if (PageParseUtil.available(dis, fileLength) != 0) {
			List<Byte> line = new ArrayList<Byte>();
			byte b = dis.readByte();
			while (PageParseUtil.available(dis, fileLength) != 0) {
				if (b == '\n') {
					break;
				}
				if (b != '\r') {
					line.add(b);
				}
				b = dis.readByte();
			}

			if (line.size() != 0) {

				final int size = line.size();
				byte[] l = new byte[size];

				for (int i = 0; i < size; i++) {
					l[i] = line.get(i);
				}

				result = new String(l);
			} else {
				result = "";
			}
		}

		return result;
	}

	public static String readLine(DataInputStream dis) throws IOException {
		String result = null;

		List<Byte> line = new ArrayList<Byte>();
		byte b = dis.readByte();
		while (dis.available() > 0) {

			if (b == '\n') {
				break;
			}
			if (b != '\r') {
				line.add(b);
			}
			b = dis.readByte();
		}

		if (line.size() != 0) {

			final int size = line.size();
			byte[] l = new byte[size];

			for (int i = 0; i < size; i++) {
				l[i] = line.get(i);
			}

			result = new String(l);
		} else {
			result = "";
		}

		return result;
	}
}