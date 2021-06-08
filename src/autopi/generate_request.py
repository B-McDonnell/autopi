#!/usr/bin/env python3
"""This script generates IP discovery requests and send them as JSON via POST."""

import argparse
import json
import ssl
import sys
import urllib.request
from http.client import HTTPResponse
from pathlib import Path
from urllib.error import URLError

from util import config, device_info, network_info


def generate_shutdown_request() -> dict:
    """Get field(s) needed for the request, in this case: 'event: shutdown'.

    Returns:
        dict: Dictionary of field(s)
    """
    return {"event": "shutdown"}


def get_service_status(service: str) -> str:
    """Return a string to be used as the service status.

    Args:
        service (str): service name.

    Returns:
        str: service status.
    """
    b = device_info.is_service_up(service)
    return "up" if b else "down"


def _is_ssh_up() -> bool:
    """Check SSH service status."""
    return device_info.is_service_up("sshd")


def _is_vnc_up() -> bool:
    """Check VNC service status."""
    # TODO Currently, there are multiple services, I'm uncertain which one(s) matters
    return device_info.is_service_up("vncserver-x11-serviced")


def _get_interface() -> str:
    """Get connected interface.

    Raises:
        RuntimeError: no connected network interfaces

    Returns:
        str: interface name
    """
    connected_interfaces = list(
        filter(
            network_info.is_interface_connected,
            network_info.get_interfaces(),
        )
    )
    if len(connected_interfaces) == 0:
        raise RuntimeError("No connected network interfaces")
    default_interface = network_info.get_default_interface()
    return (
        connected_interfaces[0]
        if default_interface not in connected_interfaces
        else default_interface
    )


def get_network_fields(interface: str) -> dict:
    """Return network fields needed for request.

    Returns:
        dict: dictionary of field(s).

    Raises:
        RuntimeError: if no interface can be found
    """
    ip = network_info.get_interface_ip(interface)
    if ip is None:
        raise RuntimeError("Interface disconnected")

    mac = network_info.get_mac(interface)
    fields = {
        "ip": ip,
        "mac": mac,
    }

    ssid = network_info.get_ssid(interface)
    if ssid is not None:  # ensures ssid available for interface before adding it
        fields["ssid"] = ssid

    return fields


def get_service_fields() -> dict:
    """Return service fields needed for request.

    Returns:
        dict: dictionary of field(s).
    """
    return {
        "ssh": "up" if _is_ssh_up() else "down",
        "vnc": "up" if _is_vnc_up() else "down",
    }


def get_id_fields() -> dict:
    """Return dev and hardware IDs.

    Returns:
        dict: dictionary with fields {'hwid': hwid, 'devid': devid}
    """
    return {"hwid": device_info.get_hw_id(), "devid": device_info.get_dev_id()}


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
    # TODO: get path from config
    CSM_ROOT = Path("/var/opt/autopi/")
    REQ_PATH = CSM_ROOT / "old_request.json"

    info_fields = {}
    if event != "shutdown":
        info_fields = {**get_network_fields(_get_interface()), **get_service_fields()}

    try:
        if force:
            save_request(REQ_PATH, info_fields)
        else:
            # TODO: replace this implementation with a checksum
            # compare new request to previous
            old = load_request(REQ_PATH)
            if old == info_fields:
                info_fields = {}  # clear non-essential fields
                REQ_PATH.touch()
            else:
                save_request(REQ_PATH, info_fields)
    except OSError:
        # TODO probably log this
        pass

    request = get_id_fields()
    request["event"] = event
    request = {**request, **info_fields}
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


def generate_and_send_request(
    event: str = "general", force: bool = False, verbose: bool = False
):
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
    api_url = config.get_api_url()

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
    if event in ("shutdown", "start"):
        force_req = True

    verbose = result.verbose > 0

    return event, force_req, verbose


def main():
    """Catch exceptions."""
    try:
        generate_and_send_request(*parse_commandline())
    except RuntimeError as re:
        print(re)
        sys.exit(1)
    except URLError as ue:
        print("Connection failed:", ue)
        sys.exit(1)


if __name__ == "__main__":
    main()
