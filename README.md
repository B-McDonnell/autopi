# Table of contents

# Installation instructions
## Build image


## Setup web server


## Migrate web server


# Usage instructions
## Setup
### Network Registration


### Device Registration


### Home Network Registration
- There are two methods for adding a Home network to the RPi.
- The first method is as follows:
  1. Run CSM_setup_home_network on the RPi.
  2. Follow the prompts and enter network information.
  3. Once completed, network settings will reconfigure.

- Alternative method
  1. Insert SD card into Windows machine.
  2. Find file 'CSM_new_network.txt'.
  3. Fill out listed fields.
  4. Remove SD card from Windows machine.
  5. Insert SD card into RPi.
  6. Boot RPi, network settings will reconfigure.
  7. 'CSM_new_network.txt' will be reset to blank parameters.


## Get IP/status information


# Development instructions
Run `pip3 install -r requirements.txt` and `pip3 install -r requirements-dev.txt`.
Run `pre-commit install`.
When `pre-commit` fails (and a hook states that files have changed), run `git add --update` to update the git staging area.
