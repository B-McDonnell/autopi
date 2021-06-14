"""Utilities to retrieve network information."""

import subprocess
from ipaddress import ip_address
from typing import List, Optional, Tuple


import netifaces
import util.wpa_interface as wpa


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


def get_new_config_after_del(ssid: str, config_file: str) -> str:
    """Create new configuration after deletion.

    Args:
        ssid (str): SSID of network
        config_file (str): Fill path of network configuration

    Returns:
        str: Text of new configuration file
    """
    with open(config_file, "r") as fin:
        current_contents = fin.read()
        position = current_contents.find('ssid="' + ssid + '"')
        start = current_contents.rfind("\n\nnetwork={", 0, position)
        end = current_contents.find("}", position)
        new_config = current_contents[0:start] + current_contents[end + 1:]
        return new_config


def ssid_exists(ssid: str, config_file: str) -> bool:
    """Check to see if SSID exists in config.

    Args:
        ssid (str): SSID of network
        config_file (str): File path of network configuration

    Returns:
        bool: Exists
    """
    with open(config_file, "r") as fin:
        return f"ssid=\"{ssid}\"" in fin.read()


def check_duplicate_ssid(ssid: str, config_file: str) -> bool:
    """Check for multiple networks with same SSID.

    Args:
        ssid (str): SSID of network
        config_file (str): File path of network configuration

    Returns:
        bool: Multiple networks with same SSID
    """
    with open(config_file, "r") as fin:
        return fin.read().count('ssid="' + ssid + '"') > 1


def delete_ssid(ssid: str) -> bool:
    """Delete network after check if exists.

    Args:
        ssid (str): SSID to be deleted.

    Returns:
        bool: Deletion successful.
    """
    config_file = wpa.get_default_wpa_config_file()
    if ssid_exists(ssid, config_file):
        new_text = get_new_config_after_del(ssid, config_file)
        with open(config_file, "wt") as fin:
            fin.write(new_text)
            return True
    return False
