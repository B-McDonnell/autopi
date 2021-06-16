# Raspberry Pi-side

## Logging
The only logging present on the RPi are builtins when using, for example, `systemd` units that log automatically. Errors, warnings, etc and not logged.

## Multiple IP addresses per interface
It is possible to have multiple functional IP addresses on a single IPv4 interface, each with different rules. This is a sufficiently rare situation (requires special configuration) that it was ignored in favor of the much simpler single-IP address system.

# Server-side

## User interaction
All content served to the users from the server is unidirectional; the server never gets anything back.

### Dismissing warnings
Perhaps the best use of user interaction would be the manual dismissal of warnings. This would force acknowledgement and would help ensure that the warning is actually seen before being deleted.

### Custom aliases
Currently, aliases are generated from a list of 228 adjectives and 50 nouns. While this helps identify the device, aliases could be even more effective if the users could name them something specific and memorable.

### Admin conttrols
If user interaction was possible, it would not be too difficult to extend some admin controls. For example, showing currently active users, clearing warnings, etc., all without SSH and manual SQL.