#!/usr/bin/env python3
"""Add a network from user input."""

import os
import sys

import util.user_interface as ui
import util.wpa_interface as wpa


def _is_yes(user_input: str) -> bool:
    return user_input.lower() in ("y", "yes")


def _is_no(user_input: str) -> bool:
    return user_input.lower() in ("n", "no")


def _is_yes_or_no(user_input: str) -> bool:
    return _is_yes(user_input) or _is_no(user_input)


def set_home_network():
    """Use user input, add a network."""
    # ssid
    ssid = ui.get_input(
        "What is the name of your home network? (case sensitive)",
        validator=wpa.is_valid_ssid,
        error_message=wpa.SSIDLengthError.constraint_msg,
    )

    # password
    if _is_yes(ui.get_input("Does this network have a password? (y/n)", validator=_is_yes_or_no)):
        password = ui.get_secret(
            "What is the password? (It will be encrypted)",
            validator=wpa.is_valid_passwd,
            error_message=wpa.PasswordLengthError.constraint_msg,
        )
    else:
        password = None

    # priority
    if _is_yes(
        ui.get_input(
            "Would you like to set a priority of connecting to this network? (y/n)",
            validator=_is_yes_or_no,
        )
    ):
        priority = ui.get_input(
            "Would you like low, medium, or high priority?",
            validator=lambda l: l.lower() in ("l", "m", "h", "low", "medium", "high"),
        )
        priority = "1" if priority in ("l", "low") else "2" if priority in ("m", "medium") else "3"
    else:
        priority = None

    wpa.add_network(
        network_config=wpa.make_network(ssid, password, priority),
        config_file=wpa.get_default_wpa_config_file(),
    )
    if wpa.get_country(wpa.get_default_wpa_config_file()) is None:
        wpa.update_country(wpa.get_default_wpa_config_file(), country="US")  # TODO: get from config


def main():
    """Tell to run with sudo."""
    if os.geteuid() != 0:
        print("Permission Denied: Must be run as super user!")
        sys.exit(1)
    set_home_network()


if __name__ == "__main__":
    main()
