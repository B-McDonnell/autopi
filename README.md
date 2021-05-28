# Table of contents
The table of contents can be accessed from the dropdown menu to the left of `README.md`'s title.

# Installation instructions
## Build image
1. `cd /path/to/autopi/`
2. `chmod +x install`
3. `./install`
4. Remove autopi project: `cd ..; rm -rf autopi`


## Setup web server
TODO: will be done via Docker compose.
Server requirements: Docker, Docker Compose.

## Migrate web server
TODO: will be done via Docker volume management (the containers are ephemeral).


# Usage instructions
## Setup
There are two required setups steps. First, the Raspberry Pi must have its MAC address registered with the school so it can connect to the internet on `CSMwireless`. Second, the Raspberry Pi must be registered with the IP/Status discovery system. This registration can only occur once the Raspberry Pi is connected to the network (i.e. has performed network registration).

Custom networks can also be added to the Raspberry Pi.

### Network Registration


### Device Registration


### Home Network Registration


## Get IP/status information


# Development instructions
Run `pip3 install -r requirements.txt` and `pip3 install -r requirements-dev.txt`.
Run `pre-commit install`.
When `pre-commit` fails (and a hook states that files have changed), run `git add --update` to update the git staging area.
