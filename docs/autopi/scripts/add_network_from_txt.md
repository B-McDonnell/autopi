# Usage
`add_network_from_txt.py`

- Look in `/boot/CSM_new_network.txt` file, and use provided network details to add network.


# Implementation
- Run on reboot, add network, reset .txt file.

# Dependencies
- `autopi.util.wpa_interface`

# Technical considerations
- Needs to use `/boot/CSM_new_network.txt`
