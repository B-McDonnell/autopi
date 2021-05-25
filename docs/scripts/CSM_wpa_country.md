# Usage
`CSM_wpa_country`:
```
usage: CSM_wpa_country [-h] (get | update) ...

optional arguments:
  -h, --help      show this help message and exit

subcommands:
  (get | update)
    get           get the current country code. Fails if country code does not exist
    update        change the current country code
```
`CSM_wpa_country get`:
```
usage: CSM_wpa_country get [-h] [FILENAME]

positional arguments:
  FILENAME    path to configuration file. Fails if file not not exist. Uses /etc/wpa_supplicant/wpa_supplicant.conf by default

optional arguments:
  -h, --help  show this help message and exit
```
`CSM_wpa_country update`:
```
usage: CSM_wpa_country update [-h] [FILENAME] COUNTRY_CODE

positional arguments:
  FILENAME      path to configuration file. Fails if file not not exist. Uses /etc/wpa_supplicant/wpa_supplicant.conf by default
  COUNTRY_CODE  ISO 3166-1 country code

optional arguments:
  -h, --help    show this help message and exit
```

# Implementation
`CSM_wpa_country` allows for the detection, retrieval, and update of the country code in a `wpa_supplicant` configuration file

# Dependencies
None