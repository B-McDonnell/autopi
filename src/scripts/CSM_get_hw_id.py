#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256


def get_hw_info():
    """
    Returns 4 lines of cpu serial and hardware data
    """
    path = Path('/proc/cpuinfo')
    with open(path) as f:
        lines=f.readlines()
    return lines[-4:]


def get_hw_id():
    """
    Returns standard hardware ID
    
    Implementation details:
    Uses a sha256 checksum of the last 4 lines of /proc/cpuinfo
    """
    info_lines = get_hw_info()
    raw = ''.join(info_lines).encode('utf-8')
    return sha256(raw).hexdigest()

if __name__ == "__main__":
    print(get_hw_id())
