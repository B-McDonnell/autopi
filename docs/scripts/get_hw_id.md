# Usage
`get_hw_id`

Returns a sha256 string serving as the hardware id. 

The function `get_hw_id()` in the script returns the same data.

# Implementation
- Description of technologies and how they were used as needed.
Internally, it reads from `/proc/cpuinfo`, takes the last 4 lines (containing the serial number and other data), sha256 hashes it, and returns the hash as a string.

# Dependencies
None

# Technical considerations
`/proc/cpuinfo` data should be the same for the lifetime of a single RasberryPi, and should only change when moving to a new device.
