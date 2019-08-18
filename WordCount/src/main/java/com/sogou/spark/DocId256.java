package com.sogou.spark;

import java.nio.ByteBuffer;
import java.security.DigestException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import com.sogou.spark.DocIdUrlInfo;

public class DocId256 {
	private byte[] id;
	private String strId;
	
	final public static int STRING_DOCID_LENGTH = 66;
	final public static int BYTE_DOCID_LENGTH = 32;
	final public static int STRING_SITEID_LENGTH = 33;
	final public static int BYTE_SITEID_LENGTH = 16;
	final public static int STRING_DOMAINID_LENGTH = 16;
	final public static int BYTE_DOMAINID_LEGNTH = 8;
	final public static int STRING_URLID_LENGTH = 32;
	final public static int BYTE_URLID_LENGTH = 16;

	public DocId256() {
		id = new byte[BYTE_DOCID_LENGTH];
		for( int i = 0; i < BYTE_DOCID_LENGTH; i ++ ) {
			id[i] = 0;
		}
	}
	public DocId256(String docId, int strType) {
		this();
		this.setDocId256(docId);
	}
	public DocId256(String url) {
		this();
		this.setUrl(url);
	}
	
	public void setUrl(String url) {
		if( url == null ) {
			return;
		}
		DocIdUrlInfo info = new DocIdUrlInfo(url);
		try{
			MessageDigest md = MessageDigest.getInstance("MD5");
			byte[] b = new byte[16];
			
			info.getDomainSign(md, b, 0, b.length);
			maskFill( b, 0, id, 0, 64 );
			info.getHostSign(md, b, 0, b.length);
			maskFill( b, 0, id, 64, 64 );
			info.getUrlSign(md, b, 0, b.length);
			maskFill( b, 0, id, 128, 128 );
		} catch( NoSuchAlgorithmException e ){
		} catch( DigestException e){
		}
		strId = bytesToString(id);
	}
	
	public String toString() {
		return getDocId256();
	}
	public boolean equals(Object obj) {
		DocId256 docId2 = (DocId256)obj;
		return this.strId.equals(docId2.strId);
	}
	public int hashCode() {
		return this.strId.hashCode();
	}
	
	public void setDocId256(String docId) {
		if(docId == null || docId.length() != STRING_DOCID_LENGTH) {
			return;
		}
		strId = docId;
		id = stringToBytes(strId);
	}
	public void setDocId256Bytes(byte[] docId) {
		if(docId == null || docId.length != BYTE_DOCID_LENGTH) {
			return;
		}
		id = docId;
		strId = bytesToString(id);
	}
	public String getDocId256() {
		return strId;
	}
	public byte[] getDocId256Bytes() {
		return id;
	}
	public byte[] getDocId256ReverseBytes() {
		byte[] rid = new byte[BYTE_DOCID_LENGTH];
		for( int i = 0; i < BYTE_DOCID_LENGTH; i ++ ) {
			rid[i] = id[BYTE_DOCID_LENGTH-i-1];
		}
		return rid;
	}
	
	public String getHostId() {
		return strId.substring(STRING_DOMAINID_LENGTH+1, STRING_SITEID_LENGTH);
	}
	public void setSiteId(String siteId) {
		if(siteId == null || siteId.length() != STRING_SITEID_LENGTH) {
			return;
		}
		strId = siteId+"-00000000000000000000000000000000";
		id = stringToBytes(strId);
	}
	public String getSiteId() {
		return strId.substring(0, STRING_SITEID_LENGTH);
	}
	public byte[] getSiteIdBytes() {
		byte[] siteId = new byte[BYTE_SITEID_LENGTH];
		System.arraycopy(id, 0, siteId, 0, BYTE_SITEID_LENGTH);
		return siteId;
	}
	
	public String getDomainId() {
		return strId.substring(0, STRING_DOMAINID_LENGTH);
	}
	public byte[] getDomainIdBytes() {
		byte[] domainId = new byte[BYTE_DOMAINID_LEGNTH];
		System.arraycopy(id, 0, domainId, 0, BYTE_DOMAINID_LEGNTH);
		return domainId;
	}
	
	public void setUrlId(String urlId) {
		if(urlId == null || urlId.length() != STRING_URLID_LENGTH) {
			return;
		}
		strId = "0000000000000000-0000000000000000-"+urlId;
		id = stringToBytes(strId);
	}
	public String getUrlId() {
		return strId.substring(STRING_DOCID_LENGTH-STRING_URLID_LENGTH, STRING_DOCID_LENGTH);
	}
	public void setUrlIdBytes(byte[] urlId) {
		if(urlId == null || urlId.length != BYTE_URLID_LENGTH) {
			return;
		}
		System.arraycopy(urlId, 0, id, BYTE_DOCID_LENGTH-BYTE_URLID_LENGTH, BYTE_URLID_LENGTH);
		strId = bytesToString(id);
	}
	public byte[] getUrlIdBytes() {
		byte[] urlId = new byte[BYTE_URLID_LENGTH];
		System.arraycopy(id, BYTE_DOCID_LENGTH-BYTE_URLID_LENGTH, urlId, 0, BYTE_URLID_LENGTH);
		return urlId;
	}
	public void setReverseUrId(String reverseUrlId) {
		if(reverseUrlId == null || reverseUrlId.length() != STRING_URLID_LENGTH) {
			return;
		}
		String urlId = "";
		for( int i = (STRING_URLID_LENGTH/2)-1; i >= 0 ; i -- ){
			urlId += reverseUrlId.substring(i*2,i*2+2);
		}
		strId = "0000000000000000-0000000000000000-"+urlId;
		id = stringToBytes(strId);
	}
	public String getReverseUrlId() {
		String urlId = getUrlId();
		String reverseUrlId = "";
		for( int i = (STRING_URLID_LENGTH/2)-1; i >= 0 ; i -- ){
			reverseUrlId += urlId.substring(i*2,i*2+2);
		}
		return reverseUrlId;
	}

	public long getDocId256Rank(){
		return Long.parseLong(strId.substring(50,56),16);
	}
	public long getSiteIdRank(){
		return Long.parseLong(strId.substring(23,29),16);
	}
	
	public int getCircleNumberByDocId256(int totalCircle) {
		byte res[] = new byte[8];
		for( int i = 0; i < 5; i ++ ) {
			res[7-i] = id[i+16];
		}
		for( int i = 5; i < 8; i ++ ) {
			res[7-i] = 0;
		}
		ByteBuffer bb = ByteBuffer.wrap(res);
		long value = bb.getLong();
		return (int)((((value >> 8) & 0xffffffff) * totalCircle) >> 32);
	}
	
	public int getCircleNumberBySiteId(int totalCircle) {
		byte res[] = new byte[8];
		for( int i = 0; i < 4; i ++ ) {
			res[i+4] = id[i+8];
		}
		for( int i = 0; i < 4; i ++ ) {
			res[i] = 0;
		}
		ByteBuffer bb = ByteBuffer.wrap(res);
		long value = bb.getLong();
		return (int)((((value) & 0xffffffff) * totalCircle) >> 32);
	}

	public void setScatterDocId256BySiteId(String scatterDocId256) {
		setDocId256(scatterDocId256);
	}
	public String getScatterDocId256BySiteId(int scatterLevel) {
		return getDocId256();
	}
	public String[] getScatterDocId256ListBySiteId(int scatterLevel) {
		if(scatterLevel <= 0) {
			String[] docIds = new String[1];
			docIds[0] = getSiteId()+"-"+String.format("%032x", 0);
			return docIds;
		}
		if(scatterLevel > 8) {
			scatterLevel = 8;
		}
		int totalSize = 1;
		for( int i = 0; i < scatterLevel; i ++ ) {
			totalSize *= 2;
		}
		String[] scatterDocId256List = new String[totalSize];
		//int leftHalfByte = STRING_URLID_LENGTH-scatterLevel;
		String formatter = getSiteId()+"-%04x%028x";
//		System.err.println("formatter:"+formatter);
		for( int i = 0; i < totalSize; i ++ ) {
			int k = i;
			k = (k << (16-scatterLevel));
			scatterDocId256List[i] = String.format(formatter, k, 0);
//			System.err.println("i:"+i+"\tk:"+k);
//			System.err.println("doclist:"+scatterDocId256List[i]);
		}
		return scatterDocId256List;
	}
	public int getCircleNumberByScatterDocId256BySiteId(int totalCircle, int scatterLevel) {
		if(scatterLevel <= 0) {
			return getCircleNumberBySiteId(totalCircle);
		}
		if(scatterLevel > 8) {
			scatterLevel = 8;
		}
		int k = 0;
		int hBit = Integer.parseInt(getUrlId().substring(0,4), 16);
		int lBit = Integer.parseInt(getHostId().substring(0,4), 16);
		int hBit2 = ((hBit >> (16-scatterLevel)) << (16-scatterLevel));
		int lBit2 = (((lBit << scatterLevel) & 0x0000ffff) >> scatterLevel);
		//System.out.println(String.format("%04x", hBit2));
		//System.out.println(String.format("%04x", lBit2));
		k = (hBit2 | lBit2);
		DocId256 newDocId256 = new DocId256();
		newDocId256.setSiteId(this.getDomainId()+"-"
				+String.format("%04x", k)+this.getHostId().substring(4));
		//System.out.println(newDocId256.getDocId256());
		return newDocId256.getCircleNumberBySiteId(totalCircle);
	}
	
	private void maskFill( byte[]src, int src_start, byte[] dst, int dst_start, int bit_len){
		for( int i = 0; i < bit_len ; i ++ ){
			updateBit( src, src_start + i, dst, dst_start + i);
		}
	}
	private void updateBit( byte[] src, int src_start, byte[] dst, int dst_start){
		int src_i = (src_start & 0x07);
		int dst_i = (dst_start & 0x07);
		
		int src_index = (src_start >> 3);
		int dst_index = (dst_start >> 3);
		
		int bit = ( (int)src[ src_index ] >> src_i ) & 0x01;
		if( bit == 0 ){
			byte mask = nega_mask[ dst_i ];
			dst[ dst_index ] &= mask;
		} else {
			byte mask = posi_mask[ dst_i ];
			dst[ dst_index ] |= mask;
		}
	}
	private String bytesToString(byte[] key){
		if( key == null || key.length != BYTE_DOCID_LENGTH ) {
			return null;
		}
		char[] buf = new char[key.length*2+2];
		for (int i = 0; i < 8; ++i) {	//DomainSign
			int v = (key[i] > -1) ? key[i] : (key[i] + 0x100);
			buf[2*i] = hexchars[v/0x10];
			buf[2*i+1] = hexchars[v%0x10];
		}
		buf[16] = '-';
		for (int i = 8; i < 16; ++i) {	//HostSign
			int v = (key[i] > -1) ? key[i] : (key[i] + 0x100);			
			buf[1+2*i] = hexchars[v/0x10];
			buf[1+2*i+1] = hexchars[v%0x10];
		}
		buf[33] = '-';
		for (int i = 16; i < 32; ++i) {	//UrlSign
			int v = (key[i] > -1) ? key[i] : (key[i] + 0x100);			
			buf[2+2*i] = hexchars[v/0x10];
			buf[2+2*i+1] = hexchars[v%0x10];
		}
		return new String(buf);
	}
	private byte[] stringToBytes(String key) {
		if( key == null || key.length() != STRING_DOCID_LENGTH ) {
			return null;
		}
		ByteBuffer bb = ByteBuffer.allocate(32);
		int i = 0;
		while(i<key.length()-1){
			if( key.charAt(i) == '-' ){
				i++;
			} else {
				try{
					int a = Integer.parseInt(key.substring(i, i+2), 16);
						bb.put((byte)a);
					i+= 2;
				}catch(Exception e){
					break;
				}
			}
		}
		if( i != key.length() || bb.position() == 0){
			return null;
		} else {
			return bb.array();
		}
	}
	
	private byte[] nega_mask = {(byte)0xFE,(byte)0xFD,(byte)0xFB,(byte)0xF7,
			(byte)0xEF,(byte)0xDF,(byte)0xBF,(byte)0x7F,};
	private byte[] posi_mask = {(byte)0x01,(byte)0x02,(byte)0x04,(byte)0x08,
			(byte)0x10,(byte)0x20,(byte)0x40,(byte)0x80,};
	private char[] hexchars = { '0', '1', '2', '3', '4', '5', '6', '7', 
			'8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };
			
	public static String url2docId( String url ){
		DocId256 docId = new DocId256(url);
		return docId.getDocId256();
	}
	
	public static void main(String[] args) {
		String siteId = "6eca4c3d7807437c-32b6c57be8eb82d3";
		siteId = "http://www.baidu.com/";
		DocId256 docId = new DocId256(siteId);
		String[] scatterDocId256ListBySiteId = docId
				.getScatterDocId256ListBySiteId(5);
		for (int i = 0; i < scatterDocId256ListBySiteId.length; i++) {
			System.out.println("0=="+scatterDocId256ListBySiteId[i]);
		}
	}
}

