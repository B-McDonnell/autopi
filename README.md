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
### Network Registration


### Device Registration


### Home Network Registration


## Get IP/status information


# Development instructions
Run `pip3 install -r requirements.txt` and `pip3 install -r requirements-dev.txt`.
Run `pre-commit install`.
When `pre-commit` fails (and a hook states that files have changed), run `git add --update` to update the git staging area.
