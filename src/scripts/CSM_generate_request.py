#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import netifaces
import json
import ssl
import urllib.request
import CSM_getip
import CSM_get_hwid
import CSM_get_devid
import CSM_getssid
import CSM_get_mac


def get_interfaces():
    ifaces = ['wlan0', 'eth0']
    ref_ifaces = netifaces.interfaces()
    present = []
    for i in ifaces:
        if i in ref_ifaces:
            present.append(i)
    return present


def select_interface(interfaces: list):
    """
    Select first interface available and get its ip address
    Parameters:
        interfaces: list -- list of interface strings, the first entry that has an ip will be selected
    returns:
         interface_available:bool, interface_name: str, ip_addr: str

    Note:
    To properly select the interface, you have to get its ip, so the ip is returned as well
    """
    interface = ''
    has_ip = False
    for i in interfaces:
        int_ip, status = CSM_getip.get_interface_ip(i)
        if status:
            ip = int_ip
            interface = i
            has_ip = True
            break
    return has_ip, interface, ip


def generate_shutdown_request():
    """
    Return field(s) needed for the request
    In this case, 'event: shutdown'
    """
    return {'event': 'shutdown'}


def get_mac(interface: str):
    return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']


def generate_general_request():
    """
    Returns fields needed for request
    """
    available, int_name, ip = select_interface(get_interfaces())
    if not available:  # can't send message
        # raise exceptiontype
        sys.exit(1)  # TODO there should *maybe* be logging here...

    mac = get_mac(int_name)
    fields = {
                'ip': ip,
                'mac': mac,
             }

    ssid,status = CSM_getssid.get_ssid(int_name)
    if status:  # ensures ssid available for interface
        fields['ssid'] = ssid
    ssh_status = 'up'  # FIXME do this right...
    fields['ssh'] = ssh_status
    vnc_status = 'up'  # FIXME do this right...
    fields['vnc'] = vnc_status

    return fields


def get_id_fields():
    """
    Return dev and hardware IDs
    """
    hwid = CSM_get_hwid.get_hwid()
    devid = CSM_get_devid.get_devid()
    return {'hwid': hwid, 'devid': devid}


def load_request(request_path: Path):
    """
    Load request JSON file
    """
    try:
        with open(request_path) as f:
            return f.read()
    except:
        return ''

def save_request(request_path: Path, request: str):
    """
    Save request JSON file
    """
    with open(request_path, "w") as f:
        f.write(request)  # TODO add return behavior


def send_request(request: dict):
    API_URL = 'http://localhost:8000/'
    req_json = json.dumps(request).encode('utf-8')
    ctxt = ssl.create_default_context()
    req = urllib.request.Request(API_URL, data=req_json)
    req.add_header('Content-Type', 'application/json')
    resp = urllib.request.urlopen(req)
    # resp = request.urlopen(req, context=ctxt)  # uncomment for SSL
    return resp  # FIXME determine return type


def main(*args):
    CSM_ROOT = Path('/var/csm/')
    OLD_REQ = Path(CSM_ROOT) / 'old_request.json'

    shutdown_req = len(args) > 0 and args[0] == 'SHUTDOWN'
    force_req = True
    if not shutdown_req:
        force_req = len(args) > 0 and args[0] == 'START'

    if shutdown_req:
        request_fields = generate_shutdown_request()
    else:
        request_fields = generate_general_request()

    request = get_id_fields()
    if force_req:
        # perform union
        request = {**request, **request_fields}
    else:
        # compare new request to previous
        old = load_request(OLD_REQ)
        new_req = json.dumps(request_fields)
        if old != new_req:
            # they are different, so keep all fields
            save_request(OLD_REQ, new_req)
            # perform union
            request = {**request, **request_fields}

    print(request)
    resp = send_request(request)
    print(resp.status)
    print(resp.readlines())


if __name__ == '__main__':
    main(*sys.argv[1:])
