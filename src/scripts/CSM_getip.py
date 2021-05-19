#!/usr/bin/env python3

import sys
import netifaces


def get_interface_ip(interface: str):
    """
    Uses module netifaces to get obtain the IP
    address information for the specified interface
    """
    if interface not in netifaces.interfaces():
        return '', False
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
        ipinfo = addrs[netifaces.AF_INET][0]
        return ipinfo['addr'], True
    return '', False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # read command line arg
        ip, status = get_interface_ip(sys.argv[1])
        if status:
            print('Interface:', sys.argv[1], '--', 'IP:', ip)
        else:
            print('Interface inactive')
            sys.exit(1)
    else:
        wlanip, wstatus = get_interface_ip('wlan0')
        ethip, estatus = get_interface_ip('eth0')
        if wstatus:
            print('Interface: wlan0 -- IP:', wlanip)
        elif estatus:
            print('Interface: eth0 -- IP:', ethip)
        else:
            print('No active interface')
            sys.exit(1)
