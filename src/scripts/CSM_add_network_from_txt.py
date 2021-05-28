#!/usr/bin/env python3

import subprocess

# on boot, run this, then rewrite file in format...
# sudo sh -c "printf '%s\n' '#No space after (=).' '#Priority is an int value 1,2, or 3 (3 being prioritized the most).' '#If no password/priority, leave empty.' '#This file will be reset after network is added.' '' 'ssid=' 'password=' 'priority=' > /boot/CSM_new_network.txt"

f = open("/boot/CSM_new_network.txt", "r")
# Look for format:
#
# ssid=
# password=
# priority=
#
#

d = {}
for line in f:
    if not line.lstrip().startswith("#"):
        if len(line.strip().split("=")) > 1:
            (key, val) = line.strip().split("=")
            d[key] = val

items = ["CSM_add_network"]

if len(d.get("priority")) > 0:
    items.append("--priority")
    items.append(d.get("priority"))

if len(d.get("password")) > 0:
    items.append("-p")
    items.append(d.get("password"))
else:
    items.append("-n")
items.append(d.get("ssid"))

if len(d.get("ssid")) > 0:
    subprocess.run(items)


f.close()
