#!/usr/bin/env python3

import socket
import requests
import ipaddress
from urllib.parse import urlparse

# Check if site is in cloudflare
def isCloudFlare(link):
	parsed_uri = urlparse(link)
	domain = '{uri.netloc}'.format(uri = parsed_uri)
	try:
		origin = socket.gethostbyname(domain)
		iprange = requests.get('https://www.cloudflare.com/ips-v4').text
		ipv4 = [row.rstrip() for row in iprange.splitlines()]
		for i in range(len(ipv4)):
			if ipaddress.ip_address(origin) in ipaddress.ip_network(ipv4[i]):
				return True
	except socket.gaierror:
		print("\033[1;31m"+"[-]"+"\033[0m"+"Unable to verify if victim's IP address belong to a CloudFlare\'s subnet!")
		return False
