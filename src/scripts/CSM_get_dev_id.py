#!/usr/bin/env python3
r"""Get the device ID. ¯\_(ツ)_/¯."""


def get_dev_id() -> str:
    """Return device UUID as string."""
    with open("/boot/CSM_device_id.txt") as f:
        lines = f.readlines()
    return "".join(lines)


if __name__ == "__main__":
    print(get_dev_id())
