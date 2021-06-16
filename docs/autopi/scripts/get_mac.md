# Usage
`get_mac.py [interface]`

- Script to retrieve ethernet or wireless MAC address.

##Example
- `get_mac.py wlan0` gets wireless MAC address

# Implementation
- Uses netifaces to obtain needed network information

# Dependencies
- `autopi.util.user_interface`
- `autopi.util.network_info`

# Technical considerations
- Looks for "wifi", "wireless", or "ethernet" as user input.
