# Overview
These components together generate IP discovery `keepalive` requests on 1 minute intervals. It will start automatically 3o seoncds after boot.

# Components
`periodic.timer`
`periodic.service`

## periodic.timer
Triggers 30 seconds after first boot. THen, every 60 seconds after that. WHen the timer triggers, the unit specified in the file (`periodic.service` in this case) is activated. It will be automatically started on multiuser or higher run levels.

### Detailed notes
`OnUnitActiveSec=60s` will trigger the event 60 seconds after the last activatation.
`Unit=...` specifies which unit to activate on timer interval.
`AccuracySec=1s` is necessary because of an apparent bug in systemd. By default, `AccuracySec` is one minute, and should allow a winodw of 1 minute to execute the service. The apparent bug is that, while the 1 minute window should specify a range of possible execution times to avoid too many services triggering at once, systemd always seems to execute the service exactly `AccuracySec` time after it should trigger. To get an actual 1 minute interval, you have to specify `AccuracySec`. In other words, the timer actually runs on a 1 minute + 1 second interval. Alternatively, `AccuracySec=1u` can also be specified, allowing only 1 microsecond of delay; however, it is unnecessary, and if the bug is ever fixed, would prevent it from being useful.

## periodic.service
The service file is necessary to provide the command for the timer to execute, because the timer can only trigger a unit file. It will generate a `keepalive` request.


### Detailed notes
`Type=simple` specifies the recommended service type for timer triggered services.
`After=...` should prevent the service from being triggered before the network is up, but it is not strictly necessary.
`ExecStart=...` contains the actual command to execute.
