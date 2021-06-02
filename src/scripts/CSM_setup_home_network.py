#!/usr/bin/env python3
"""Add a network from user input."""

import os
import subprocess
import sys

import CSM_wpa_country
import stdiomask


class HiddenPrints:
    """Hide output for updating country.

    https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
    """

    def __enter__(self):
        """Initialize hiding."""
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Revert to show prints."""
        sys.stdout.close()
        sys.stdout = self._original_stdout


def set_home_network():
    """Use user input, add a network."""
    items = ["CSM_add_network"]
    ssid = input("What is the name of your home network? (Case sensitive)\n")
    password_bool = False
    is_there_password = False
    while not password_bool:
        want_password = input("Does this network have a password? (y/n)\n")
        if want_password.lower() == "y":
            while True:
                password = stdiomask.getpass(
                    prompt="What is the password to this network? (It will be encrypted)\n"
                )
                password_reentered = stdiomask.getpass(prompt="Re-enter password.\n")
                if password == password_reentered:
                    password_bool = True
                    is_there_password = True
                    break
                else:
                    print("-" * 50)
                    print("Passwords do not match! Re-enter.")
                    print("-" * 50)
        elif want_password.lower() == "n":
            password = ""
            break
        else:
            print("-" * 50)
            print("Error! Re-enter input using (y/n)")
            print("-" * 50)
    want_priority = False
    p_bool = False
    while not p_bool:
        priority = input(
            "Would you like to set a priority of connecting to this network over MINES networks? (y/n)\n"
        )
        if priority.lower() == "n":
            p_bool = True
        elif priority.lower() == "y":
            want_priority = True
            items.append("--priority")
            p_bool = True

        else:
            print("-" * 50)
            print("Error! Re-enter input using (y/n)")
            print("-" * 50)
        while want_priority:
            priority_level = input(
                "Would you like low, medium, or high priority? (CSMwireless is set to medium)\n"
            )
            if priority_level.lower() == "low":
                priority = 1
                items.append(str(priority))
                break
            elif priority_level.lower() == "medium":
                priority = 2
                items.append(str(priority))
                break
            elif priority_level.lower() == "high":
                priority = 3
                items.append(str(priority))
                break
            else:
                print("-" * 50)
                print("Error! Re-enter input using (low, medium, high)")
                print("-" * 50)

    try:
        with HiddenPrints():
            CSM_wpa_country.get_country("/etc/wpa_supplicant/wpa_supplicant.conf")
    except SystemExit:
        CSM_wpa_country.update_country("/etc/wpa_supplicant/wpa_supplicant.conf", "US")
    if is_there_password:
        items.append("-p")
        items.append(password)
    else:
        items.append("-n")

    items.append(str(ssid))
    print()

    print("Adding network...")
    try:
        subprocess.run(items, check=True)
    except subprocess.CalledProcessError as e:
        print("\nAdding network failed:", e, file=sys.stderr)


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Permission Denied: Must be run as super user!")
        sys.exit(1)
    set_home_network()
