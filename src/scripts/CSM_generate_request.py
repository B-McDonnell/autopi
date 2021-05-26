#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import netifaces
import json
import ssl
import urllib.request
import subprocess
import CSM_getip
import CSM_get_hw_id
import CSM_get_dev_id
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


def generate_shutdown_request() -> dict:
    """
    Return field(s) needed for the request
    In this case, 'event: shutdown'
    """
    return {'event': 'shutdown'}


def get_mac(interface: str) -> str:
    return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']


def get_service_status(service: str) -> str:
    """
    Returns a string to be used as the service status. 
    Obtains status from 'service sshd status' return code. 
    0 => UP, else => DOWN
    The return codes are different per-service, but 0 should always imply UP.
    """
    result = subprocess.run(['service', service, 'status'], capture_output=True)
    code = result.returncode
    if code == 0:
        return 'up'
    else:
        return 'down'


def get_ssh_status():
    return get_service_status('sshd')


def get_vnc_status():
    # Currently, there are two services, I'm uncertain which one matters
    return get_service_status('vncserver-virtuald')
    #return get_service_status('vncserver-x11-systemd')


def generate_general_request() -> dict:
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
    fields['ssh'] = get_ssh_status()
    fields['vnc'] = get_vnc_status()

    return fields


def get_id_fields() -> dict:
    """
    Return dev and hardware IDs
    """
    hwid = CSM_get_hw_id.get_hw_id()
    devid = CSM_get_dev_id.get_dev_id()
    return {'hwid': hwid, 'devid': devid}


def load_request(request_path: Path) -> str:
    """
    Load request JSON file as string
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
    try:
        with open(request_path, "w") as f:
            f.write(request)
    except:
        pass  # TODO log the event


def send_request(request: dict):
    API_URL = 'http://localhost:8000/'
    req_json = json.dumps(request).encode('utf-8')
    req = urllib.request.Request(API_URL, data=req_json)
    req.add_header('Content-Type', 'application/json')
    resp = None
    try: 
        resp = urllib.request.urlopen(req)  # comment for SSL
        # ctxt = ssl.create_default_context()  # uncomment for SSL
        # resp = request.urlopen(req, context=ctxt)  # uncomment for SSL
    except(urllib.error.URLError):
        print("Connection failed")
        # TODO handle error better?
    return resp  # FIXME determine return type


def parse_commandline(*args):
    """
    Parse the command line and return flags, just two at the moment.
    Returns:
        shutdown_req: bool, force_req: bool
    """
    if len(args) == 0:
        return False, False

    valid = ['SHUTDOWN', 'START']
    if len(args) > 1 or args[0] not in valid:
        print("Invalid commandline arguments")  # TODO proper logging?
        sys.exit(1)

    shutdown_req = args[0] == 'SHUTDOWN'
    return shutdown_req, True


def main(*args):
    CSM_ROOT = Path('/var/csm/')
    OLD_REQ = Path(CSM_ROOT) / 'old_request.json'

    shutdown_req, force_req = parse_commandline(*args)
        
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
    if resp:
        print(resp.status)
        print(resp.readlines())


if __name__ == '__main__':
    main(*sys.argv[1:])
