#!/usr/bin/env python3
"""Get the MAC address of an interface."""

import sys

from util.network_info import get_mac


def main() -> str:
    """If there is not an argument in the call, ask for user input.

    Returns:
        str: MAC address.
    """
    if len(sys.argv) > 1:
        interface = sys.argv[1]
        return get_mac(interface)
    return ""


if __name__ == "__main__":
    print(main())
