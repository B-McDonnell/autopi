#!/usr/bin/env python3
from pathlib import Path


def get_dev_id():
    """
    Returns device UUID as string
    """
    path = Path('/boot/CSM_device_id.txt')  # TODO should this change?
    with open(path) as f:
        lines = f.readlines()
    return ''.join(lines).strip()


if __name__ == "__main__":
    print(get_dev_id())
