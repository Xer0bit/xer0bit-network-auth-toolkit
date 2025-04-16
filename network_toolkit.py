import os
import sys
import subprocess
import time
from typing import List, Tuple
import netifaces
import PySimpleGUI as sg

class NetworkToolkit:
    def __init__(self):
        self.interface = None
        self.monitor_mode = False
        self.requirements_met = False

    def check_requirements(self) -> bool:
        try:
            import scapy
            result = subprocess.run(['which', 'aircrack-ng'], capture_output=True)
            if result.returncode == 0:
                self.requirements_met = True
                return True
            return False
        except ImportError:
            return False

    def install_requirements(self):
        try:
            subprocess.run(['pip', 'install', 'scapy', 'PySimpleGUI', 'netifaces'])
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'aircrack-ng'])
            return True
        except Exception as e:
            sg.popup_error(f"Error installing requirements: {str(e)}")
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

    def run_wifi_jammer(self):
        import wifi_jammer
        wifi_jammer.main()

    def run_probe_sniffer(self):
        import probe_sniffer
        probe_sniffer.sniff(iface=self.interface, prn=probe_sniffer.probe_request, store=0)

    def run_beacon_flooder(self):
        import beacon_flooder
        beacon_flooder.beacon_flood(self.interface)

    def create_gui(self):
        sg.theme('DarkBlue')

        layout = [
            [sg.Text('Network Security Toolkit', font=('Helvetica', 20))],
            [sg.Text('Interface:'), sg.Combo(self.get_wireless_interfaces(), key='-INTERFACE-', enable_events=True)],
            [sg.Text('Monitor Mode:'), sg.Text('OFF', key='-MONITOR-')],
            [sg.Button('Toggle Monitor Mode')],
            [sg.Frame('Tools', [
                [sg.Button('WiFi Jammer')],
                [sg.Button('Probe Sniffer')],
                [sg.Button('Beacon Flooder')]
            ])],
            [sg.Frame('Status', [
                [sg.Text('Requirements:'), sg.Text('Checking...', key='-REQUIREMENTS-')],
                [sg.Button('Install Requirements')]
            ])],
            [sg.Button('Exit')]
        ]

        window = sg.Window('Network Security Toolkit', layout)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            if event == '-INTERFACE-':
                self.interface = values['-INTERFACE-']
                is_monitor = self.check_monitor_mode(self.interface)
                window['-MONITOR-'].update('ON' if is_monitor else 'OFF')

            if event == 'Toggle Monitor Mode' and self.interface:
                self.toggle_monitor_mode(self.interface)
                window['-MONITOR-'].update('ON' if self.monitor_mode else 'OFF')

            if event == 'Install Requirements':
                if self.install_requirements():
                    window['-REQUIREMENTS-'].update('Met')
                else:
                    window['-REQUIREMENTS-'].update('Failed')

            if not self.requirements_met:
                self.requirements_met = self.check_requirements()
                window['-REQUIREMENTS-'].update('Met' if self.requirements_met else 'Not Met')

            if event == 'WiFi Jammer' and self.interface:
                window.hide()
                self.run_wifi_jammer()
                window.un_hide()

            if event == 'Probe Sniffer' and self.interface:
                window.hide()
                self.run_probe_sniffer()
                window.un_hide()

            if event == 'Beacon Flooder' and self.interface:
                window.hide()
                self.run_beacon_flooder()
                window.un_hide()

        window.close()

if __name__ == "__main__":
    toolkit = NetworkToolkit()
    toolkit.create_gui()
