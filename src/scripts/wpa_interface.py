"""An interface with wpa config files and commands."""

import subprocess
from pathlib import Path
from typing import Optional


class PasswordLengthException(RuntimeError):
    """Password does not meet wpa_password length requirements."""

    pass


class SSIDLengthException(RuntimeError):
    """SSID has an invalid length."""

    pass


def _make_network_with_passwd(ssid: str, passphrase: str) -> str:
    """Create an encrypted network config information for an ssid/passphrase pair.

    Args:
        ssid (str): ssid name of the network.
        passphrase (str): password of the network.

    Raises:
        SSIDLengthException: ssid is too long.
        PasswordLengthException: password does not meet wpa length requirements.
        subprocess.CalledProcessError: wpa_passphrase failed.

    Returns:
        str: wpa network configuration.
    """
    if len(ssid) > 32:
        raise SSIDLengthException("SSID must be less than or equal to 32 characters")
    if len(passphrase) < 8 or len(passphrase) > 63:
        raise PasswordLengthException(
            "Passphrase must be from 8 to 63 characters (inclusive)"
        )
    result = subprocess.run(
        ["wpa_passphrase", ssid, passphrase], capture_output=True, check=True
    )
    return str(result.stdout, encoding="utf8")


def _make_network_without_passwd(ssid: str) -> str:
    """Generate a wpa network config for an unprotected network.

    Args:
        ssid (str): ssid of the network.

    Returns:
        str: generated network config.
    """
    config = "network={\n"
    config += f'\tssid="{ssid}"\n'
    config += "\tkey_mgmt=NONE\n"
    config += "}\n"
    return config


def _add_priority(network_config: str, priority: int) -> str:
    """Add a priority level to a wpa network config.

    Args:
        network_config (str): wpa network config to modify.
        priority (int): priority level.

    Returns:
        str: modified wpa network config.
    """
    lines = network_config.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "}":
            closing_index = i
    lines.insert(closing_index, f"\tpriority={priority}")
    return "\n".join(lines)


def _strip_comment_lines(network_config: str) -> str:
    """Remove any lines starting with '#'.

    Args:
        network_config (str): config to remove comments from.

    Returns:
        str: config with commented lines removed.
    """
    lines = network_config.split("\n")
    commentless_lines = [line for line in lines if not line.strip().startswith("#")]
    return "\n".join(commentless_lines)


def network_exists(
    network_config: str,
    config_file: str,
    ignore_comments: bool = True,
    ignore_empty_lines: bool = True,
) -> bool:
    """Check if network config already exists in a wpa config file.

    Args:
        network_config (str): network config to check for
        config_file (str): wpa config to check in
        ignore_comments (bool, optional): exclude lines starting with '#' from the check. Defaults to True.
        ignore_empty_lines (bool, optional): exclude empty lines from the check. Defaults to True.

    Raises:
        ValueError: config_file is not a valid file

    Returns:
        bool: network already exists in the config
    """
    if not Path(config_file).absolute().is_file():
        raise ValueError("config file path is not a valid file")
    with open(config_file, "r") as config_file:
        current_contents = config_file.read()

    if ignore_comments:
        current_contents = _strip_comment_lines(current_contents)
        network_config = _strip_comment_lines(network_config)

    if ignore_empty_lines:
        current_contents = "\n".join(
            [
                line
                for line in current_contents.splitlines()
                if len(line) > 0 and not line.isspace()
            ]
        )
        network_config = "\n".join(
            [
                line
                for line in network_config.splitlines()
                if len(line) > 0 and not line.isspace()
            ]
        )

    return network_config in current_contents


def make_network(
    ssid: str,
    passwd: Optional[str] = None,
    priority: Optional[int] = None,
    drop_comments: bool = True,
) -> str:
    """Create a new wpa network string.

    Args:
        ssid (str): ssid of the network
        passwd (str | None, optional): password of the network. If None, network without password protection is assumed. Defaults to None.
        priority (int | None, optional): priority of the network. Defaults to None.
        drop_comments (bool, optional): do not include comments generated by wpa_passphrase. Defaults to True.

    Returns:
        str: new wpa network string
    """
    network_str = (
        _make_network_with_passwd(ssid, passwd)
        if passwd is not None
        else _make_network_without_passwd(ssid)
    )
    if priority is not None:
        network_str = _add_priority(network_str, priority)

    return network_str


def add_network(
    network_config: str, config_file: str, drop_comments: bool = True
) -> bool:
    """Add a new network config to a wpa config file.

    Args:
        network_config (str): network config to add
        config_file (str): filename of wpa cconfig file
        drop_comments (bool, optional): remove any comments before adding to config. Defaults to True.

    Raises:
        ValueError: config_file is not a valid file.

    Returns:
        bool: config was succesfully added. Returns False if network config already exists.
    """
    if not Path(config_file).absolute().is_file():
        raise ValueError("config file path is not a valid file")

    if network_exists:
        return False

    with open(config_file, "a") as fout:
        fout.write(network_config)
    return True


def run_reconfigure(interface: Optional[str]) -> bool:
    """Use wpa_cli to force wpa_supplicant to re-read its config file.

    Args:
        interface (str | None): interface to reconfigure. Reconfigures all interfaces if None.

    Returns:
        bool: wpa_supplicant was successfully reconfigured.

    Raises:
        subprocess.CalledProcessError: wpa_cli's reconfigure failed.
    """
    command = ["wpa_cli"]
    if interface is not None:
        command.extend(["-i", interface])
    command.append("reconfigure")
    response = subprocess.run(command, check=True, capture_output=True)
    if response.stdout != b"OK\n":
        return False
