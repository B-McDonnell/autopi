# Usage
- Look in `/boot/new_network.py.txt` file, and use provided network details to add network.


# Implementation
- Uses subprocess to run `add_network.py` and add the provided network.
- Run on reboot, add network, reset .txt file.

# Dependencies
- subprocess

# Technical considerations
- Needs to use `/boot/new_network.py.txt`
