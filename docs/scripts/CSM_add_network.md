# Usage
```
usage: CSM_add_network [-h] [-o] [--dry-run] [--priority PRIORITY] [-c COUNTRY] (-n | -p PASSWORD) SSID

positional arguments:
  SSID                  SSID of the network

optional arguments:
  -h, --help            show this help message and exit
  -o, --std-out         write network configuration to stdout
  --dry-run             do not update network configuration. --std-out is assumed
  --priority PRIORITY   priority level for the network. Networks with a higher priority network will be joined first
  -c COUNTRY, --country COUNTRY
                        ISO 3166-1 country code for network country. Defaults to US
  -n, --no-password     network does not require a password
  -p PASSWORD, --password PASSWORD
                        password for network. If not specified, will read from stdin
```
Add a network to be automatically connected to.

# Implementation
`CSM_add_network` automatically generates `wpa_supplicant` configurations, adds them to their appropriate location, and reconfigures `wpa` to allow for automatic connections using `wpa_cli`

# Dependencies
- `wpa_cli`
- `wpa_supplicant`