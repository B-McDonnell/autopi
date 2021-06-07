# Implementation
N/A.

# Dependencies
- Uses `/proc/cpuinfo` to generate a hardware ID. Requires the last four lines of `/proc/cpuinfo` to be static.
- Uses `service` command

# Technical considerations
Currently, `get_hw_info` does not validate that the data it uses is permanent and identifying. If a system does not have permanent identifying information in the last four lines of `/proc/cpuinfo`, a different source must be used.
