# Functionality
This script is executed on any `dhcpcd` event. For select events, the script will generate an IP discovery request with event `net_change`; otherwise, it ignores the event. 

# Implementation
It is installed to `/lib/dhcpcd/dhcpcd-hooks/`. This enables `dhcpcd` to trigger it. Raspberry Pi has 2 different DHCP services. The default is `dhcpcd`. `dhclient` is the other one that is installed. If `dhclient` is used instead, this script may work when added to `/etc/dhcp/dhclient-exit-hooks.d/`, but it has not been tested. 
The script name is prefixed with `99-`, because other scripts in `dhcpcd-hooks` have a numeric prefix; the docs do not, however, specify that the prefix is necessary. It appears, based on the execution script, that the prefixes have the effect of ordering the execution of the scripts; though this is not guaranteed anywhere.

The hook script does not need to have execute permissions configured.

# Dependencies
- `CSM_generate_request.py`
