from scapy.all import *

def probe_request(packet):
    if packet.haslayer(Dot11ProbeReq):
        mac = packet.addr2
        ssid = packet.info.decode(errors='ignore')
        print(f"Probe Request from {mac} for SSID: '{ssid}'")

def start_sniffing(interface):
    print(f"[*] Sniffing probe requests on {interface}...")
    print("[*] Press Ctrl+C to stop...")
    try:
        sniff(iface=interface, prn=probe_request, store=0)
    except KeyboardInterrupt:
        print("\n[*] Stopping probe sniffer...")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: sudo python3 {sys.argv[0]} <interface>")
        exit(1)
    start_sniffing(sys.argv[1])