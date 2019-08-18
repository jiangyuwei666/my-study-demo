package com.sogou.spark;

import java.security.DigestException;
import java.security.MessageDigest;

public class DocIdUrlInfo{
	byte[] b;
	int host_head = 0;
	int host_tail = 0;
	int domain_head = -1;
	int domain_tail = 0;

	public int getHostHead() {
		return host_head;
	}
	public int getHostTail() {
		return host_tail;
	}
	public int getDomainHead() {
		return domain_head;
	}
	public int getDomainTail() {
		return domain_tail;
	}
	public String getHost() {
		if(host_head < 0 || host_head >= b.length || 
				host_tail < 0 || host_tail >= b.length || host_head >= host_tail ) {
			return new String(b);
		}
		return new String(b, host_head, host_tail-host_head);
	}
	public String getDomain() {
		if(domain_head < 0 || domain_head >= b.length || 
				domain_tail < 0 || domain_tail >= b.length || domain_head >= domain_tail ) {
			return new String(b);
		}
		return new String(b, domain_head, domain_tail-domain_head);
	}
	
	int getDomainSign( MessageDigest md, byte[]out, int start, int len ) throws DigestException{
		md.reset();
		md.update(b, domain_head, domain_tail - domain_head);
		return md.digest( out, start, len );
	}
	int getHostSign( MessageDigest md, byte[]out, int start, int len ) throws DigestException{
		md.reset();
		md.update(b, host_head, host_tail - host_head);
		return md.digest( out, start, len );
	}
	int getUrlSign( MessageDigest md, byte[]out, int start, int len ) throws DigestException{
		md.reset();
		md.update(b);
		return md.digest( out, start, len );
	}

	public DocIdUrlInfo( String url ){
        b = url.getBytes();
		
		int domain_pre_head = domain_head;
		int domain_post_head = domain_head;
		domain_tail = domain_head;
		boolean find_domain = false;
		boolean deal_domain = false;
		int i = 0;
		for( i = 0; i < b.length; i ++ ){
			if( b[i] == '.' ){
				deal_domain = true;
			}
			else if( b[i] == '/' ){
				break;
			}
			else if( b[i] == ':'){
				if( i + 2 < b.length && b[i+1] == '/' && b[i+2] == '/' ){
					i += 2;
					domain_head = i ;
					domain_pre_head = i;
					domain_post_head = i;
					domain_tail = i;
					continue;
				} 
				else if( !find_domain ){
					deal_domain = true;
					find_domain = true;
				}
			}
			if( deal_domain ){
				domain_pre_head = domain_head;
				domain_head = domain_post_head;
				domain_post_head = domain_tail;
				domain_tail = i;
				deal_domain = false;
			}
		}
		host_tail = i;
		
		if( !find_domain ){
			domain_pre_head = domain_head;
			domain_head = domain_post_head;
			domain_post_head = domain_tail;
			domain_tail = i;
		}
	
		if ( in_second_domain_set(b, domain_post_head - domain_head - 1, domain_head + 1) > 0  
				&& in_top_domain_set(b, domain_tail-domain_post_head - 1, domain_post_head+1) == 0 ) {
			domain_head = domain_pre_head;
		}
		domain_head ++;
	}
	
	int in_top_domain_set(byte[] url, int len, int start ){
		final String domain_set_2[] = {
				"ac", "co",
		};
		final String domain_set_3[] = {
				"cat", "edu", "net", "biz", "mil", "int", "com", "gov", "org", "pro",
		};
		final String domain_set_4[] = {
				"name", "aero", "info", "coop", "jobs", "mobi", "arpa",
		};
		final String domain_set_6[] = {
				"travel", "museum",
		};
		final String [][]domain_set = {
				null, null, domain_set_2, domain_set_3, domain_set_4, null, domain_set_6,
		};
		final int domain_set_len[] = {
				0,
				0,
				(domain_set_2.length),
				(domain_set_3).length,
				(domain_set_4).length,
				0,
				(domain_set_6).length,
		};

		switch (len)
		{
		case 2:
		case 3:
		case 4:
		case 6:
			return in_domain_set(url, len, domain_set[len], domain_set_len[len], start);
		default:
			return 0;
		}
	}

	int in_second_domain_set(byte[]url, int len, int start) {
		final String domain_set_2[] = {                       /// domain in china & ac & co
				"ha", "hb", "ac", "sc", "gd", "sd", "he", "ah", "qh",
				"sh", "hi", "bj", "fj", "tj", "xj", "zj", "hk", "hl",
				"jl", "nm", "hn", "ln", "sn", "yn", "co", "mo", "cq",
				"gs", "js", "tw", "gx", "jx", "nx", "sx", "gz", "xz",
		};
		final String domain_set_3[] = {
				"cat", "edu", "net", "biz", "mil", "int", "com", "gov", "org", "pro",
		};
		final String domain_set_4[] = {
				"name", "aero", "info", "coop", "jobs", "mobi", "arpa",
		};
		final String domain_set_6[] = {
				"travel", "museum",
		};
		final String[] domain_set[] = {
				null, null, domain_set_2, domain_set_3, domain_set_4, null, domain_set_6,
		};
		final int domain_set_len[] = {
				0,
				0,
				(domain_set_2).length,
				(domain_set_3).length,
				(domain_set_4).length,
				0,
				(domain_set_6).length,
		};
	
		switch (len)
		{
		case 2:
		case 3:
		case 4:
		case 6:
			return in_domain_set(url, len, domain_set[len], domain_set_len[len], start);
		default:
			return 0;
		}
	}

	int in_domain_set(byte[]url, int len, String[]domain_set, int domain_set_len, int start) {
		int begin = 0;
		int end = domain_set_len - 1;
		int mid = -1;
		int ret;
		int i = 2;

		while (begin <= end) {
			mid = (begin + end) / 2;
			ret = url[start+1] - (domain_set[mid].charAt( 1 ) );
			if (ret > 0) {
				begin = mid + 1;
			}
			else if (ret < 0) {
				end = mid - 1;
			}
			else {
				ret = url[start] - domain_set[mid].charAt(0);
				if( ret > 0 ) {
					begin = mid + 1;
				}
				else if( ret < 0 ) {
					end = mid - 1;
				}
				else {
					break;
				}
			}
		}

		if (begin > end) {
			return 0;
		}

		while (i<len && url[start+i]==domain_set[mid].charAt(i) ) {
			i++;
		}
		return i==len?1:0;
	}
}

