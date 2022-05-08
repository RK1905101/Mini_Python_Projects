#!/usr/bin/env python3

import os

os.system("printf '\033]2;Quack Toolkit\a'")

import argparse
import sys
import signal

def signal_handler(signal, frame):
    A = '\033[1;33m'
    W = '\033[0m'
    E = '\033[0m'
    print(A+'\n[!]'+W+' Attack terminated.'+E)
    os._exit(0)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--target", type = str, metavar = "<ip:port/URL/phone>",
					help = "Target IP and port, URL or phone.")
	parser.add_argument("--tool", type = str, metavar = "[SMS|NTP|TCP|UDP|SYN|POD|SLOWLORIS|MEMCACHED|HTTP|NJRAT]",
					help = "Attack tool.")
	parser.add_argument("--timeout", type = int, default = 10, metavar = "<timeout>",
					help = 'Timeout in seconds.')
	parser.add_argument("--threads", type = int, default = 3, metavar = "<threads>",
					help = "Threads count.")
	parser.add_argument("-u", "--update", action='store_true', dest="update", help = "Update Quack Toolkit.")
	parser.add_argument("--version", action='store_true', dest="version", help = "Show Quack Toolkt version.")

	# Get args
	args = parser.parse_args()
	threads = args.threads
	time = args.timeout
	method = str(args.tool).upper()
	target = args.target

	if method == "NTP":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.ntp import NTP_ATTACK
		NTP_ATTACK(threads, time, target)
		
	elif args.update:
		os.system("chmod +x bin/quack && bin/quack -u")
		sys.exit()

	elif args.version:
		print("")
		os.system("cat banner/banner.txt")
		print("")
		print("Quack Toolkit v2.0")
		sys.exit()

	elif method == "SYN":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.syn import SYN_ATTACK
		SYN_ATTACK(threads, time, target)

	elif method == "TCP":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.tcp import TCP_ATTACK
		TCP_ATTACK(threads, time, target)

	elif method == "POD":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.pod import POD_ATTACK
		POD_ATTACK(threads, time, target)

	elif method == "NJRAT":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.njrat import NJRAT_ATTACK
		NJRAT_ATTACK(threads, time, target)

	elif method == "UDP":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.udp import UDP_ATTACK
		UDP_ATTACK(threads, time, target)

	elif method == "HTTP":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.http import HTTP_ATTACK
		HTTP_ATTACK(threads, time, target)

	elif method == "SLOWLORIS":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.slowloris import SLOWLORIS_ATTACK
		SLOWLORIS_ATTACK(threads, time, target)
	
	elif method == "MEMCACHED":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.other.memcached import MEMCACHED_ATTACK
		MEMCACHED_ATTACK(threads, time, target)

	elif method == "SMS":
		signal.signal(signal.SIGINT, signal_handler)
		import tools.addons.clean
		import tools.addons.logo
		from tools.SMS.main import SMS_ATTACK
		SMS_ATTACK(threads, time, target)

	else:
		parser.print_help()

if __name__ == '__main__':
	main()
