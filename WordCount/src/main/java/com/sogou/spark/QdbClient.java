package com.sogou.spark;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class QdbClient {

	private static final Log LOG = LogFactory.getLog(QdbClient.class.getName());
	byte QDB_NET_GET_CMD = 1;
	byte QDB_NET_PUT_CMD = 2;
	byte QDB_NET_DEL_CMD = 3;
	byte QDB_NET_SYNC_CMD = 4;
	byte QDB_NET_CURSOR_OPEN_CMD = 7;
	byte QDB_NET_CURSOR_GET_CMD = 8;
	byte QDB_NET_CURSOR_CLOSE_CMD = 9;
	byte QDB_NET_CURSOR_SEEK_CMD = 10;
	byte QDB_NET_GET_STATE_CMD = 11;
	byte QDB_NET_TEST_CMD = 12;

	static public class QdbData {
		public byte[] key;
		public byte[] data;
	}

	static public class QdbState {
		public int entry_total;
		public int entry_free;
		public int entry_used;
		public int entry_deleted;
		public int unit_size;
		public int unit_total;
		public int unit_free;
		public int unit_used;
		public int unit_wasted;
		public int record_count;
		public int chunk_total;
		public int chunk_empty;
		public int chunk_allocated;
	}

	long cursorOffset = 0;
	private int timeout = 5000;
	int sleepTime = 1000;
	private SocketChannel channel = null;
	private SocketChannel cursor_channel = null;
	private String host = null;
	private int port = 0;

	Selector selector = null;

	private byte[] uint2byte(long res) {
		byte[] targets = new byte[4];

		targets[3] = (byte) (res & 0xff);// 最低位
		targets[2] = (byte) ((res >> 8) & 0xff);// 次低位
		targets[1] = (byte) ((res >> 16) & 0xff);// 次高位
		targets[0] = (byte) ((res >> 24) & 0xff);// 最高位,无符号右移。
		return targets;
	}

	public QdbClient(String h, int p) {
		host = h;
		port = p;
	}

	public int open() {
		try {

			channel = SocketChannel.open();
			channel.configureBlocking(false);
			InetSocketAddress addr = new InetSocketAddress(host, port);
			channel.connect(addr);
			// Thread.sleep(5);
			Thread.sleep(sleepTime);
			boolean ret = channel.finishConnect();
			int retryNum = 2;

			while (retryNum > 0) {
				if (ret) {
					LOG.info("open success");
					return 0;
				}
				Thread.sleep(sleepTime);
				ret = channel.finishConnect();
				retryNum--;
			}
			LOG.error("open failed");
			return -1;

		} catch (Exception e) {
			try {
				channel.close();
			} catch (Exception e1) {
				e1.printStackTrace();
			}
			e.printStackTrace();
			return -1;
		}
	}

	public int qdbCursorOpen(int flags) {
		try {
			cursor_channel = SocketChannel.open();
			cursor_channel.configureBlocking(false);
			InetSocketAddress addr = new InetSocketAddress(host, port);
			cursor_channel.connect(addr);
			try {
				Thread.sleep(sleepTime);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			boolean cret = cursor_channel.finishConnect();
			if (cret) {
				byte cmd = QDB_NET_CURSOR_OPEN_CMD;
				ByteBuffer outbuffer = ByteBuffer.allocate(1024);
				outbuffer.put(cmd);
				outbuffer.putInt(flags);
				outbuffer.flip();
				int ret = -1;
				cursorOffset = 0;
				if (cursor_channel.write(outbuffer) > 0) {
					ret = extract_int(cursor_channel, getTimeout());
					{
						if (ret < 0) {
							int error_no = extract_int(cursor_channel, getTimeout());
							throw new IOException("remote:" + Integer.toString(error_no));
						}
					}
				}
				LOG.info("qdbCursorOpen success");
				return 0;
			} else {
				LOG.error("qdbCursorOpen failed");
				return -1;
			}
			// selector = Selector.open();

		} catch (IOException e) {
			e.printStackTrace();
			return -1;
		}
	}

	int qdbCursorGet(QdbData data, int flags) {
		byte cmd = QDB_NET_CURSOR_GET_CMD;
		ByteBuffer outbuffer = ByteBuffer.allocate(1024);
		outbuffer.put(cmd);
		outbuffer.putInt(flags);
		outbuffer.flip();
		int ret = -1;
		//cursorOffset = 0;
		try {
			if (cursor_channel.write(outbuffer) > 0) {
				ret = extract_int(cursor_channel, getTimeout());

				if (ret == 0) {
					extract_dbt_key(cursor_channel, data);
					extract_dbt_data(cursor_channel, data);
					cursorOffset = extract_uint(cursor_channel, getTimeout());
					LOG.debug("next succ");
				}
				if (ret < 0) {
					int x = extract_int(cursor_channel, getTimeout());
					LOG.debug("next fail " + ret + " " + x);
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return ret;
	}

	private long read_timeout(SocketChannel ch, ByteBuffer buffer, int timeout) throws IOException {
		selector = Selector.open();
		ch.register(selector, SelectionKey.OP_READ);
		int num = selector.select(timeout);

		// caused by timeout
		if (num == 0) {
			throw new IOException("Timeout");
		}

		long n = 0;
		Set<SelectionKey> set = selector.selectedKeys();
		Iterator<SelectionKey> it = set.iterator();
		while (it.hasNext()) {
			it.next();
			int read = ch.read(buffer);
			if( read < 0 )
				throw new IOException("Channel reached EOF prematurely");
			n += read;
		}
		selector.close();
		return n;
	}

	private long readn_timeout(SocketChannel ch, ByteBuffer buffer, long len, int timeout) throws IOException {
		long nleft = len;
		long nbytes;

		while (nleft > 0) {
			if ((nbytes = read_timeout(ch, buffer, timeout)) > 0) {
				nleft -= nbytes;
			} else if (nbytes == 0)
				return len - nleft;
			else
				return -1;
		}

		return len;
	}

	int extract_int(SocketChannel ch, int timeout) throws IOException {
		try {
			ByteBuffer result = ByteBuffer.allocate(4);
			readn_timeout(ch, result, 4, timeout);
			result.flip();
			return result.getInt();
		} catch (Exception e) {
			e.printStackTrace();
			throw new IOException("extract_int Exception");
		}
	}

	public static long byteToLong(byte[] b) {
		long s = 0;
		long s0 = b[0] & 0xff;// 最低位
		long s1 = b[1] & 0xff;
		long s2 = b[2] & 0xff;
		long s3 = b[3] & 0xff;

		// s0����
		s0 <<= 24;
		s1 <<= 16;
		s2 <<= 8;
		s = s0 + s1 + s2 + s3;
		return s;
	}

	long extract_uint(SocketChannel ch, int timeout) throws IOException {
		try {
			ByteBuffer result = ByteBuffer.allocate(4);
			readn_timeout(ch, result, 4, timeout);
			result.flip();
			/*
			 * byte tmp[] =result.array(); for (int i=0;i<tmp.length;i++)
			 * System.out.println("tmp="+(tmp[i] & 0xFF));
			 */
			return byteToLong(result.array());
		} catch (Exception e) {
			throw new IOException("extract_int Exception");
		}
	}

	int extract_dbt_key(SocketChannel ch, QdbData data) throws IOException {

		try {
			int size = extract_int(ch, getTimeout());
			{
				ByteBuffer buffer = ByteBuffer.allocate(size);
				readn_timeout(ch, buffer, size, getTimeout());
				data.key = buffer.array();
				return 0;
			}
		} catch (IOException e) {
			throw e;
		}
	}

	int extract_dbt_data(SocketChannel ch, QdbData data) throws IOException {
		int size = extract_int(ch, getTimeout());
		ByteBuffer buffer = ByteBuffer.allocate(size);
		readn_timeout(ch, buffer, size, getTimeout());
		data.data = buffer.array();
		return 0;
	}

	int extract_dbt_state(SocketChannel ch, QdbState state) throws IOException {
		try {
			int size = extract_int(ch, getTimeout());
			// System.out.println("extract_dbt_data,size="+size);
			{
				ByteBuffer buffer = ByteBuffer.allocate(size);
				readn_timeout(ch, buffer, size, getTimeout());
				buffer.flip();
				// data.data = buffer.array();
				/*
				 * byte tmp[] = buffer.array(); for (int i = 0;i<tmp.length;i++)
				 * { System.out.println("tmp="+tmp[i]); }
				 */

				state.entry_total = buffer.getInt();
				state.entry_free = buffer.getInt();
				state.entry_used = buffer.getInt();
				state.entry_deleted = buffer.getInt();
				state.unit_size = buffer.getInt();
				state.unit_total = buffer.getInt();
				state.unit_free = buffer.getInt();
				state.unit_used = buffer.getInt();
				state.unit_wasted = buffer.getInt();
				state.record_count = buffer.getInt();
				state.chunk_total = buffer.getInt();
				state.chunk_empty = buffer.getInt();
				state.chunk_allocated = buffer.getInt();
				return 0;
			}
		} catch (IOException e) {
			throw e;
		}
	}

	public int get(QdbData data, int flags) throws IOException {
		byte cmd = QDB_NET_GET_CMD;
		int key_len = data.key.length;
		ByteBuffer outbuffer = ByteBuffer.allocate(key_len + 100);
		outbuffer.put(cmd);
		outbuffer.putInt(key_len);
		outbuffer.put(data.key);
		outbuffer.putInt(flags);
		outbuffer.flip();
		int ret = -1;
		try {
			if (channel.write(outbuffer) > 0) {
				ret = extract_int(channel, getTimeout());
				if (ret == 0) {
					extract_dbt_data(channel, data);
				} else if (ret < 0) {
					int error = extract_int(channel, getTimeout());
					ret = -1;
					throw new IOException("remote:" + Integer.toString(error));
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return ret;
	}

	public int del(QdbData data, int flags) throws IOException {
		byte cmd = QDB_NET_DEL_CMD;
		int key_len = data.key.length;
		ByteBuffer outbuffer = ByteBuffer.allocate(key_len + 100);
		outbuffer.put(cmd);
		outbuffer.putInt(key_len);
		outbuffer.put(data.key);
		outbuffer.putInt(flags);
		outbuffer.flip();
		int ret = -1;
		try {
			if (channel.write(outbuffer) > 0) {
				ret = extract_int(channel, getTimeout());
				if (ret == 0) {
					//succeed
				} else if (ret < 0) {
					int error = extract_int(channel, getTimeout());
					ret = -1;
					throw new IOException("remote:" + Integer.toString(error));
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return ret;
	}

	public int put(QdbData data, short digest, int flags) throws IOException {

		byte cmd = QDB_NET_PUT_CMD;
		int key_len = data.key.length;
		int data_len = data.data.length;
		ByteBuffer outbuffer = ByteBuffer.allocate(key_len + data_len + 100);
		outbuffer.put(cmd);
		outbuffer.putInt(key_len);
		outbuffer.put(data.key);
		outbuffer.putInt(data_len);
		outbuffer.put(data.data);
		outbuffer.putShort(digest);
		outbuffer.putInt(flags);
		outbuffer.flip();
		int ret = -1;
		// channel.register(selector, SelectionKey.OP_READ);
		if (channel.write(outbuffer) > 0) {
			try {
				ret = extract_int(channel, getTimeout());
				{
					if (ret < 0) {
						int error_no = extract_int(channel, getTimeout());
						throw new IOException("remote:" + Integer.toString(error_no));
					}
				}
			} catch (IOException e) {
				e.printStackTrace();
			}

		}
		return ret;

	}

	int cursor_get(QdbData data, int flags) {
		return flags;

	}

	public int seek(int flags, long offset) {
		byte cmd = QDB_NET_CURSOR_SEEK_CMD;
		int ret = 0;
		ByteBuffer outbuffer = ByteBuffer.allocate(1024);
		outbuffer.put(cmd);
		outbuffer.put(uint2byte(offset));
		outbuffer.putInt(flags);
		outbuffer.flip();
		try {
			if (cursor_channel.write(outbuffer) > 0) {
				ret = extract_int(cursor_channel, getTimeout());
				{
					if (ret < 0) {
						int error_no = extract_int(cursor_channel, getTimeout());
						throw new IOException("remote:" + Integer.toString(error_no));
					}
				}
				this.cursorOffset = offset;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return ret;
	}

	int qdbCursorClose(int flags) {
		byte cmd = QDB_NET_CURSOR_CLOSE_CMD;
		ByteBuffer outbuffer = ByteBuffer.allocate(1024);
		outbuffer.put(cmd);
		outbuffer.putInt(flags);
		outbuffer.flip();
		try {
			cursor_channel.write(outbuffer);
			cursor_channel.close();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return 0;
	}

	public int next(QdbData data) {
		long preCursorOffset = this.cursorOffset;
		int ret = qdbCursorGet(data, 0);
		while (ret < 0) {
			LOG.error("next error ret=" + ret + " cursorOffset=" + cursorOffset);
			qdbCursorClose(0);
			ret = qdbCursorOpen(0);
			if (ret == 0) {
				seek(0, ++preCursorOffset);
				ret = qdbCursorGet(data, 0);
			}
		}
		if (ret > 0) {
			return 1;
		}
		return ret;
	}

	public int state(QdbState state) {
		byte cmd = QDB_NET_GET_STATE_CMD;
		int ret = 0;
		ByteBuffer outbuffer = ByteBuffer.allocate(1024);
		outbuffer.put(cmd);
		outbuffer.putInt(3);
		outbuffer.flip();
		try {
			if (channel.write(outbuffer) > 0) {

				ret = extract_int(channel, getTimeout());
				{
					if (ret == 0) {
						ret = extract_dbt_state(channel, state);
						return ret;
					}
					if (ret < 0) {
						int error_no = extract_int(cursor_channel, getTimeout());
						throw new IOException("remote:" + Integer.toString(error_no));
					}
				}

			}
		} catch (IOException e) {
			e.printStackTrace();
			return -1;
		}
		return ret;
	}

	public void close() {
		try {
			if (channel != null)
				channel.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public int getTimeout() {
		return timeout;
	}

	public void setTimeout(int timeout) {
		this.timeout = timeout;
	}

	public long getCursorOffset() {
		return cursorOffset;
	}

}
