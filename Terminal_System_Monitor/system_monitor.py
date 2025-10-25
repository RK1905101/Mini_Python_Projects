"""
SysNet Monitor — Terminal system & network stats dashboard.
Single-file monitoring tool with CPU, memory, disk, network, and ping metrics.
"""

import psutil
import time
import sys
import shutil
import argparse
import subprocess
import platform
import math
from collections import deque
from datetime import datetime
from statistics import mean

DEFAULT_PING_HOST = "8.8.8.8"
DEFAULT_RATE = 1.0
HISTORY_LENGTH = 60
DEFAULT_CPU_ALERT = 80.0
DEFAULT_MEM_ALERT = 80.0
DEFAULT_PING_ALERT = 200.0
DEFAULT_PING_COUNT = 3

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
DIM = "\033[2m"

def clear_screen():
    sys.stdout.write("\033[2J\033[H")

def hide_cursor():
    sys.stdout.write("\033[?25l")

def show_cursor():
    sys.stdout.write("\033[?25h")

def flush():
    sys.stdout.flush()

def term_size():
    return shutil.get_terminal_size((100, 30))

def human_bytes(n):
    step = 1024.0
    if n < step:
        return f"{n} B"
    for unit in ("KB", "MB", "GB", "TB"):
        n /= step
        if n < step:
            return f"{n:.2f} {unit}"
    return f"{n:.2f} PB"

def uptime_str(start_ts):
    dt = datetime.now() - datetime.fromtimestamp(start_ts)
    days, hrs = dt.days, dt.seconds // 3600
    mins, secs = (dt.seconds % 3600) // 60, dt.seconds % 60
    if days:
        return f"{days}d {hrs}h {mins}m"
    if hrs:
        return f"{hrs}h {mins}m"
    if mins:
        return f"{mins}m {secs}s"
    return f"{secs}s"

def percent_bar(pct, width=30):
    pct = max(0.0, min(100.0, pct))
    filled = int(round((pct / 100.0) * width))
    return "[" + "#" * filled + "-" * (width - filled) + "]"

def sparkline(values, width=30, minval=None, maxval=None):
    ticks = "▁▂▃▄▅▆▇█"
    if not values:
        return " " * width
    minval = min(values) if minval is None else minval
    maxval = max(values) if maxval is None else maxval
    if math.isclose(maxval, minval):
        return ticks[0] * min(len(values), width)
    
    arr = list(values)
    if len(arr) > width:
        step = len(arr) / width
        out = [arr[int(i * step)] for i in range(width)]
    else:
        out = arr + [arr[-1]] * (width - len(arr))
    
    return "".join(
        ticks[max(0, min(len(ticks) - 1, int(round((v - minval) / (maxval - minval) * (len(ticks) - 1)))))]
        for v in out
    )

def safe_ping(host, count=1, timeout=1000):
    system = platform.system().lower()
    try:
        if system == "windows":
            out = subprocess.check_output(
                ["ping", "-n", str(count), "-w", str(timeout), host],
                stderr=subprocess.DEVNULL, universal_newlines=True
            )
            for line in out.splitlines():
                if "Average" in line and "=" in line:
                    last = line.split("=")[-1].strip()
                    if last.endswith("ms"):
                        return float(last.replace("ms", "").strip())
                if "time=" in line:
                    try:
                        return float(line.split("time=")[1].split()[0].replace("ms", ""))
                    except:
                        continue
        else:
            timeout_s = max(1, int(math.ceil(timeout / 1000.0)))
            out = subprocess.check_output(
                ["ping", "-c", str(count), "-W", str(timeout_s), host],
                stderr=subprocess.DEVNULL, universal_newlines=True
            )
            for line in out.splitlines():
                if "time=" in line:
                    try:
                        return float(line.split("time=")[1].split()[0])
                    except:
                        continue
    except Exception:
        pass
    return None

class SysNetMonitor:
    def __init__(self, ping_host=DEFAULT_PING_HOST, rate=DEFAULT_RATE,
                 cpu_alert=DEFAULT_CPU_ALERT, mem_alert=DEFAULT_MEM_ALERT,
                 ping_alert=DEFAULT_PING_ALERT, ping_count=DEFAULT_PING_COUNT):
        self.ping_host = ping_host
        self.rate = max(0.1, float(rate))
        self.cpu_alert = cpu_alert
        self.mem_alert = mem_alert
        self.ping_alert = ping_alert
        self.ping_count = ping_count

        net = psutil.net_io_counters()
        self.prev_bytes_sent = net.bytes_sent
        self.prev_bytes_recv = net.bytes_recv
        self.total_sent = 0
        self.total_recv = 0

        self.cpu_history = deque(maxlen=HISTORY_LENGTH)
        self.mem_history = deque(maxlen=HISTORY_LENGTH)
        self.net_down_history = deque(maxlen=HISTORY_LENGTH)
        self.net_up_history = deque(maxlen=HISTORY_LENGTH)
        self.ping_history = deque(maxlen=HISTORY_LENGTH)

        self.last_ping_time = 0
        self.ping_interval = max(1.0, self.rate * 2)
        self.last_ping_ms = None
        self.pings_done = 0

    def gather(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        per_cpu = psutil.cpu_percent(interval=None, percpu=True)
        
        vm = psutil.virtual_memory()
        swap = psutil.swap_memory()

        disk_usages = []
        seen = set()
        for p in psutil.disk_partitions(all=False):
            if p.mountpoint not in seen:
                try:
                    du = psutil.disk_usage(p.mountpoint)
                    disk_usages.append((p.mountpoint, du.percent, du.used, du.total))
                    seen.add(p.mountpoint)
                except:
                    continue
        disk_usages.sort(key=lambda x: -x[1])

        net = psutil.net_io_counters()
        delta_sent = net.bytes_sent - self.prev_bytes_sent
        delta_recv = net.bytes_recv - self.prev_bytes_recv
        down_bps = delta_recv / max(1e-6, self.rate)
        up_bps = delta_sent / max(1e-6, self.rate)

        self.prev_bytes_sent = net.bytes_sent
        self.prev_bytes_recv = net.bytes_recv
        self.total_sent += delta_sent
        self.total_recv += delta_recv

        now = time.time()
        ping_ms = None
        if self.ping_count != 0 and self.pings_done < 3 and (now - self.last_ping_time >= self.ping_interval):
            ping_results = [t for _ in range(max(1, self.ping_count)) 
                           if (t := safe_ping(self.ping_host, count=1, timeout=800)) is not None]
            if ping_results:
                ping_ms = sum(ping_results) / len(ping_results)
            self.last_ping_time = now
            if ping_ms is not None:
                self.last_ping_ms = ping_ms
            self.pings_done += 1
        else:
            ping_ms = self.last_ping_ms

        self.cpu_history.append(cpu_percent)
        self.mem_history.append(vm.percent)
        self.net_down_history.append(down_bps)
        self.net_up_history.append(up_bps)
        if ping_ms is not None:
            self.ping_history.append(ping_ms)

        return {
            "cpu_percent": cpu_percent,
            "per_cpu": per_cpu,
            "mem_percent": vm.percent,
            "mem_used": vm.used,
            "mem_total": vm.total,
            "swap": swap,
            "disks": disk_usages,
            "uptime": uptime_str(psutil.boot_time()),
            "down_bps": down_bps,
            "up_bps": up_bps,
            "total_recv": self.total_recv,
            "total_sent": self.total_sent,
            "ping_ms": ping_ms
        }

    def render(self, stats):
        cols, rows = term_size()
        clear_screen()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{BOLD}{CYAN}SysNet Monitor{RESET}  {DIM}{now}{RESET}")
        print("-" * cols)

        alert_cpu = stats['cpu_percent'] >= self.cpu_alert
        cpu_bar = percent_bar(stats['cpu_percent'], width=30)
        print(f"{BOLD}CPU{RESET}   {cpu_bar}  {'' if not alert_cpu else RED + '⚠ HIGH' + RESET}")
        
        per = stats["per_cpu"]
        if per and len(per) <= 64:
            print(" per-core: " + " | ".join(f"{i}:{int(p)}%" for i, p in enumerate(per)))
        print(" trend: " + sparkline(self.cpu_history, width=min(40, cols - 20)))

        alert_mem = stats["mem_percent"] >= self.mem_alert
        mem_bar = percent_bar(stats["mem_percent"], width=30)
        print(f"\n{BOLD}MEM{RESET}   {mem_bar}  {stats['mem_percent']:.1f}%  "
              f"({human_bytes(stats['mem_used'])} / {human_bytes(stats['mem_total'])})"
              f"{'' if not alert_mem else RED + '  ⚠ HIGH' + RESET}")
        print(" trend: " + sparkline(self.mem_history, width=min(40, cols - 20)))

        print(f"\n{BOLD}DISKS (top usage){RESET}")
        for mount, pct, used, total in stats["disks"][:3]:
            print(f" {mount:10s} {percent_bar(pct, width=20)} {pct:.1f}%  {human_bytes(used)}/{human_bytes(total)}")

        print(f"\n{BOLD}NET{RESET}   ↓ {human_bytes(stats['down_bps'])}/s   ↑ {human_bytes(stats['up_bps'])}/s")
        max_net = max(max(self.net_down_history) if self.net_down_history else stats['down_bps'], 1)
        print(" down: " + sparkline(self.net_down_history, width=min(40, cols - 20), minval=0, maxval=max_net))
        print("   up: " + sparkline(self.net_up_history, width=min(40, cols - 20), minval=0, maxval=max_net))
        print(f" total recv: {human_bytes(stats['total_recv'])}   total sent: {human_bytes(stats['total_sent'])}")

        ping_ms = stats.get("ping_ms")
        ping_s = f"{ping_ms:.1f} ms" if ping_ms is not None else "N/A"
        avg_ping = f"{mean(self.ping_history):.1f} ms" if self.ping_history else "0.0 ms"
        alert_ping = ping_ms is not None and ping_ms >= self.ping_alert
        print(f"\n{BOLD}PING{RESET}  host: {self.ping_host}  last: {ping_s}  avg: {avg_ping}"
              f"{'' if not alert_ping else RED + '  ⚠ HIGH' + RESET}")
        if self.ping_history:
            print(" trend: " + sparkline(self.ping_history, width=min(40, cols - 20),
                                       minval=min(self.ping_history), maxval=max(self.ping_history)))

        print(f"\nUptime: {stats['uptime']}    Refresh: {self.rate}s    Samples: {len(self.cpu_history)}")
        
        alerts = []
        if alert_cpu:
            alerts.append(f"CPU {stats['cpu_percent']:.0f}%")
        if alert_mem:
            alerts.append(f"MEM {stats['mem_percent']:.0f}%")
        if alert_ping:
            alerts.append(f"PING {ping_ms:.0f}ms")
        if alerts:
            print(RED + BOLD + "\n! ALERTS: " + "; ".join(alerts) + RESET)
        
        print("\nPress Ctrl+C to quit. Re-run with --help for options.")
        flush()

    def run(self):
        hide_cursor()
        try:
            if self.ping_count == 0:
                print(YELLOW + "\nPing is disabled. The monitor will run until you press Ctrl+C." + RESET)
                print(YELLOW + "Use --ping-count=N (N>0) to auto-quit after N ping cycles." + RESET)
                flush()
                while True:
                    start = time.time()
                    stats = self.gather()
                    self.render(stats)
                    time.sleep(max(0.0, self.rate - (time.time() - start)))
            elif self.ping_count == -1:
                print(YELLOW + "\nContinuous ping mode. The monitor will run until you press Ctrl+C." + RESET)
                flush()
                while True:
                    start = time.time()
                    stats = self.gather()
                    self.render(stats)
                    time.sleep(max(0.0, self.rate - (time.time() - start)))
            else:
                while True:
                    start = time.time()
                    stats = self.gather()
                    self.render(stats)
                    if self.pings_done >= 3:
                        print(GREEN + "\nDone: 3 ping cycles completed. Exiting SysNet Monitor. Bye!" + RESET)
                        break
                    time.sleep(max(0.0, self.rate - (time.time() - start)))
        except KeyboardInterrupt:
            pass
        finally:
            show_cursor()
            if self.ping_count != -1 and self.pings_done < 3:
                print("\nExiting SysNet Monitor. Bye!")

def parse_args():
    p = argparse.ArgumentParser(description="SysNet Monitor — terminal system & network dashboard")
    p.add_argument("--host", help="Ping host (default 8.8.8.8)", default=DEFAULT_PING_HOST)
    p.add_argument("--rate", type=float, help="Refresh rate in seconds (default 1.0)", default=DEFAULT_RATE)
    p.add_argument("--cpu-th", type=float, help="CPU alert threshold percent (default 80)", default=DEFAULT_CPU_ALERT)
    p.add_argument("--mem-th", type=float, help="Memory alert threshold percent (default 80)", default=DEFAULT_MEM_ALERT)
    p.add_argument("--ping-th", type=float, help="Ping alert threshold ms (default 200)", default=DEFAULT_PING_ALERT)
    p.add_argument("--ping-count", type=int, help="Number of pings per refresh (0 disables ping, -1 continuous)", default=DEFAULT_PING_COUNT)
    return p.parse_args()

def main():
    args = parse_args()
    monitor = SysNetMonitor(
        ping_host=args.host,
        rate=args.rate,
        cpu_alert=args.cpu_th,
        mem_alert=args.mem_th,
        ping_alert=args.ping_th,
        ping_count=args.ping_count
    )
    monitor.run()

if __name__ == "__main__":
    main()