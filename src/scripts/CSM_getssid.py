#!/usr/bin/env python3

import subprocess
import sys


def get_ssid(interface: str):
    """
    Get wireless SSID for specified interface
    It will return 'ssid,status' (string,boolean respectively). 
    Returns:
        ssid: str, status: bool
    If status is true, then the ssid was successfully obtained and returned in 'ssid', otherwise ssid is empty. 
    Status false if interface nonexistent, interface is not wireless, or currently has no SSID
    """
    result = subprocess.run(['iwgetid', interface, '-r'], capture_output=True)
    if result.returncode != 0:
        return '', False
    output_b = result.stdout
    output = output_b.decode('utf-8').strip()
    return output, True


if __name__ == '__main__':
    # take second argument if supplied to be interface name
    interface = sys.argv[1] if len(sys.argv) > 1 else 'wlan0'

    ssid, status = get_ssid(sys.argv[1])
    if status:
        print("Interface:", sys.argv[1], "--", "ESSID:", ssid)
    else:
        print("Interface '" + interface + "' not connected.")
        sys.exit(1)
