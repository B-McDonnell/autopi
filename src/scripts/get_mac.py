#!/usr/bin/env python3
"""Get the MAC address of an interface."""

import sys

import netifaces


def getMAC(interface: str) -> str:
    """Return MAC address using network interface as a parameter.

    Args:
        interface (str): Interface (i.e. wlan0 or eth0).

    Returns:
        str: MAC address.
    """
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
    except Exception as e:
        print("MAC address could not be found:", e)
        sys.exit(1)


def user_input() -> str:
    """Get an interface from the user.

    Returns:
        str: Network interface (wlan0 or eth0).
    """
    while True:
        connection = input("What is your connection type? (ethernet, wireless)\n")
        if connection.lower() == "ethernet":
            return "eth0"
        elif connection.lower() == "wifi" or connection.lower() == "wireless":
            return "wlan0"


def main() -> str:
    """If there is not an argument in the call, ask for user input.

    Returns:
        str: MAC address.
    """
    if len(sys.argv) == 1:
        interface = user_input()
    else:
        interface = sys.argv[1]
    return getMAC(interface)


if __name__ == "__main__":
    print(main())
