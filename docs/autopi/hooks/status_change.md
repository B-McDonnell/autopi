# Overview
These components together serve to generate an IP discovery `SERVICE_change` request when triggered.

# Components
`status_change@.timer`
`status_change@.service`
`ssh_override.conf`
`vnc_override.conf`

## Note on `status_change@.*`
These two files have an `@` symbol, signifying they should be 'instantiated'. To properly execute these units, the `@` must be followed with a string, in this case, either `ssh_change` or `vnc_change`. The supplies the particular event that should be used in the IP discovery request. This string is called the 'instance string'.

## `status_change@.timer`
When triggered, waits 3 seconds before triggering the service (`status_change@.service`).

### Detailed notes
`OnActiveSec=3s` will trigger the event 3 seconds after it is triggered with `start`.
`AccuracySec=1s` is necessary to enforce an expedient notification, be default, the trigger may be anwhere in a 1 minute window after the specified time.
`RemainAfterElapse=false` ensures that the timer can be started again, otherwise, it would have to be manually stopped.
By default, the timer will trigger a service with the same name (including the instance string)

## `status_change@.service`
The service file can be called directly, or by the timer. The timer needs the service file to be able to run a command. 

### Detailed notes
`Type=simple` specifies the recommended service type for timer triggered services.
`After=...` should prevent the service from being triggered before the network is up, but it is not strictly necessary.
`ExecStart=...` contains the actual command to execute. In this case, `%I` inserts the instance string into the command, specifying which event should be sent for IP discovery.

## `ssh_override.conf` and `vnc_override.conf`
These provide the override configuration necessary to inject hooks into their respective services. They are added `/etc/systemd/system/TARGET_SERVICE_UNIT.d/` where `TARGET_SERVICE_UNIT` is the actual service name of their respective unit. 

### Detailed notes
`OnFailure=...` runs a command every time the service fails.
`ExecStartPost=...` runs a command after service start. Note that this particular command triggers the timer instead of the service directly; this is because the status of the service is not yet set correctly, and the IP discovery request would erroneously report the service as down.
`ExecStopPost=...` runs a command after service stop. 
