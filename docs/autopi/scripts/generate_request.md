# Usage
`generate_request.py [start | shutdown | keepalive | net_update | ssh_change | vnc_change | general] [-v]`

The first argument is the event type.
If `start` is supplied, it generates the same request as above, but it does not compare it to the prior request. This is intended to be used on system startup.
If `shutdown` is supplied, it generates a request with a shutdown event and sends it as a POST request without comparing to previous requests.
For any other event type, it will generate a general request, fetching network configuration and service status, if this request differs from the previous request, then it sends it as a POST request to the API target via HTTPS.
The default event type is `general`.
Add `-v` for verbose output. Prints the message, status returned, and reply.

# Implementation
Requests are POST requests with JSON data. 
The overall structure of the JSON is:
```json
{
    'hwid': 'sdflhagsdshslsha256sumghsalghs',
    'devid': 'abc123',
    'ip': '10.2.3.4',
    'ssid': 'mynet',
    'ssh': 'up',
    'vnc': 'down',
    'event': 'keepalive',
    ...
}
```
The fields take the following form, with all variables being strings:
- Present in all requests
    - `'hwid': HW_ID`
    - `'devid': DEVICE_ID`
- Present in shutdown request
    - `'event': 'shutdown'`
- Present in general request (`*_STATUS` fields are either 'up' or 'down')
    - `'ip': IP_ADDR`
    - `'ssid': SSID`; this field will not be here if ethernet is selected.
    - `'ssh': SSH_STATUS`
    - `'vnc': VNC_STATUS`
    - `'event': EVENT_TYPE`; the type is the event that triggered the request

`EVENT_TYPE` is one of: 
- `'shutdown'`; Raspberry Pi shutdown
- `'start'`; Raspberry Pi boot
- `'network_update'`; any change in network configuration
- `'ssh_change'`; ssh start/stop
- `'vnc_change'`; vnc start/stop

The service statuses are obtained from the `service` command as follows: 
`SSH_STATUS` = `service sshd status`
`VNC_STATUS` = `service vncserver_x11_serviced status`

# Dependencies
- `autopi.util.network_info`
- `autopi.util.device_info`
- `autopi.util.config`

# Technical considerations
The VNC service has multiple components, it is unclear which component(s) must be functioning to work or what to expect in the future.
