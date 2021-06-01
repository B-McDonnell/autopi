# Overview
This service generates `start` event requests on system boot. Triggers on `multi-user` run level or higher. The service should not run until networking has started, after which the service will restart every 5 seconds until successfully sending a request. Waiting longer delays sending the `start` event, a shorter restart interval risks systemd killing the service because of too many restarts.

# Detailed notes
`Type=simple` specifies the recommended service type.
`After=...` should prevent the service from being triggered before the network is up, but it is not strictly necessary.
`ExecStart=...` contains the actual command to execute.
`Restart=on-failure` ensures that the event will restart if it failed.
`RestartSec=5` prevents the event from firing in too rapid succession. This is useful because, typically, if the request fails, networking needs to finish connecting.
