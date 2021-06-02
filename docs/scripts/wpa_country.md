# Usage
`wpa_country`:
```
usage: wpa_country [-h] (get | update) ...

optional arguments:
  -h, --help      show this help message and exit

subcommands:
  (get | update)
    get           get the current country code. Fails if country code does not exist
    update        change the current country code
```
`wpa_country get`:
```
usage: wpa_country get [-h] [FILENAME]

positional arguments:
  FILENAME    path to configuration file. Fails if file not not exist. Uses /etc/wpa_supplicant/wpa_supplicant.conf by default

optional arguments:
  -h, --help  show this help message and exit
```
`wpa_country update`:
```
usage: wpa_country update [-h] [FILENAME] COUNTRY_CODE

positional arguments:
  FILENAME      path to configuration file. Fails if file not not exist. Uses /etc/wpa_supplicant/wpa_supplicant.conf by default
  COUNTRY_CODE  ISO 3166-1 country code

optional arguments:
  -h, --help    show this help message and exit
```
Retrieves and updates country code information in `wpa_supplicant` configuration files.

# Implementation
Configuration file is parsed and managed in pure Python.

# Dependencies
None

# Technical considerations
`wpa_country` does not validate the country code used. The country code must be in ISO 3166-1 format.
