#!/usr/bin/env bash

case $reason in
  BOUND | BOUND6 | CARRIER | IPV4LL | STATIC | RECONFIGURE)
    /home/pi/autopi/src/scripts/CSM_generate_request.py net_update # TODO maybe write to a log
    ;;
esac
