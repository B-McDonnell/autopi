#!/usr/bin/env python3
import sys
import netifaces


def getMAC(c_type):
    # pass in c_type as 'wlan0 or eth0"
    try:
        str = netifaces.ifaddresses(c_type)[netifaces.AF_LINK][0]['addr']
    except:
        print("Error")
        sys.exit(1)
    return str[0:17]


def user_input():
    input_bool = False
    while not input_bool:
        connection = input(
            "What is your connection type? (ethernet, wireless)\n")
        c_type, input_bool = determine_c_type(connection, input_bool)
    return c_type


def determine_c_type(input_string, input_bool):
    if input_string.lower() == 'ethernet':
        c_type = 'eth0'
        input_bool = True
    elif input_string.lower() == 'wifi' or input_string.lower() == 'wireless':
        c_type = 'wlan0'
        input_bool = True
    else:
        c_type = ''
    return c_type, input_bool


def main():
    if len(sys.argv) == 1:
        c_type = user_input()
    else:
        c_type = sys.argv[1]
    return getMAC(c_type)


if __name__ == "__main__":
    print(main())

