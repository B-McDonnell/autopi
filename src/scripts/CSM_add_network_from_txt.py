#!/usr/bin/env python3

"""Add network via .txt file."""

import subprocess
from io import TextIOWrapper

# on boot, run this, then rewrite file in format...
# sudo sh -c "printf '%s\n' '#No space after (=).' '#Priority is an int value 1,2, or 3 (3 being prioritized the most).' '#If no password/priority, leave empty.' '#This file will be reset after network is added.' 'ssid=' 'password=' 'priority=' > /boot/CSM_new_network.txt"

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
        if not line.lstrip().startswith("#"):
            values = list(filter(None, line.strip().split("=")))
            if len(values) > 1:
                (key, val) = values
                d[key] = val
    return d


def create_process(d: dict) -> list:
    """Create subprocess of adding new network.

    Args:
        d (dict): Dictionary set up with (field, input) Ie. ('ssid', 'CSMwireless').

    Returns:
        list: List of arguments for subprocess to run.
    """
    items = ["CSM_add_network"]
    if "priority" in d:
        items.append("--priority")
        items.append(d.get("priority"))

    if "password" in d:
        items.append("-p")
        items.append(d.get("password"))
    else:
        items.append("-n")
    items.append(d.get("ssid"))
    return items


def main():
    """Perform main action and call helper functions."""
    f = open("/boot/CSM_new_network.txt", "r")
    d = get_dict(f)
    items = create_process(d)
    if "ssid" in d:
        subprocess.run(items)
    f.close()


if __name__ == "__main__":
    main()
