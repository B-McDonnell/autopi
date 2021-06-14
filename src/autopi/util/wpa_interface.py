"""An interface with wpa config files and commands."""

import itertools
import subprocess
from typing import Iterable, List, Optional


class PasswordLengthError(RuntimeError):
    """Password does not meet wpa_password length requirements."""

    __default_message: str = "Password length must be in 8..63 (inclusive)"

    def __init__(self, msg=__default_message, *args, **kwargs):
        """Set default message."""
        super().__init__(msg, *args, **kwargs)

    @property
    def constraint_msg(self) -> str:
        """Get password contraint message."""
        return self.__default_message


class SSIDLengthError(RuntimeError):
    """SSID has an invalid length."""

    __default_message: str = "SSID length must be in 1..32 (inclusive)"

    def __init__(self, msg=__default_message, *args, **kwargs):
        """Set default message."""
        super().__init__(msg, *args, **kwargs)

    @property
    def constraint_msg(self) -> str:
        """Get ssid contraint message."""
        return self.__default_message


def is_valid_ssid(ssid: str) -> bool:
    """Check if ssid is valid."""
    n = len(ssid)
    return 1 <= n <= 32


def is_valid_passwd(passwd: str) -> bool:
    """Check if wpa password is valid."""
    n = len(passwd)
    return 8 <= n <= 63


def get_default_wpa_config_file() -> str:
    """Get default wpa config file."""
    return "/etc/wpa_supplicant/wpa_supplicant.conf"  # TODO: get from config


def _make_network_with_passwd(ssid: str, passphrase: str) -> str:
    """Create an encrypted network config information for an ssid/passphrase pair.

    Args:
        ssid (str): ssid name of the network.
        passphrase (str): password of the network.

    Raises:
        SSIDLengthError: ssid is too long.
        PasswordLengthError: password does not meet wpa length requirements.
        subprocess.CalledProcessError: wpa_passphrase failed.

    Returns:
        str: wpa network configuration.
    """
    result = subprocess.run(["wpa_passphrase", ssid, passphrase], capture_output=True, check=True)
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
    lines = network_config.splitlines()
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
    lines = network_config.splitlines()
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
        OSError: config_file could not be opened.

    Returns:
        bool: network already exists in the config
    """
    with open(config_file, "r") as fin:
        current_contents = fin.read()

    if ignore_comments:
        current_contents = _strip_comment_lines(current_contents)
        network_config = _strip_comment_lines(network_config)

    if ignore_empty_lines:
        current_contents = "\n".join(
            [line for line in current_contents.splitlines() if len(line) > 0 and not line.isspace()]
        )
        network_config = "\n".join(
            [line for line in network_config.splitlines() if len(line) > 0 and not line.isspace()]
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
    if not is_valid_ssid(ssid):
        raise SSIDLengthError()
    if passwd is not None and not is_valid_passwd(passwd):
        raise PasswordLengthError()

    network_str = _make_network_with_passwd(ssid, passwd) if passwd is not None else _make_network_without_passwd(ssid)
    if drop_comments:
        network_str = _strip_comment_lines(network_str)
    if priority is not None:
        network_str = _add_priority(network_str, priority)

    return network_str


def add_network(network_config: str, config_file: str, drop_comments: bool = True) -> bool:
    """Add a new network config to a wpa config file.

    Args:
        network_config (str): network config to add
        config_file (str): filename of wpa config file
        drop_comments (bool, optional): remove any comments before adding to config. Defaults to True.

    Raises:
        OSError: config_file could not be opened.

    Returns:
        bool: config was succesfully added. Returns False if network config already exists.
    """
    if network_exists(network_config, config_file):
        return False

    if drop_comments:
        network_config = _strip_comment_lines(network_config)

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
    return response.stdout == b"OK\n"


def get_country(config_file: str) -> Optional[str]:
    """Get the country code from a wpa config file.

    Args:
        config_file (str): filename of wpa config file

    Raises:
        OSError: config_file could not be opened.

    Returns:
        str | None: country code from config_file or None if it does not exist
    """
    with open(config_file, "r") as fin:
        # get country
        for line in (line.strip() for line in fin.readlines()):
            if line.startswith("country="):
                return line.split("=")[1]

    # country was not found
    return None


def _split_config_file(config_file) -> (List[str], List[str]):
    with open(config_file, "r") as fin:
        lines = fin.readlines()

    def _not_network_line(line: str) -> bool:
        return not line.strip().startswith("network={")

    header = list(itertools.takewhile(_not_network_line, lines))
    contents = list(itertools.dropwhile(_not_network_line, lines))

    return header, contents


def _without_trailing_empty_lines(lines: List[str]) -> Iterable[str]:
    bad_indices = []
    last_index = len(lines) - 1
    for i, line in enumerate(reversed(lines)):
        if len(line) == 0 or line.isspace():
            bad_indices.append(last_index - i)
        else:
            break
    print(bad_indices)
    return (line for i, line in enumerate(lines) if i not in bad_indices)


def update_country(config_file: str, country: str):
    """Add or replace country code in a wpa config file.

    Undefined behavior may occur with a broken wpa config file.

    Args:
        config_file (str): filename of wpa config file
        country (str): country code to add or update to

    Raises:
        OSError: config_file is not a valid file
    """
    header, contents = _split_config_file(config_file)
    header = list(_without_trailing_empty_lines(header))

    country_code_index = next(
        (index for index, line in enumerate(header) if line.strip().startswith("country=")),
        None,
    )
    if country_code_index is not None:
        header[country_code_index] = f"country={country}\n"
    else:
        header.append(f"country={country}\n")
    header.append("\n")

    with open(config_file, "w") as fout:
        fout.writelines(header + contents)
