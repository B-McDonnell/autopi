# Usage
- Prompts user for network information and adds the information to network configuration.


# Implementation
- Uses user input to configure a new network via `add_network.py`.

# Dependencies
- Uses stdiomask
- Uses `add_network.py` as command
- Uses `wpa_country.py` as command

# Technical considerations
- Sets country to 'US' as default if empty.
- stdiomask must be installed as root.
