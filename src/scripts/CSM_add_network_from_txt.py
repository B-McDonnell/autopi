#!/usr/bin/env python3

import subprocess

# on boot, run this, then rewrite file in format...
# sudo sh -c "printf '%s\n' '#No space after (=).' '#Priority is an int value 1,2, or 3 (3 being prioritized the most).' '#If no password/priority, leave empty.' '' 'ssid=' 'password=' 'priority=' > /boot/CSM_new_network.txt"

f = open("/boot/CSM_new_network.txt", "r")
# Look for format:
#
# ssid=
# password=
# priority=
#
#
list_of_lists = [(line.strip()).split() for line in f]
ssid = list_of_lists[0][0].split("=")
password = list_of_lists[1][0].split("=")
priority = list_of_lists[2][0].split("=")
passsword_bool = False
priority_bool = False
items = ["CSM_add_network"]
if len(ssid) > 1:
    ssid = ssid[1]
if len(priority) > 1:
    items.append("--priority")
    items.append(priority[1])
    priority_bool = True

if len(password) > 1:
    password_bool = True
    items.append("-p")
    items.append(password[1])
else:
    items.append("-n")
items.append(ssid)

if priority_bool and passsword_bool and len(ssid) > 0:
    subprocess.run(items)

else:
    print("None")
f.close()