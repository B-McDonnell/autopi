#!/usr/bin/env python3
"""Get the IP address on some interface."""

import sys

import netifaces


def get_interface_ip(interface: str):
    """Get the IP address linked to an interface."""
    if interface not in netifaces.interfaces():
        return "", False
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
        ipinfo = addrs[netifaces.AF_INET][0]
        return ipinfo["addr"], True
    return "", False


def main():
    if len(sys.argv) > 1:
        # read command line arg
        ip, status = get_interface_ip(sys.argv[1])
        if status:
            print("Interface:", sys.argv[1], "--", "IP:", ip)
        else:
            print("Interface inactive")
            sys.exit(1)
    else:
        wlanip, wstatus = get_interface_ip("wlan0")
        ethip, estatus = get_interface_ip("eth0")
        if wstatus:
            print("Interface: wlan0 -- IP:", wlanip)
        elif estatus:
            print("Interface: eth0 -- IP:", ethip)
        else:
            print("No active interface")
            sys.exit(1)


if __name__ == "__main__":
    main()
