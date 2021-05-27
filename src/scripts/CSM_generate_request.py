#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import netifaces
import json
import ssl
import urllib.request
from http.client import HTTPResponse
import subprocess
import CSM_getip
import CSM_get_hw_id
import CSM_get_dev_id
import CSM_getssid
import CSM_get_mac
from typing import Optional


def get_interfaces() -> list:
    """
    Obtain a list of available interfaces.

    Returns:
        list: list of interface name strings.
    """
    ifaces = ['wlan0', 'eth0']
    ref_ifaces = netifaces.interfaces()
    present = []
    for i in ifaces:
        if i in ref_ifaces:
            present.append(i)
    return present


def select_interface(interfaces: list) -> (bool, str, str):
    """
    Select first interface available and get its ip address
    Note:
    To properly select the interface, you have to get its ip, so the ip is returned as well

    Args:
        interfaces (list): list of interface names, the first entry that has an ip will be selected.

    returns:
        bool: interface_available
        str: interface_name
        str: ip_addr

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
    Get field(s) needed for the request
    In this case, 'event: shutdown'.

    Returns:
        dict: Dictionary of field(s)
    """
    return {'event': 'shutdown'}


def get_mac(interface: str) -> str:
    return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']


def get_service_status(service: str) -> str:
    """
    Returns a string to be used as the service status.
    Obtains status from 'service sshd status' return code.
    The return codes are different per-service, but 0 should always imply UP.

    Args:
        service (str): service name.

    Returns:
        str: service status. 0 => UP, not 0 => DOWN.
    """
    result = subprocess.run(['service', service, 'status'],
                            capture_output=True)
    code = result.returncode
    if code == 0:
        return 'up'
    else:
        return 'down'


def get_ssh_status() -> str:
    return get_service_status('sshd')


def get_vnc_status() -> str:
    # TODO Currently, there are two services, I'm uncertain which one matters
    return get_service_status('vncserver-virtuald')
    # return get_service_status('vncserver-x11-systemd')


def generate_general_request() -> dict:
    """
    Returns fields needed for request.

    Returns:
        dict: dictionary of field(s).
    """
    available, int_name, ip = select_interface(get_interfaces())
    if not available:  # can't send message
        # raise exceptiontype maybe?
        sys.exit(1)  # TODO there should *maybe* be logging here...

    mac = get_mac(int_name)
    fields = {
                'ip': ip,
                'mac': mac,
             }

    ssid, status = CSM_getssid.get_ssid(int_name)
    if status:  # ensures ssid available for interface
        fields['ssid'] = ssid
    fields['ssh'] = get_ssh_status()
    fields['vnc'] = get_vnc_status()

    return fields


def get_id_fields() -> dict:
    """
    Return dev and hardware IDs

    Returns:
        dict: dictionary with fields {'hwid': hwid, 'devid': devid}
    """
    hwid = CSM_get_hw_id.get_hw_id()
    devid = CSM_get_dev_id.get_dev_id()
    return {'hwid': hwid, 'devid': devid}


def load_request(request_path: Path) -> str:
    """
    Load request JSON file as string.
    If file read fails, a blank string is returned.

    Args:
        request_path (Path): path to a file with a json request.

    Returns:
        str: file contents.
    """
    try:
        with open(request_path) as f:
            return f.read()
    except:
        return ''


def save_request(request_path: Path, request: str):
    """
    Save request JSON file.
    If file open/save fails, the failure is ignored as it is not critical.

    Args:
        request_path (Path): path to a file with a json request.
    """
    try:
        with open(request_path, "w") as f:
            f.write(request)
    except:
        pass  # TODO log the event


def send_request(api_url: str, request) -> Optional[HTTPResponse]:
    """
    Sends a POST request with JSON data to the specified url.

    Args:
        api_url (str): url to the target for the post request.
        request: Anything that json.dumps(request) can convert to a JSON string.

    Returns:
        Optional[HTTPResponse]: None if request fails for any reason, otherwise, returns the response from the server.
    """
    req_json = json.dumps(request).encode('utf-8')
    req = urllib.request.Request(api_url, data=req_json)
    req.add_header('Content-Type', 'application/json')
    try:
        ctxt = ssl.create_default_context()
        resp = urllib.request.urlopen(req, context=ctxt)
        return resp
    except(urllib.error.URLError):
        # TODO handle error better? as in, better logging
        return None


def parse_commandline(*args) -> (bool, bool):
    """
    Parse the command line and return flags, just two at the moment.
    Returns:
        bool: shutdown_request. Implies force_request.
        bool: force_request. Forces request to be sent without comparing last update.
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
    """
    Args:
        args (list): normal commandline arguments minus script name
    """
    CSM_ROOT = Path('/var/opt/autopi/')
    OLD_REQ = CSM_ROOT / 'old_request.json'
    API_URL = 'http://localhost:8000/'  # TODO retarget API URL

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
    resp = send_request(API_URL, request)
    if resp:
        print(resp.status)
        print(resp.readlines())
    else:
        print("Connection failed")


if __name__ == '__main__':
    main(*sys.argv[1:])
