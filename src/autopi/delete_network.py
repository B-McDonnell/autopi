#!/usr/bin/env python3
"""Delete a network from user input."""


import util.user_interface as ui
import util.wpa_interface as wpa


def delete_ssid():
    """Delete network after check if exists."""
    ssid = ui.get_input(
        "What is the SSID of the network to be deleted? (case sensitive)",
        validator=wpa.is_valid_ssid,
        error_message=wpa.SSIDLengthError.constraint_msg,
    )
    config_file = wpa.get_default_wpa_config_file()
    if _ssid_exists(ssid, config_file):
        new_text = _get_new_config(ssid, config_file)
        with open(config_file, "wt") as fin:
            fin.write(new_text)
            print(ssid + " has been deleted!")
    else:
        print("SSID not found.")


def _ssid_exists(ssid: str, config_file: str) -> bool:
    """Check to see if SSID exists in config.

    Args:
        ssid (str): SSID of network
        config_file (str): File path of network configuration

    Returns:
        bool: Exists
    """
    with open(config_file, "r") as fin:
        current_contents = fin.read()
        if current_contents.find('ssid="' + ssid + '"') == -1:
            return False
        return True


def _get_new_config(ssid: str, config_file: str) -> str:
    """Create new configuration after deletion.

    Args:
        ssid (str): SSID of network
        config_file (str): Fil path of network configuration

    Returns:
        str: Text of new configuration file
    """
    with open(config_file, "r") as fin:
        current_contents = fin.read()
        position = current_contents.find('ssid="' + ssid + '"')
        start = current_contents.rfind("\n\nnetwork={", 0, position)
        end = current_contents.find("}", position)
        new_config = current_contents[0:start:] + current_contents[end + 1::]
        return new_config


if __name__ == "__main__":
    delete_ssid()
