#!/usr/bin/env python3
import sys

def getMAC():
    input_bool = False
    if len(sys.argv) == 1:
        while not input_bool:
            connection = input("What is your connection type? (ethernet, wireless)\n")
            c_type, input_bool = determine_c_type(connection, input_bool)
    else:
        new_c_string = sys.argv[1]
        c_type, input_bool = determine_c_type(new_c_string, input_bool)
        if not input_bool:
          print("Error entering connection type.")
          sys.exit(1)
        
    try:
            str = open('/sys/class/net/'+c_type+'/address').read()
    except:
        str = "00:00:00:00:00:00"
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
        
    
    
print(getMAC())
