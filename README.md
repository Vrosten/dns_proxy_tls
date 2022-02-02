# dns_proxy_tls
A simple proxy to enable to query DNS over TLS


Requirements of the proxy

Parts of classes

Socket AF_UNIX



Structure
 - A class that can read the public key published in the keychain 
 - DNS service bind on TCP/UDP 53
    - Need to check the query is well formated. Maybe parse the string sent by the client

- DNS-over-TLS send query and receive the response
    - Get the information from the above class and perform the query and format the response


- A logger to log all the messages into a log file
- A main caller to manage initialization of the objects
- Each thread on proxy service should initiate a new client object to query the domain, log the query 





- The health check should be a different process initiated outside of the pool, or even outside of the main call.
- A health check daemon to check if the proxy service is running, if not, try to execute it three times after declares the service is not able to initiate



List of DNS over TLS providers

censurfridns.dk 	91.239.100.100 	anycast.uncensoreddns.org
	2002:d596:2a92:1:71:53:: 	
Cloudflare 	1.1.1.1 	cloudflare-dns.com
	1.0.0.1 	
	2606:4700:4700::1111 	
	2606:4700:4700::1001 	
Freifunk München e.V. 	5.1.66.255 	anycast01.ffmuc.net
	2001:678:e68:f000:: 	
	5.1.66.255 	dot.ffmuc.net
	2001:678:e68:f000:: 	
dns.sb 	185.222.222.222 	dns.sb
	185.184.222.222 	
	2a09:: 	
	2a09::1 	
Google Public Free DNS 	8.8.8.8 	dns.google
	8.8.4.4 	
Austria (AT) 		
Foundation for Applied Privacy 	146.255.56.98 	dot1.applied-privacy.net
	2a01:4f8:c0c:83ed::1 	
Canada (CA) 		
CMRG DNS 	199.58.81.218 	dns.cmrg.net
	2001:470:1c:76d::53 	
Switzerland (CH) 		
Digitale Gesellschaft Schweiz 	185.95.218.42 	dns.digitale-gesellschaft.ch
	185.95.218.43 	
	2a05:fc84::42 	
	2a05:fc84::43 	
post-factum 	140.238.215.192 	dot.post-factum.tk
Germany (DE) 		
Digitalcourage e.V. 	5.9.164.112 	dns3.digitalcourage.de
Lightning Wire Labs 	81.3.27.54 	recursor01.dns.ipfire.org
	2001:678:b28::54 	
	81.3.27.54 	recursor01.dns.lightningwirelabs.com
	2001:678:b28::54 	
Denmark (DK) 		
censurfridns.dk 	89.233.43.71 	unicast.uncensoreddns.org
	2a01:3a0:53:53:: 	
Finland (FI) 		
Snopyta 	95.216.24.230 	fi.dot.dns.snopyta.org
	2a01:4f9:2a:1919::9301 	
France (FR) 		
Neutopia 	89.234.186.112 	dns.neutopia.org
	2a00:5884:8209::2 	
Luxembourg (LU) 		
Restena Foundation 	158.64.1.29 	kaitain.restena.lu
	2001:a18:1::29 	
Netherlands (NL) 		
GetDNS 	185.49.141.37 	getdnsapi.net
	2a04:b900:0:100::37 	
Surfnet 	145.100.185.17 	dnsovertls2.sinodun.com
	145.100.185.18 	dnsovertls3.sinodun.com
	2001:610:1:40ba:145:100:185:17 	
	2001:610:1:40ba:145:100:185:18 	
United States (US) 		
Comcast / Xfinity (beta) 	96.113.151.145 	dot.xfinity.com