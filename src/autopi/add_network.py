#!/usr/bin/env python3
"""Add a network to autoconnect to."""

import argparse
import subprocess
import sys
from dataclasses import dataclass

from util import wpa_interface as wpa
from util.config import Config


@dataclass
class _Args:
    ssid: str
    std_out: bool
    dry_run: bool
    config_file: str
    priority: int
    password: str
    interface: str


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("SSID", type=str, help="SSID of the network")
    parser.add_argument(
        "-o",
        "--std-out",
        action="store_true",
        help="write network configuration to stdout",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="do not update network configuration. --std-out is assumed",
    )
    parser.add_argument(
        "-f",
        "--config-file",
        type=str,
        required=False,
        help=f"path to the configuration file. Only for advanced users. Defaults to {Config.WPA_CONFIG_FILE}",
        default=Config.WPA_CONFIG_FILE,
    )
    parser.add_argument(
        "--priority",
        type=int,
        help="priority level for the network. Networks with a higher priority network will be joined first",
    )
    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        default=Config.DEFAULT_WIRELESS_INTERFACE,
        help=f"interface to add network to. Defaults to {Config.DEFAULT_WIRELESS_INTERFACE}",
    )

    pass_group = parser.add_mutually_exclusive_group(required=True)
    pass_group.add_argument(
        "-n",
        "--no-password",
        action="store_true",
        help="network does not require a password",
    )
    pass_group.add_argument(
        "-p",
        "--password",
        type=str,
        required=False,
        help="password for network. If not specified, will read from stdin",
    )
    args = parser.parse_args()

    return _Args(
        args.SSID,
        args.std_out,
        args.dry_run,
        args.config_file,
        args.priority,
        None if args.no_password else args.password,
        args.interface,
    )


def main():
    """Add network from command line arguments."""
    cli_args = _parse_args()

    try:
        new_network = wpa.make_network(
            cli_args.ssid, cli_args.password, cli_args.priority
        )
    except (RuntimeError, subprocess.CalledProcessError) as e:
        # TODO: log error
        print(e, file=sys.stderr)
        sys.exit(1)

    if cli_args.std_out or cli_args.dry_run:
        print(new_network)
        if cli_args.dry_run:
            return

    try:
        wpa.add_network(new_network, cli_args.config_file)
    except FileNotFoundError as e:
        # TODO: log error
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        wpa.run_reconfigure(cli_args.interface)
    except subprocess.CalledProcessError as e:
        # TODO: log error
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
