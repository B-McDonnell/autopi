# Usage
`CSM_getssid [INTERFACE_NAME]`

The script will simply return the SSID for the specified wireless interface (or wlan0) or indicate that no SSID is connected. Failure can also occur due to an invalid interface name.

# Implementation Notes
The script calls `iwgetid INTERFACE_NAME -r` internally. If the call fails, the result is discarded, otherwise the result is printed as the SSID.

# DETAILED IMPLEMENTATION
The script requires python3.

The script includes 1 function:
- `get_ssid(interface)` This function will accept an interface name in string form, defaulting to 'wlan0'. It will return 'ssid,status' (string,boolean respectively). If status is true, then the ssid was successfully obtained and returned in 'ssid', otherwise ssid is empty. 

The script can safely be used as a module in another python script with `import CSM_getssid` as long as the script is in the module path.
