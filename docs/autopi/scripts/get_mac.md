# Usage
`get_mac.py [wlan0 | eth0]`

- Script to retrieve ethernet or wireless MAC address.
- Can be called with parameters (wlan0, eth0)
##Example
- `get_mac.py wlan0` gets wireless MAC address

# Implementation
- Uses netifaces to obtain needed network information

# Dependencies
- `autopi.util.user_interface`
- `autopi.util.network_info`

# Technical considerations
- Uses eth0 and wlan0 as interfaces for argv.
- Looks for "wifi", "wireless", or "ethernet" as user input.