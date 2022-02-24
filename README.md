1. How do you build, run and use your proxy locally?

- First you need to define which IP address will be used to listen the DNS queries in /etc/proxy.conf file, specifically in the option 'AddressToBind' under the section '[InternalComm]'. By default, the program will allocate the 0.0.0.0 to listen locally the requests. 

To build, you can either use the dockerfile to distribute it as a container image but with elevate privilege, or run the command 'sudo python3 main.py' to execute this application with elevate privileges. The elevated privilege is required because the application needs enough permission to bind a port and ip address within the host or in the container.

--------------------------------------------------------------------------------------------------------
2. What privacy issue arises when using unencrypted communication to query DNS
records?

- You're expose to:
	. Man in Midlle attack, which is the interception of your DNS query before it reach out the original server, and further be modified by the attacker,
	. Unauthorized access to your queries, allow the interceptor, or even other entities in the network service, to collect this information without your consent to other commercial and non-commercial purposes
	. Impossibility to check if you are connected to a reliable DNS server

--------------------------------------------------------------------------------------------------------
3. How would you securely integrate the proxy in a distributed, microservices-oriented
and containerized architecture?

- You can deploy this container (DNS proxy) on each cluster that you have to allow the other containers to access internally this DNS proxy without leaving the internal network cluster by changing the DNS settings of the cluster to be redirected to the internal Docker ip address of the DNS proxy container, once it's already running and listening on TCP/53 and UDP/53

Also, you can deploy this container into a single cluster but using the mapping option to map a specific port and protocal used internally in Docker environment with a port and protocol to be allocated on the host device. This deployment will allow this service be ready to receive both internal request from Docker network as well from other external hosts from your network. 

--------------------------------------------------------------------------------------------------------
4. How would you configure the clients to talk securely to the proxy?

- Once the clients doesn't support DNS over TLS, I would leverage the container archicture to let the containers request DNS queries only internally within the cluster to the DNS proxy container. At the least this communication won't required additional configuration from network perspective, and at the same time you start to isolate or reduce the cross communication between the container clusters.

--------------------------------------------------------------------------------------------------------
5. How would you protect the proxy against MITM attacks?
- Rely on the use of certificates between clients <> proxy, and proxy <> remote server. In this way, if there is any entity without internal certificate (from client side) or a valid public certificate (from server side), the connection can't be done.

--------------------------------------------------------------------------------------------------------
6. How would you ensure the trustworthiness of the remote DNS server?
- By checking the information and status of the certificate of the remote DNS server, including to check if it still valid, for what domains, hostname and ip addresses the certificate cover, for which IP address this remote server is listen for DNS service and if this service is not present in the public deny lists due bad activity detected by security vendors such as Cisco, Imperva, Crowdstrike, Palo Alto, McAfee and others.

--------------------------------------------------------------------------------------------------------
7. What other improvements do you think would be interesting to add to the project?
- This project can be improved in these points:
	. Improve the mechanism to ensure the trustworthiness of the remote DNS server, including the pinning of the certificate
	. Improve the mechanism to monitor and change the remote DNS server appointment automatically based on network metrics like timeout and response time
	. Open the binary DNS request sent from clients and check if the domain requested is present in any deny list publicity or internally available to block the request before it reachs out the remote DNS server
	. Improve the UDP socket code to reduce the time to convert the data from UDP to TCP, and TCP to UDP
	. Implement a mechanism to authenticate the clients based on internal certificates issued by an internal CA, or any other mechanism.