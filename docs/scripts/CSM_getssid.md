# Usage
`CSM_getssid [INTERFACE_NAME]`

# Output
The script will simply return the SSID for the specified wireless interface (or wlan0) or indicate that no SSID is connected. Failure can also occur due to an invalid interface name.

# Implementation Notes
The script calls `iwgetid INTERFACE_NAME -r` internally. If the call fails, the result is discarded, otherwise the result is printed as the SSID.

The script requires python3.

The script can safely be used as a module in another python script with `import CSM_getssid` as long as the script is in the module path.
