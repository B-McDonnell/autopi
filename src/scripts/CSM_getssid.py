#!/usr/bin/env python3

import subprocess
import sys


def is_wireless_active(interface: str):
    """
    Check if the interface is an active wireless interface.
    Parameters:
        interface: str -- the name of an interface
    Returns:
        active: bool
    Internally uses iwconfig return code to determine if the interface is wireless
    """
    result = subprocess.run(['iwconfig', interface], capture_output=True)
    if result.returncode != 0:
        return False
    return True


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
    return output, len(output) > 0


if __name__ == '__main__':
    # take second argument if supplied to be interface name
    interface = sys.argv[1] if len(sys.argv) > 1 else 'wlan0'

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
