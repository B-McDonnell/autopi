#!/usr/bin/env python3
"""Manage the country code in a WPA config file."""

import argparse
import sys
from pathlib import Path

from util import wpa_interface as wpa
from util.config import Config


def main():
    """Get or update country in a wpa config from command line inputs."""
    parser = argparse.ArgumentParser()

    shared_parser = argparse.ArgumentParser(add_help=False)

    subparsers = parser.add_subparsers(dest="subparser", required=True, title="subcommands", metavar="(get | update)")
    shared_parser.add_argument(
        "FILENAME",
        nargs="?",
        help=f"path to configuration file. Fails if file not not exist. Defaults to {Config.WPA_CONFIG_FILE}",
        default=Config.WPA_CONFIG_FILE,
    )

    subparsers.add_parser(
        "get",
        help="get the current country code. Fails if country code does not exist",
        parents=[shared_parser],
    )
    update_parser = subparsers.add_parser("update", help="change the current country code", parents=[shared_parser])
    update_parser.add_argument("COUNTRY_CODE", help="ISO 3166-1 country code")

    args = parser.parse_args()

    if not Path(args.FILENAME).is_file():
        print(f'"{args.FILENAME}" is not a valid file', file=sys.stderr)
        sys.exit(1)

    if args.subparser == "get":
        country = wpa.get_country(args.FILENAME)
        if country is None:
            sys.exit(1)
        else:
            print(country)
    elif args.subparser == "update":
        wpa.update_country(args.COUNTRY_CODE, args.FILENAME)


if __name__ == "__main__":
    main()
