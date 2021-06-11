"""Utilities to retrieve network information."""

import subprocess
from ipaddress import ip_address
from typing import List, Optional, Tuple

import netifaces


def get_default_gateway() -> Tuple[str, str]:
    """Get the default IPv4 gateway (ip, interface) of the device.

    Returns:
        tuple[str, str]: tuple containing the ip and interface of the default gateway
    """
    return netifaces.gateways()["default"][netifaces.AF_INET]


def get_default_interface() -> str:
    """Get the default IPv4 interface of the device.

    Returns:
        str: the interface of the default gateway
    """
    return get_default_gateway()[0]


def get_interfaces(exclude_loopback: bool = True) -> List[str]:
    """Obtain a list of available interfaces.

    Args:
        exclude_loopback (bool): exclude interfaces with an ip address in the range reserved for loopbacks

    Returns:
        list[str]: list of interface name strings
    """
    ref_ifaces = netifaces.interfaces()
    up_ifaces = (x for x in ref_ifaces if get_interface_ip(x) is not None)
    if not exclude_loopback:
        return list(up_ifaces)
    return [x for x in up_ifaces if not ip_address(get_interface_ip(x)).is_loopback]


def get_mac(interface: str) -> str:
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


def is_interface(interface: str) -> bool:
    """Check if a string is a network interface on the system."""
    return interface in netifaces.interfaces()


def is_interface_connected(interface: str) -> bool:
    """Check if interface is connected to a network."""
    return get_interface_ip(interface) is not None


def get_interface_ip(interface: str) -> Optional[str]:
    """Get the IP address linked to an interface."""
    if interface not in netifaces.interfaces():
        return None
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
        ipinfo = addrs[netifaces.AF_INET][0]  # TODO account for multiple addresses
        return ipinfo["addr"]
    return None


def is_wireless_active(interface: str) -> bool:
    """Check if the interface is an active wireless interface.

    Internally uses iwconfig return code to determine if the interface is wireless.

    Args:
        interface (str): the name of an interface.

    Returns:
        bool: Interface is wireless and active.
    """
    try:
        result = subprocess.run(
            ["iwconfig", interface], capture_output=True, check=False
        )
    except FileNotFoundError:
        # TODO Probably log this
        return "", False  # iwconfig not present
    return result.returncode == 0


def get_ssid(interface: str) -> Optional[str]:
    """
    Get wireless SSID for specified interface.

    Args:
        interface (str): the name of an interface.

    Returns:
        str | None: ssid of the network interface. If the interface cannot be obtained, False
    """
    try:
        result = subprocess.run(
            ["iwgetid", interface, "-r"], capture_output=True, check=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        # TODO Log this
        return None
    output = result.stdout.decode("utf-8").strip()
    return output if len(output) > 0 else None
