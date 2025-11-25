import time
import random

LOG_FILE = "server_logs.txt"

# Real Public IPs to simulate global traffic
# China, Russia, USA, Brazil, Germany
ip_list = [
    "223.5.5.5",      # China (AliDNS)
    "194.190.160.1",  # Russia
    "45.33.22.11",    # USA 
    "200.147.67.142", # Brazil
    "185.70.40.10"    # Germany
]

users = ["admin", "root", "dev_ops", "sql_svc"]

def write_log(message):
    with open(LOG_FILE, "a") as f:
        timestamp = time.strftime("%b %d %H:%M:%S")
        f.write(f"{timestamp} server sshd[1234]: {message}\n")

print(f"[*] Simulating GLOBAL traffic to {LOG_FILE}...")

try:
    while True:
        # Pick a random IP from our global list
        ip = random.choice(ip_list)
        user = random.choice(users)
        
        # 50/50 chance of failure vs success for the demo
        if random.random() < 0.5:
            write_log(f"Accepted password for {user} from {ip} port 22 ssh2")
        else:
            write_log(f"Failed password for {user} from {ip} port 22 ssh2")
        
        time.sleep(2) # Slower speed to not hit API limits
except KeyboardInterrupt:
    print("\n[!] Stopping log generation.")