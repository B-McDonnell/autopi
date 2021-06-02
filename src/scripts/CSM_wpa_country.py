#!/usr/bin/env python3
"""Manage the country code in a WPA config file."""

import argparse
import os
import subprocess
import sys


def run_reconfigure() -> bool:
    """Use wpa_cli to reconfigure wpa. Exits program if wpa_cli fails."""
    try:
        response = subprocess.run(
            ["wpa_cli", "-i", "wlan0", "reconfigure"], check=True, capture_output=True
        )
        if response.stdout != b"OK\n":
            print("wpa_cli reconfiguration failed", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(
            f"\"{' '.join(e.cmd)}\" returned non-zero exit status {e.returncode}",
            end="",
        )
        if len(e.output) > 0:
            print(f": {e.output}")
        else:
            print()
        sys.exit(1)


def get_country(config_file: str):
    """Get the country code in config_file. Exit with status 1 if not found."""
    with open(config_file, "r") as fin:
        # get country
        lines = [line.strip() for line in fin.readlines()]
        for line in lines:
            if line.startswith("country="):
                print(line.split("=")[1])
                sys.exit(0)

        # country was not found
        sys.exit(1)


def update_country(config_file: str, country: str):
    """Change the country code in config_file to country."""
    # separate header and contents
    header = []
    contents = []
    with open(config_file, "r") as fin:
        line = fin.readline()
        while line:
            if line.strip().startswith("network={"):
                contents.append(line)
                break
            header.append(line)

            line = fin.readline()
        contents.extend(fin.readlines())

    # strip trailing empty lines from header
    while len(header) > 0 and header[-1].isspace():
        header.pop(-1)

    # if country exists, update it
    country_exists = False
    for i, line in enumerate(header):
        if line.strip().startswith("country="):
            line = line.replace(line.split("=")[1], country, 1)
            header.pop(i)
            header.insert(i, line)
            country_exists = True
            break
    # else, add it
    if not country_exists:
        header.append(f"country={country}")
    header.append("\n\n")

    with open(config_file, "w") as fout:
        fout.writelines(header + contents)


def main():
    parser = argparse.ArgumentParser()

    shared_parser = argparse.ArgumentParser(add_help=False)

    subparsers = parser.add_subparsers(
        dest="subparser", required=True, title="subcommands", metavar="(get | update)"
    )
    shared_parser.add_argument(
        "FILENAME",
        nargs="?",
        help="path to configuration file. Fails if file not not exist. Uses /etc/wpa_supplicant/wpa_supplicant.conf by default",
        default="/etc/wpa_supplicant/wpa_supplicant.conf",
    )

    get_parser = subparsers.add_parser(
        "get",
        help="get the current country code. Fails if country code does not exist",
        parents=[shared_parser],
    )
    update_parser = subparsers.add_parser(
        "update", help="change the current country code", parents=[shared_parser]
    )
    update_parser.add_argument("COUNTRY_CODE", help="ISO 3166-1 country code")

    args = parser.parse_args()

    if not os.path.isfile(os.path.abspath(args.FILENAME)):
        print(f'"{args.FILENAME}" is not a valid file', file=sys.stderr)
        sys.exit(1)

    if args.subparser == "get":
        get_country(args.FILENAME)
    elif args.subparser == "update":
        update_country(args.FILENAME, args.COUNTRY_CODE)


if __name__ == "__main__":
    main()
