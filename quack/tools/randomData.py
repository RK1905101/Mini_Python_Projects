#!/usr/bin/env python3

import json
import random

# Get random IP
def random_IP():
    ip = []
    for _ in range(0, 4):
        ip.append(str(random.randint(1,255)))
    return ".".join(ip)

# Get random referer
def random_referer():
    with open("tools/other/referers.txt", 'r') as referers:
    	referers = referers.readlines()
    return random.choice(referers)

# Get random user agent
def random_useragent():
    with open("tools/other/user_agents.json", 'r') as agents:
        user_agents = json.load(agents)["agents"]
    return random.choice(user_agents)
