#!/usr/bin/env python3
"""Delete a network from user input."""


import util.network_info as ni
import util.user_interface as ui
import util.wpa_interface as wpa


def main():
    ssid = ui.get_input(
        "What is the SSID of the network to be deleted? (case sensitive)",
        validator=wpa.is_valid_ssid,
        error_message=wpa.SSIDLengthError.constraint_msg,
    )
    if ni.delete_ssid(ssid):
        print(ssid+ " deleted!")
    else:
        print("Error: None or mutiple networks with name: "+ssid)


if __name__ == "__main__":
    main()
