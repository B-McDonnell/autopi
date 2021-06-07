# Implementation
Abstracts away the interaction with `wpa_supplicant` and `wpa_cli`.

# Dependencies
- `wpa_cli`
- `wpa_supplicant`

# Technical considerations
While existing configuration settings for `wpa_supplicant` should persist, it is assumed that a valid standard-format config is used. There may be undefined behavior in config modification if the `wpa_supplicant` config is not valid.
