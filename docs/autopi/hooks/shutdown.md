# Overview
This service generates a `shutdown` event requests on system shutdown. It triggers on `shutdown.target`.

# Detailed notes
`Before=...` specifies the service should be completed before the specified services.
`Type=oneshot` specifies that the service should be run to completion.
`ExecStart=...` contains the actual command to execute.
`TimeoutStartSec=...` prevents the service from hanging too long and stopping shutdown.
