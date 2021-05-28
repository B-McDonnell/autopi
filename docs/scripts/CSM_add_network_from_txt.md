# Usage
- Look in .txt file in /boot/, and use provided network details to add network.


# Implementation
- Uses subprocess to run CSM_add_network and add the provided network.
- Run on reboot, add network, reset .txt file.

# Dependencies
- subprocess

# Technical considerations
- Needs to use /boot/CSM_new_network.txt
