#!/usr/bin/env python3

"""Add network via .txt file."""

from io import TextIOWrapper

import util.wpa_interface as wpa
from util.config import Config

# TODO: get default file from config dir
# on boot, run this, then rewrite file in format...
# sudo sh -c "printf '%s\n' '#No space after (=).' '#Priority is an int value 1,2, or 3 (3 being prioritized the most).' '#If no password/priority, leave empty or delete line.' '#This file will be reset after network is added.' 'ssid=' 'password=' 'priority=' > /boot/CSM_new_network.txt"

# Look for format:
#
# ssid=
# password=
# priority=
#
#


def get_dict(f: TextIOWrapper) -> dict:
    """Create dictionary of passed in file contents.

    Only includes values in the format `key=value` where `value` is not empty. Excludes comments ('#').

    Args:
        f (TextIOWrapper): Text file including network info.

    Returns:
        dict: Dictionary set up with (field, input) Ie. ('ssid', 'CSMwireless').
    """
    d = {}
    for line in f:
        if line.lstrip().startswith("#"):
            continue
        values = list(filter(None, line.strip().split("=")))
        if len(values) > 1:
            key, *val = values
            d[key] = "=".join(val)
    return d


def main():
    """Perform main action and call helper functions."""
    with open(Config.NEW_NETWORK_FILE, "r") as fin:
        d = get_dict(fin)
    if "ssid" not in d:
        # TODO: log
        return

    wpa.add_network(
        network_config=wpa.make_network(
            ssid=d["ssid"],
            passwd=d["password"] if "password" in d else None,
            priority=d["priority"] if "priority" in d else None,
        )
    )


if __name__ == "__main__":
    main()
