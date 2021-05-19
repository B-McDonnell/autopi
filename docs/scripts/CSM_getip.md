# Usage 
`CSM_getip [INTERFACE_NAME]`

By default, the script will fetch the IP address of the active network interface (either eth0 or wlan0). If both eth0 and wlan0 are active, it will favor wlan0.

# Output Format
It will output "Interface: IFTERFACE\_NAME -- IP: x.x.x.x" on success.

# Implementation Notes
The script internally uses netifaces to fetch the interface information, and parses the output.

# DETAILED IMPLEMENTATION
Script requires python 3.7

It has one python function: 
- `get_interface_ip(interface)` which gets the ip address of the specified 'interface' (string) if the interface is available. Returns 'ipaddress,status' (string, boolean respectively). Status (if 'True') indicates that the interface is active (has an ipaddress), ipaddress will be blank if status is 'False'.

The script can be used as a python module `import CSM_getip` if desired with no ill effects, as long as the script is in the module path.
