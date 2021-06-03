# Usage
`get_ssid [INTERFACE_NAME]`

- `INTERFACE_NAME` is `wlan0` by default. Script fails if interface not wireless or disconnected.

## Output
The script will simply return the SSID for the specified wireless interface (or `wlan0` by default) or indicate that no SSID is connected. Failure can also occur due to an invalid interface name.

# Implementation Notes
Uses `iwconfig` to check if the interface is wireless. If so, the script calls `iwgetid INTERFACE_NAME -r` internally. If the call fails or the result is blank the interface is not connected to WIFI, otherwise the result is printed as the SSID.

# Dependencies
- Technologies
    - `iwgetid`
    - `iwconfig`
    - `Python 3`
