# Simple Local System Resource Monitor
# Monitors CPU, Memory, and Disk usage

import psutil
import time

# Set thresholds
CPU_LIMIT = 80
MEMORY_LIMIT = 75
DISK_LIMIT = 85

# Check interval in seconds
INTERVAL = 5

def monitor_system():
    print("Starting System Resource Monitor...\n")
    while True:
        cpu = psutil.cpu_percent(1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        print(f"CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%")

        # Alerts
        if cpu > CPU_LIMIT:
            print("ALERT! CPU usage is high!")
        if memory > MEMORY_LIMIT:
            print("ALERT! Memory usage is high!")
        if disk > DISK_LIMIT:
            print("ALERT! Disk usage is high!")

        print("------------------------------")
        time.sleep(INTERVAL)

# Run the monitor
try:
    monitor_system()
except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")
