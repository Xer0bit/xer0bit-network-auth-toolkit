# Network Security Testing Scripts

A collection of network security testing scripts for educational and authorized testing purposes only.

## ⚠️ Legal Disclaimer
These scripts are provided for educational purposes and authorized security testing only. Unauthorized use of these tools against networks you don't own or have explicit permission to test is illegal.

## Scripts Overview

### wifi_jammer.py
A WiFi deauthentication tool that can disrupt wireless connections.

**Features:**
- Monitor mode activation/deactivation
- Access point scanning
- Deauthentication packet sending

**Usage:**
```bash
sudo python wifi_jammer.py
```

### probe_sniffer.py
Captures and displays probe requests from nearby wireless devices.

**Features:**
- Real-time probe request monitoring
- MAC address and SSID logging

**Usage:**
```bash
sudo python probe_sniffer.py <interface>
```

### beacon_flooder.py
Creates multiple fake WiFi networks by broadcasting beacon frames.

**Features:**
- Random SSID generation
- Customizable beacon frame creation
- RSN (WPA2) security simulation

**Usage:**
```bash
sudo python beacon_flooder.py <interface>
```

### network_toolkit.py
A graphical user interface that integrates all network security tools.

**Features:**
- Unified interface for all tools
- Automatic requirement checking and installation
- Monitor mode management
- Interface selection and validation

**Usage:**
```bash
sudo python main.py
```

**Additional Requirements:**
- PySimpleGUI
- netifaces

## Requirements
- Python 3.x
- Scapy library
- Wireless interface capable of monitor mode
- Root/sudo privileges
- aircrack-ng suite

## Installation
```bash
pip install scapy PySimpleGUI netifaces
sudo apt-get install aircrack-ng
```

## Security Notice
These tools should only be used in controlled environments with proper authorization. Misuse may violate laws and regulations.
