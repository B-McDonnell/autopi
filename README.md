# Table of contents

# Installation instructions
## Build image


## Setup web server


## Migrate web server


# Usage instructions
## Setup
### Network Registration


### Device Registration
1. Connect the SD card to your computer.
2. Open the SD card drive in file explorer.
3. Open the file `CSM_device_id.txt`
4. Connect to the web server at `https://SERVER.mines.edu/`. 
5. Login with multipass.
6. If you have not previously registered a Raspberry Pi, click `Register`.
7. Copy the 'DEVID' into the file opened in step 3.
8. Save the file.
9. Eject the SD card and plug it into the Raspberry Pi.
10. Boot the Raspberry Pi. 
11. Device registration should be complete.

### Home Network Registration
There are two methods for adding a Home network to the RPi.
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
In order to see the IP and status information for the Raspberry Pi, do the following:
1. Connect to the web server at `https://SERVER.mines.edu/`. 
2. Login with multipass.
3. Your registered Raspberry Pi will be displayed with all corresponding IP, network, and status information.
   If you have multiple Raspberry Pi's, they will all be displayed.

## Common issues

# Development instructions
Run `pip3 install -r requirements.txt` and `pip3 install -r requirements-dev.txt`.
Run `pre-commit install`.
When `pre-commit` fails (and a hook states that files have changed), run `git add --update` to update the git staging area.
