#!/usr/bin/env python3

import subprocess
import sys


def parse_output_ip(output):
    """ parse ifconfig output and get the ip
    """
    arr = output.split(b'\n')
    if not arr[0].find(b'RUNNING') != -1:
        return '', False
    ipline = arr[1].decode('utf-8').strip()
    iparg = ipline.split(' ')[1]
    return iparg, True


def get_interface_ip(interface):
    """  run ifconfig, check status code, and parse
    """
    result = subprocess.run(['ifconfig', interface], capture_output=True)
    if result.returncode != 0:
        return '', False
    return parse_output_ip(result.stdout)


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
            print('Interface: eth0 -- IP:', wlanip)
        else:
            print('No active interface')
            sys.exit(1)
