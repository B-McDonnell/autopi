# Usage 
`CSM_getip [INTERFACE_NAME]`

By default, the script will fetch the IP address of the active network interface (either eth0 or wlan0). If both eth0 and wlan0 are active, it will favor wlan0.

It will output "Interface: INTERFACE\_NAME -- IP: x.x.x.x" on success.

## Example:
`CSM_getip wlan0` gets ip address of `wlan0`.

# Implementation
The script internally uses netifaces to fetch the interface information, and ensure that the interface exists.

# Dependencies
netifaces

Python 3.7
