#!/usr/bin/env python3
import sys
import netifaces


def getMAC(c_type) -> str:
    """Returns MAC address using network interface as a parameter.

    Args:
        c_type (str): Interface (wlan0 or eth0)

    Returns:
        str: MAC address
    """
    try:
        mac = netifaces.ifaddresses(c_type)[netifaces.AF_LINK][0]['addr']
    except:
        print("Error")
        sys.exit(1)
    return mac


def user_input() -> str:
    """Function to allow for user to input network interface.

    Returns:
        str: Network interface (wlan0 or eth0)
    """
    input_bool = False
    while not input_bool:
        connection = input(
            "What is your connection type? (ethernet, wireless)\n")
        if connection.lower() == 'ethernet':
            c_type = 'eth0'
            break
        elif connection.lower() == 'wifi' or connection.lower() == 'wireless':
            c_type = 'wlan0'
            break
    return c_type


def main() -> str:
    """If there is not an argument in the call, ask for user input.

    Returns:
        str: MAC address
    """
    if len(sys.argv) == 1:
        c_type = user_input()
    else:
        c_type = sys.argv[1]
    return getMAC(c_type)


if __name__ == "__main__":
    print(main())