# Usage
- Script to retrieve ethernet or wireless MAC address.
- Can be called with parameters (wlan0, eth0)
##Example
- `CSM_get_mac wlan0` gets wireless MAC address

# Implementation
- Uses netifaces and argv to obtain needed network information

# Dependencies
- netifaces

# Technical considerations
- Uses eth0 and wlan0 as interfaces for argv.
- Looks for "wifi", "wireless", or "ethernet" as user input.
