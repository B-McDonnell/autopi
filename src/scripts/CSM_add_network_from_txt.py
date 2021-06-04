#!/usr/bin/env python3

"""Add network via .txt file."""

from io import TextIOWrapper

import scripts.wpa_interface as wpa

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
            d[key] = val
    return d


def main():
    """Perform main action and call helper functions."""
    with open("/boot/CSM_new_network.txt", "r") as fin:
        d = get_dict(fin)
    if not ("ssid" in d and not d["ssid"].empty()):
        return

    wpa.add_network(
        network_config=wpa.make_network(
            ssid=d["ssid"],
            passwd=d["password"]
            if "password" in d and not d["password"].empty()
            else None,
            priority=d["priority"]
            if "priority" in d and not d["priority"].empty()
            else None,
        ),
        config_file=wpa.get_default_wpa_config_file(),
    )


if __name__ == "__main__":
    main()
