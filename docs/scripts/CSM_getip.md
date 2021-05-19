# Usage 
`CSM_getip [INTERFACE_NAME]`

By default, the script will fetch the IP address of the active network interface (either eth0 or wlan0). If both eth0 and wlan0 are active, it will favor wlan0.

# Output Format
It will output "Interface: IFTERFACE\_NAME -- IP: x.x.x.x" on success.

# Implementation Notes
The script internally uses ifconfig to fetch the interface information, and parses the output.

It assumes that RUNNING (according to ifconfig) implies the interface is active and has an IP address. It also assumes the interface has proper network connectivity (i.e. if it is running, it doesn't attempt to deduce whether wlan0 or eth0 has better internet connectivity, it just picks the first running interface wlan0, eth0).

# DETAILED IMPLEMENTATION
Script requires python 3.7 (possibly 3.4)

It has two python functions: 
- `get_interface_ip(interface)` which gets the ip address of the specified 'interface' (string) if the interface is available. Returns 'ipaddress,status' (string, boolean respectively). Status (if 'True') indicates that the interface is active (has an ipaddress), ipaddress will be blank if status is 'False'.
- `parse_output_ip(output)` is a helper function for `get_interface_ip(...)`, it expects that output will be the output of running `ifconfig INTERFACE_NAME`. output is a bytes object. The functions returns the same thing as `get_interface_ip(...)`

The script can be used as a python module `import CSM_getip` if desired with no ill effects, as long as the script is in the module path.
