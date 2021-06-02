#!/usr/bin/env python3
"""Get the SSID of the network an interface is connected to."""

import subprocess
import sys


def is_wireless_active(interface: str) -> bool:
    """Check if the interface is an active wireless interface.

    Internally uses iwconfig return code to determine if the interface is wireless.

    Args:
        interface (str): the name of an interface.

    Returns:
        bool: Interface is wireless and active.
    """
    try:
        result = subprocess.run(["iwconfig", interface], capture_output=True)
    except FileNotFoundError:
        # TODO Probably log this
        return "", False  # iwconfig not present
    if result.returncode != 0:
        return False
    return True


def get_ssid(interface: str) -> (str, bool):
    """
    Get wireless SSID for specified interface.

    Args:
        interface (str): the name of an interface.

    Returns:
        str: ssid of the network interface.
        bool: status. If true, ssid was successfully obtained and returned in 'ssid', otherwise ssid is empty. If false interface nonexistent, interface is not wireless, or currently has no SSID.
    """
    try:
        result = subprocess.run(["iwgetid", interface, "-r"], capture_output=True)
    except FileNotFoundError:
        # TODO Probably log this
        return "", False  # iwgetid not present
    if result.returncode != 0:
        return "", False
    output_b = result.stdout
    output = output_b.decode("utf-8").strip()
    return output, len(output) > 0


def main():
    # take second argument if supplied to be interface name
    interface = sys.argv[1] if len(sys.argv) > 1 else "wlan0"

    status = is_wireless_active(interface)
    if not status:
        print("Interface not connected, not wireless, or inactive")
        sys.exit(1)

    ssid, status = get_ssid(interface)
    if status:
        print("Interface:", interface, "--", "ESSID:", ssid)
    else:
        print("Interface '" + interface + "' has no SSID (Not connected).")
        sys.exit(1)


if __name__ == "__main__":
    main()
