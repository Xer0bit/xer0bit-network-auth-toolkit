import os
import sys
import time
import subprocess
from typing import List
import netifaces
import wifi_jammer
import probe_sniffer
import beacon_flooder

class TerminalToolkit:
    def __init__(self):
        self.interface = None
        self.monitor_mode = False
        self.requirements_met = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_requirements(self) -> bool:
        try:
            import scapy
            result = subprocess.run(['which', 'aircrack-ng'], capture_output=True)
            return result.returncode == 0
        except ImportError:
            return False

    def get_wireless_interfaces(self) -> List[str]:
        interfaces = netifaces.interfaces()
        return [iface for iface in interfaces if iface.startswith(('wlan', 'wifi'))]

    def check_monitor_mode(self, interface: str) -> bool:
        try:
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            return 'Mode:Monitor' in result.stdout
        except:
            return False

    def toggle_monitor_mode(self, interface: str):
        if self.check_monitor_mode(interface):
            subprocess.run(['sudo', 'airmon-ng', 'stop', interface])
            self.monitor_mode = False
        else:
            subprocess.run(['sudo', 'airmon-ng', 'start', interface])
            self.monitor_mode = True

    def print_menu(self):
        self.clear_screen()
        print("=== Network Security Toolkit ===")
        print(f"Current Interface: {self.interface or 'None'}")
        print(f"Monitor Mode: {'ON' if self.monitor_mode else 'OFF'}")
        print("\nOptions:")
        print("1. Select Interface")
        print("2. Toggle Monitor Mode")
        print("3. WiFi Jammer")
        print("4. Probe Sniffer")
        print("5. Beacon Flooder")
        print("6. Check Requirements")
        print("0. Exit")

    def select_interface(self):
        interfaces = self.get_wireless_interfaces()
        print("\nAvailable interfaces:")
        for i, iface in enumerate(interfaces, 1):
            print(f"{i}. {iface}")
        try:
            choice = int(input("\nSelect interface number: ")) - 1
            if 0 <= choice < len(interfaces):
                self.interface = interfaces[choice]
                self.monitor_mode = self.check_monitor_mode(self.interface)
        except (ValueError, IndexError):
            print("Invalid selection")
            time.sleep(2)

    def run_tools(self, choice):
        if not self.interface:
            print("No interface selected!")
            time.sleep(2)
            return
        if not self.monitor_mode:
            print("Monitor mode must be enabled first!")
            time.sleep(2)
            return
            
        try:
            if choice == '3':
                wifi_jammer.main(self.interface)
            elif choice == '4':
                probe_sniffer.start_sniffing(self.interface)
            elif choice == '5':
                beacon_flooder.beacon_flood(self.interface)
        except KeyboardInterrupt:
            print("\nStopping...")
        except Exception as e:
            print(f"Error: {str(e)}")
        time.sleep(2)

    def run(self):
        while True:
            self.print_menu()
            choice = input("\nEnter your choice: ")

            if choice == '0':
                if self.monitor_mode and self.interface:
                    self.toggle_monitor_mode(self.interface)
                break
            elif choice == '1':
                self.select_interface()
            elif choice == '2':
                if self.interface:
                    self.toggle_monitor_mode(self.interface)
            elif choice in ['3', '4', '5']:
                self.run_tools(choice)
            elif choice == '6':
                if self.check_requirements():
                    print("All requirements are met!")
                else:
                    print("Requirements not met. Please install required packages.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    toolkit = TerminalToolkit()
    toolkit.run()
