# Usage
- Deletes network configuration using SSID.

# Implementation
- Uses user input to delete configured network.

# Dependencies
- `util.network_info`
- `util.user_interface`
- `util.wpa_interface`

# Technical considerations
- If multiple networks have the same SSID to be deleted, only all or none can be done.
- For specific edits in this case use: `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
- After edits, reconfigure: `wpa_cli -i wlan0 reconfigure`
