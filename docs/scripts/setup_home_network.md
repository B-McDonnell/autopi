# Usage
- Prompts user for network information and adds the information to network configuration.


# Implementation
- Uses user input to configure a new network via `CSM_add_network`.

# Dependencies
- Uses stdiomask
- Uses `CSM_add_network` as command
- Uses `CSM_wpa_country` as command

# Technical considerations
- Sets country to 'US' as default if empty.
- stdiomask must be installed as root.
