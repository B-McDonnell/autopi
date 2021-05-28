#!/usr/bin/env python3
"""Get hardware id."""

from hashlib import sha256


def get_hw_info() -> list:
    """Return 4 lines of cpu serial and hardware data."""
    with open("/proc/cpuinfo") as f:
        lines = f.readlines()
    return lines[-4:]


def get_hw_id() -> str:
    """Return standard hardware ID hashed from the last 4 lines of /proc/cpuinfo."""
    info_lines = get_hw_info()
    raw = "".join(info_lines).encode("utf-8")
    return sha256(raw).hexdigest()


if __name__ == "__main__":
    print(get_hw_id())
