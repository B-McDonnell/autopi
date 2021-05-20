#!/usr/bin/env python3
import argparse
import sys
import subprocess


def wpa_passphrase(ssid: str, passphrase: str) -> str:
    """Create an encrypted network config information for an ssid/passphrase pair.

    Args:
        ssid (str): ssid name of the network.
        passphrase (str): password of the network.

    Raises:
        ValueError: passwork does not meet wpa length requirements.
        subprocess.CalledProcessError: wpa_passphrase failed.

    Returns:
        str: wpa network configuration.
    """
    if len(passphrase) < 8 or len(passphrase) > 63:
        raise ValueError(
            "Passphrase must be between 8 and 64 characters, inclusive")
    result = subprocess.run(
        ['wpa_passphrase', ssid, passphrase], capture_output=True, check=True)
    return str(result.stdout, encoding='utf8')


def strip_comment_lines(wpa_config: str) -> str:
    """Remove any lines starting with '#'.

    Args:
        wpa_config (str): config to remove comments from.

    Returns:
        str: config with commented lines removed.
    """
    lines = wpa_config.split('\n')
    commentless_lines = [
        line for line in lines if not line.strip().startswith('#')]
    return '\n'.join(commentless_lines)


def wpa_no_passphrase(ssid: str) -> str:
    """Generate a wpa network config for an unprotected network.

    Args:
        ssid (str): ssid of the network.

    Returns:
        str: generated network config.
    """
    config = 'network={\n'
    config += f'\tssid="{ssid}"\n'
    config += '\tkey_mgmt=NONE\n'
    config += '}\n'
    return config


def add_priority(wpa_config: str, priority: int) -> str:
    """Add a priority level to a wpa network config.

    Args:
        wpa_config (str): wpa network config to modify.
        priority (int): priority level.

    Returns:
        str: modified wpa network config.
    """
    lines = wpa_config.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == '}':
            closing_index = i
    lines.insert(closing_index, f'\tpriority={priority}')
    return '\n'.join(lines)


def add_country(config_filename: str, /, country: str):
    """Add country information to the wpa config file.

    Args:
        config_filename (str): path to the wpa config file
        country (str): ISO 3166-1 country code.
    """
    with open(config_filename, 'r') as fin:
        lines = fin.readlines()
    for line in lines:
        if line.strip().startswith('country'):
            return
    for i, line in enumerate(lines):
        if line.strip().startswith('network={') or i == len(lines) - 1:
            lines.insert(i, f'country={country}\n')
            break
    with open(config_filename, 'w') as fout:
        fout.writelines(lines)


def update_config(wpa_config: str, config_filename: str):
    """Update the wpa config file and reconfigure the network via wpa_cli.

    Args:
        wpa_config (str): wpa_network config to append to the wpa config.
        config_filename (str): path to wpa config.
    """
    with open(config_filename, 'a') as fout:
        fout.write(wpa_config)
    # subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'], check=True)


def main(args: argparse.ArgumentParser):
    # build base network config
    if not args.no_password:
        try:
            config = wpa_passphrase(args.SSID, args.password)
            config = strip_comment_lines(config)
        except subprocess.CalledProcessError as e:
            print(e.stdout, file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    else:
        config = wpa_no_passphrase(args.SSID)

    # add priority
    if args.priority:
        config = add_priority(config, args.priority)

    # update config or print network config
    if args.dry_run:
        print(config)
    else:
        if args.std_out:
            print(config)

        config_filename = '/etc/wpa_supplicant/wpa_supplicant.conf'
        add_country(config_filename, args.country)
        update_config(config, config_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("SSID", type=str, help="SSID of the network")
    parser.add_argument("-o", "--std-out", action="store_true",
                        help="write network configuration to stdout")
    parser.add_argument("--dry-run", action="store_true",
                        help="do not update network configuration. --std-out is assumed")
    parser.add_argument("--priority", type=int,
                        help="priority level for the network. Networks with a higher priority network will be joined first")
    parser.add_argument("-c", "--country", type=str, required=False, default="US",
                        help="ISO 3166-1 country code for network country. Defaults to US")
    auth_group = parser.add_argument_group()

    pass_group = parser.add_mutually_exclusive_group(required=True)
    pass_group.add_argument("-n", "--no-password", action="store_true",
                            help="network does not require a password")
    pass_group.add_argument("-p", "--password", type=str, required=False,
                            help="password for network. If not specified, will read from stdin")
    args = parser.parse_args()
    main(args)
