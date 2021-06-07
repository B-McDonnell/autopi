#!/usr/bin/env bash

case $reason in
  BOUND | BOUND6 | CARRIER | IPV4LL | STATIC | RECONFIGURE)
    /usr/bin/CSM_generate_request net_update # TODO maybe write to a log
    ;;
esac
