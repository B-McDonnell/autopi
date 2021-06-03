"""Utilities to retrieve network information."""

import subprocess

import netifaces


def getMAC(interface: str) -> str:
    """Return MAC address using network interface as a parameter.

    Args:
        interface (str): Interface (i.e. wlan0 or eth0).

    Returns:
        str: MAC address.
    """
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
    except Exception as e:
        raise RuntimeError("MAC address could not be found") from e


def get_interface_ip(interface: str):
    """Get the IP address linked to an interface."""
    if interface not in netifaces.interfaces():
        return "", False
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
        ipinfo = addrs[netifaces.AF_INET][0]
        return ipinfo["addr"], True
    return "", False


def is_wireless_active(interface: str) -> bool:
    """Check if the interface is an active wireless interface.

    Internally uses iwconfig return code to determine if the interface is wireless.

    Args:
        interface (str): the name of an interface.

    Returns:
        bool: Interface is wireless and active.
    """
    try:
        result = subprocess.run(["iwconfig", interface], capture_output=True)
    except FileNotFoundError:
        # TODO Probably log this
        return "", False  # iwconfig not present
    if result.returncode != 0:
        return False
    return True


def get_ssid(interface: str) -> (str, bool):
    """
    Get wireless SSID for specified interface.

    Args:
        interface (str): the name of an interface.

    Returns:
        str: ssid of the network interface.
        bool: status. If true, ssid was successfully obtained and returned in 'ssid', otherwise ssid is empty. If false interface nonexistent, interface is not wireless, or currently has no SSID.
    """
    try:
        result = subprocess.run(["iwgetid", interface, "-r"], capture_output=True)
    except FileNotFoundError:
        # TODO Probably log this
        return "", False  # iwgetid not present
    if result.returncode != 0:
        return "", False
    output_b = result.stdout
    output = output_b.decode("utf-8").strip()
    return output, len(output) > 0
