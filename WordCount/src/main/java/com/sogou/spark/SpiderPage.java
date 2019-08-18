package com.sogou.spark;

public class SpiderPage {
	int		status;
	long	fetchtime;
	long	lastmodified;

	long	siteip;

	String	url;
	String	redirect_url;
	String	cookie;
	String	fetching_info;
	String	http_header;

	int		body_size;
	byte[]	body;

	String	fromLoc;


	public int getStatus() {
		return status;
	}
	public void setStatus(int status) {
		this.status = status;
	}
	public long getFetchtime() {
		return fetchtime;
	}
	public void setFetchtime(long fetchtime) {
		this.fetchtime = fetchtime;
	}
	public long getLastmodified() {
		return lastmodified;
	}
	public void setLastmodified(long lastmodified) {
		this.lastmodified = lastmodified;
	}
	public long getSiteip() {
		return siteip;
	}
	public void setSiteip(long siteip) {
		this.siteip = siteip;
	}
	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	public String getRedirect_url() {
		return redirect_url;
	}
	public void setRedirect_url(String redirect_url) {
		this.redirect_url = redirect_url;
	}
	public String getCookie() {
		return cookie;
	}
	public void setCookie(String cookie) {
		this.cookie = cookie;
	}
	public String getFetching_info() {
		return fetching_info;
	}
	public void setFetching_info(String fetching_info) {
		this.fetching_info = fetching_info;
	}
	public String getHttp_header() {
		return http_header;
	}
	public void setHttp_header(String http_header) {
		this.http_header = http_header;
	}
	public int getBody_size() {
		return body_size;
	}
	public void setBody_size(int body_size) {
		this.body_size = body_size;
	}
	public byte[] getBody() {
		return body;
	}
	public void setBody(byte[] body) {
		this.body = body;
	}
	public String getFromLoc() {
		return fromLoc;
	}
	public void setFromLoc(String fromLoc) {
		this.fromLoc = fromLoc;
	}
	
	
}
