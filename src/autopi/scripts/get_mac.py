#!/usr/bin/env python3
"""Get the MAC address of an interface."""

import sys

import autopi.util.user_interface as ui
from autopi.util.network_info import get_mac


def user_input() -> str:
    """Get an interface from the user.

    Returns:
        str: Network interface (wlan0 or eth0).
    """
    # TODO: possibly default interfaces from config
    connection = ui.get_input(
        "What is your connection type? (ethernet, wireless)",
        validator=lambda l: l.lower() in ("ethernet", "wifi", "wireless"),
    )
    return "eth0" if connection.lower() == "ethernet" else "wlan0"


def main() -> str:
    """If there is not an argument in the call, ask for user input.

    Returns:
        str: MAC address.
    """
    if len(sys.argv) == 1:
        interface = user_input()
    else:
        interface = sys.argv[1]
    return get_mac(interface)


if __name__ == "__main__":
    print(main())