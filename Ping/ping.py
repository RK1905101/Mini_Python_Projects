import os
import socket
import struct
import time
import re
import sys
import argparse

def checksum(source_string):
    """ Calcula o checksum ICMP. """
    sum = 0
    max_count = (len(source_string) // 2) * 2
    count = 0

    while count < max_count:
        val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + val
        sum = sum & 0xffffffff
        count += 2

    if max_count < len(source_string):
        sum = sum + source_string[-1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def ping(host, count=4, timeout=1):
    icmp = socket.getprotobyname("icmp")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError:
        print("This program needs to be run by a superuser (administrator/root)")
        sys.exit(1)

    addr = socket.gethostbyname(host)
    print(f"PING {host}/{addr}: sending {count} packages ICMP")

    for seq in range(count):
        header = struct.pack("bbHHh", 8, 0, 0, os.getpid() & 0xFFFF, seq)
        data = struct.pack("d", time.time())
        my_checksum = checksum(header + data)
        header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), os.getpid() & 0xFFFF, seq)
        packet = header + data

        sock.sendto(packet, (addr, 1))
        start = time.time()
        sock.settimeout(timeout)

        try:
            recv, _ = sock.recvfrom(1024)
            end = time.time()
            delay = (end - start) * 1000
            print(f"Answers from  {addr}: time={delay:.2f} ms")
        except socket.timeout:
            print("Timeout.")

        time.sleep(1)

def check_args():
  parser = argparse.ArgumentParser(prog='ping',description = "Sample ping python implemented")
  parser.add_argument("-H", "--Help", help = "Example: Help argument", required = False, default = "")
  parser.add_argument("-c", "--count", type=int, help = "stop after <count> replies", required = False, default = 4)
  parser.add_argument("-W", "--timeout", type=int, help = "time to wait for responses", required = False, default = 1)
  parser.add_argument('destination', type=str)
  argument = parser.parse_args()
  status = False
        
  if argument.Help:
    print("Usage\n  ping [options] <destination>")
    parser.print_help()

  return argument     
     

if __name__ == '__main__':
    if len(sys.argv)==1:
      host = input("Hostname or IP to ping: ")
      ping(host)
    else:
      args=check_args()
      ping(args.destination, count=args.count, timeout=args.timeout)
        