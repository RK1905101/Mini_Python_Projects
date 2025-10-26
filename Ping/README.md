## PING

## Setup and activate virtual environment :
For Unix based systems please execute the following command to create venv and install requirements.
```
make init
source .venv/bin/activate
```

Ping

Needs superusers to run.

Usage: 

    sudo python Ping/ping.py 127.0.0.1

output:

    PING 127.0.0.1/127.0.0.1: sending 4 packages ICMP
    Answers from  127.0.0.1: time=0.01 ms
    Answers from  127.0.0.1: time=0.02 ms
    Answers from  127.0.0.1: time=0.02 ms
    Answers from  127.0.0.1: time=0.03 ms

