#!/usr/bin/env python3

import subprocess
import sys


def get_ssid(interface: str = 'wlan0'):
    """
    Get wireless SSID for specified interface
    Return ssid,status
    status false if interface nonexistent or no SSID
    """
    result = subprocess.run(['iwgetid', interface, '-r'], capture_output=True)
    if result.returncode != 0:
        return '', False
    output_b = result.stdout
    output = output_b.decode('utf-8').strip()
    return output, True


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # take second argument to be interface name
        ssid, status = get_ssid(sys.argv[1])
        if status:
            print("Interface:", sys.argv[1], "--", "ESSID:", ssid)
        else:
            print("Interface has no SSID")
            sys.exit(1)
    else:
        ssid, status = get_ssid()
        if status:
            print("Interface: wlan0 -- ESSID:", ssid)
        else:
            print("wlan0 not connected")
            sys.exit(1)
