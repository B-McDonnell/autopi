# Usage
`CSM_generate_request [START | SHUTDOWN]`

If no argument is supplied, it will generate a general request, fetching network configuration and service status, if this request differs from the previous request, then it sends it as a POST request to the API target via HTTPS.
If START is supplied, it generates the same request as above, but it does not compare it to the prior request. This is intended to be used on system startup.
If SHUTDOWN is supplied, it generates a request with a shutdown event and sends it as a POST request without comparing to previous requests.

# Implementation
Requests are POST requests with JSON data. 
The fields take the following form, with all variables being strings:
- Present in all requests
    - `'hwid': HW_ID`
    - `'devid': DEVICE_ID`
- Present in shutdown request
    - `'event': 'shutdown'`
- Present in general request (`*_STATUS` fields are either 'up' or 'down')
    - `'ip': IP_ADDR`
    - `'ssid': SSID`
    - `'ssh': SSH_STATUS`
    - `'vnc': VNC_STATUS`
The overall structure of the JSON is:
```
{
    'field_name': VALUE,
    'field_name2': VALUE2,
    ...
}
```

The service statuses are obtained from the `service` command as follows: 
`SSH_STATUS` = `service sshd status`
`VNC_STATUS` = `service vncserver_virtuald status`

# Dependencies
- `netifaces`
- `CSM_getip`
- `CSM_getssid`
- `CSM_get_hw_id`
- `CSM_get_dev_id`
- `service SERVICE_NAME status`

# Technical considerations
The VNC service has multiple components, it is unclear which component(s) must be functioning to work or what to expect in the future.
