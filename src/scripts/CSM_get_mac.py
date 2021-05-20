#!/usr/bin/env python3
import sys
import netifaces


def getMAC():
    input_bool = False
    if len(sys.argv) == 1:
        while not input_bool:
            connection = input("What is your connection type? (ethernet, wireless)\n")
            c_type, input_bool = determine_c_type(connection, input_bool)
    else:
        c_type = sys.argv[1]
    try:
            # str = open('/sys/class/net/'+c_type+'/address').read()
            str = netifaces.ifaddresses(c_type)[netifaces.AF_LINK][0]['addr']
    except:
        print("Error")
        sys.exit(1)
    return str[0:17]


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
if __name__ == "__main__":
    print(getMAC())
