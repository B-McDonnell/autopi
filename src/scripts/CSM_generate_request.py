#!/usr/bin/env python3
"""This script generates IP discovery requests and send them as JSON via POST."""

import argparse
import json
import ssl
import subprocess
import sys
import urllib.request
from http.client import HTTPResponse
from pathlib import Path
from urllib.error import URLError

import CSM_get_config
import CSM_get_dev_id
import CSM_get_hw_id
import CSM_get_mac
import CSM_getip
import CSM_getssid
import netifaces


def get_interfaces() -> list:
    """Obtain a list of available interfaces.

    Returns:
        list: list of interface name strings.
    """
    ref_ifaces = netifaces.interfaces()
    return [x for x in ref_ifaces if not x.startswith("lo")]


def connected_interfaces() -> list:
    """Get list of network connected interfaces.

    returns:
        list[str]: connected interface names.

    Raises:
        RuntimeError: if no interface is available
    """
    interfaces = get_interfaces()
    if len(interfaces) == 0:
        raise RuntimeError("No network interfaces") from None
    connected = []
    for i in interfaces:
        _, status = CSM_getip.get_interface_ip(i)
        if status:
            connected.append(i)
    return connected


def generate_shutdown_request() -> dict:
    """Get field(s) needed for the request, in this case: 'event: shutdown'.

    Returns:
        dict: Dictionary of field(s)
    """
    return {"event": "shutdown"}


def is_service_up(service: str) -> bool:
    """Return bool representing whether service is up.

    Obtains status from 'service sshd status' return code. The return codes are different per-service, but 0 should always imply UP. 0 => UP, not 0 => DOWN.

    Args:
        service (str): service name as in linux command 'service SERVICE_STR status'

    Returns:
        bool: up
    """
    result = subprocess.run(["service", service, "status"], capture_output=True)
    return result.returncode == 0


def get_service_status(service: str) -> str:
    """Return a string to be used as the service status.

    Args:
        service (str): service name.

    Returns:
        str: service status.
    """
    b = is_service_up(service)
    return "up" if b else "down"


def get_ssh_status() -> str:
    """Get SSH status as 'up' or 'down'."""
    return get_service_status("sshd")


def get_vnc_status() -> str:
    """Get VNC status as 'up' or 'down'."""
    # TODO Currently, there are multiple services, I'm uncertain which one(s) matters
    return get_service_status("vncserver-x11-serviced")


def generate_general_request() -> dict:
    """Return fields needed for request.

    Returns:
        dict: dictionary of field(s).

    Raises:
        RuntimeError: if no interface can be found
    """
    connected = connected_interfaces()
    if len(connected) == 0:
        raise RuntimeError("No connected network interfaces") from None
    selected_int = connected[0]
    if "wlan0" in connected:
        selected_int = "wlan0"
    ip, status = CSM_getip.get_interface_ip(selected_int)
    if not status:
        raise RuntimeError("Interface disconnected") from None

    mac = CSM_get_mac.getMAC(selected_int)
    fields = {
        "ip": ip,
        "mac": mac,
    }

    ssid, status = CSM_getssid.get_ssid(selected_int)
    if status:  # ensures ssid available for interface before adding it
        fields["ssid"] = ssid
    fields["ssh"] = get_ssh_status()
    fields["vnc"] = get_vnc_status()

    return fields


def get_id_fields() -> dict:
    """Return dev and hardware IDs.

    Returns:
        dict: dictionary with fields {'hwid': hwid, 'devid': devid}
    """
    hwid = CSM_get_hw_id.get_hw_id()
    devid = CSM_get_dev_id.get_dev_id()
    return {"hwid": hwid, "devid": devid}


def load_request(request_path: Path) -> dict:
    """Load request JSON file as string.

    If file read fails, a blank string is returned.

    Args:
        request_path (Path): path to a file with a json request.

    Returns:
        dict: parsed file JSON contents.

    Raises:
        OSError: file open/read failed
    """
    with open(request_path) as f:
        return json.load(f)


def save_request(request_path: Path, request: dict):
    """Save request JSON file.

    If file open/save fails, the failure is ignored as it is not critical.

    Args:
        request_path (Path): path to a file with a json request.
        request (dict): dictionary with data fields.

    Raises:
        OSError: file open/read failed
    """
    with open(request_path, "w") as f:
        f.write(json.dumps(request))


def generate_request(event: str, force: bool) -> dict:
    """Generate the data needed for the request.

    Args:
        event (str): the type of the event.
        force (bool): if true, the non-id/event-name fields will not be compared to the previous request, and will always be sent.

    Returns:
        dict: all the fields for the request.

    Raises:
        RuntimeError: if no network interface is connected to the network
    """
    CSM_ROOT = Path("/var/opt/autopi/")
    REQ_PATH = CSM_ROOT / "old_request.json"

    request_fields = {}
    if event != "shutdown":
        request_fields = generate_general_request()

    try:
        if force:
            save_request(REQ_PATH, request_fields)
        else:
            # compare new request to previous
            old = load_request(REQ_PATH)
            if old == request_fields:
                request_fields = {}  # clear
                REQ_PATH.touch()
            else:
                save_request(REQ_PATH, request_fields)
    except OSError:
        # TODO probably log this
        pass

    request = get_id_fields()
    request["event"] = event
    # perform union
    request = {**request, **request_fields}
    return request


def send_request(api_url: str, request) -> HTTPResponse:
    """Send a POST request with JSON data to the specified url.

    Args:
        api_url (str): url to the target for the post request.
        request: Anything that json.dumps(request) can convert to a JSON string.

    Returns:
        HTTPResponse: the response from the server.

    Raises:
        URLError on connection failure.
    """
    req_json = json.dumps(request).encode("utf-8")
    req = urllib.request.Request(api_url, data=req_json)
    req.add_header("Content-Type", "application/json")
    ctxt = ssl.create_default_context()
    resp = urllib.request.urlopen(req, context=ctxt)
    return resp


def generate(event: str = "general", force: bool = False, verbose: bool = False):
    """Generate the specified request, compare it to previous request if applicable, and send it.

    Args:
        event (str):
        force (bool): force the request to be generated without comparing to previous request
        verbose (bool): show command output to stdout
        args (list): normal commandline arguments minus script name

    Raises:
        RuntimeError: if no network interface is connected to the network
        URLError: if the connection failed
    """
    # TODO get API URL from a configuration file/environment variable
    api_url = CSM_get_config.get_api_url()

    request = generate_request(event, force)
    resp = send_request(api_url, request)
    if verbose:
        print("----- POST Data ----")
        print(json.dumps(request, indent=4, sort_keys=True))
        print()
        print("----- Response -----")
        print("Response code:", resp.status)
        print("Response body:")
        print(b"".join(resp.readlines()).decode("utf-8"))


def parse_commandline() -> (str, bool, bool):
    """Parse the command line and return the appropriate arguments for generate.

    Returns:
        str: event type
        bool: force request to be sent without comparing last update.
        bool: verbose
    """
    parser = argparse.ArgumentParser(
        description="Generate a POST request for a given event."
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument(
        "type",
        choices=[
            "start",
            "shutdown",
            "keepalive",
            "net_update",
            "ssh_change",
            "vnc_change",
            "general",
        ],
        nargs="?",
        default="general",
    )
    result = parser.parse_args()

    # get the parameters
    event = result.type
    force_req = False
    if event == "shutdown" or event == "start":
        force_req = True

    verbose = result.verbose > 0

    return event, force_req, verbose

def main():
    try:
        generate(*parse_commandline())
    except RuntimeError as re:
        print(re)
        sys.exit(1)
    except URLError as ue:
        print("Connection failed:", ue)
        sys.exit(1)

if __name__ == "__main__":
    main()