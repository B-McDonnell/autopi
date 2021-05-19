#!/usr/bin/env bash

print_usage () {
    echo "Usage: CSM_add_network [OPTION]... SSID [PASSWORD]"
    echo "Adds a new network to automatically connect to. Passwork information is encrypted."
    echo ""
    echo "--no-password    network has no password"
    echo "--std-out        output new config information to std_out"
    echo "--help           display this help and exit"
}

print_usage