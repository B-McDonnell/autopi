# Usage
`CSM_getssid [INTERFACE_NAME]`

- `INTERFACE_NAME` is `wlan0` by default. Script fails if interface not wireless or disconnected.

## Output
The script will simply return the SSID for the specified wireless interface (or `wlan0` by default) or indicate that no SSID is connected. Failure can also occur due to an invalid interface name.

# Implementation Notes
Uses netifaces to check the existence of the interface. If it exists, the script calls `iwgetid INTERFACE_NAME -r` internally. If the call fails or the result is blank the interface is not connected to WIFI, otherwise the result is printed as the SSID.

# Dependencies
- Libraries:
    - `netifaces`
- Technologies
    - `iwgetid`
    - `Python 3`
