import time
import re

LOG_FILE = "server_logs.txt"
THRESHOLD = 3 # Alert after 3 failed attempts
failed_logins = {} # Dictionary to store IP counts: {'192.168.1.1': 1}

def monitor_logs():
    print("[*] SIEM started. Monitoring logs...")
    
    # Open the file and go to the end (like 'tail -f')
    with open(LOG_FILE, "r") as f:
        f.seek(0, 2) 
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            # Use Regex to parse the line
            # Looking for: "Failed password for [user] from [ip]"
            match = re.search(r"Failed password for (\w+) from ([\d\.]+)", line)
            
            if match:
                user = match.group(1)
                ip = match.group(2)
                
                # Update the counter for this IP
                if ip in failed_logins:
                    failed_logins[ip] += 1
                else:
                    failed_logins[ip] = 1
                
                print(f"[ALERT] Failed Login Detected: User: {user} | IP: {ip} | Count: {failed_logins[ip]}")

                # Check Threshold
                if failed_logins[ip] >= THRESHOLD:
                    trigger_alert(ip, user)
                    failed_logins[ip] = 0 # Reset counter after alert

def trigger_alert(ip, user):
    print("\n" + "#" * 50)
    print(f"!!! CRITICAL ALERT !!!")
    print(f"BRUTE FORCE DETECTED FROM IP: {ip}")
    print(f"Targeted Account: {user}")
    print("#" * 50 + "\n")
    # In a real job, this would email the SOC team or block the IP via Firewall

if __name__ == "__main__":
    monitor_logs()