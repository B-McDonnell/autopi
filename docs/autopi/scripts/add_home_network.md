# Usage
- Prompts user for network information and adds the information to network configuration.


# Implementation
- Uses user input to configure a new network via `wpa_interface.py`.

# Dependencies
- Uses `autopi.util.user_interface`
- Uses `autopi.util.wpa_interface`

# Technical considerations
- Sets country to 'US' as default if empty.
- stdiomask must be installed as root.
