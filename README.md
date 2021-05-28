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


### Network MAC Registration
1. Connect the SD card.
2. Boot the Raspberry Pi.
3. Wait for TODO seconds.
4. Unplug the Raspberry Pi.
5. Remove the SD card and connect it to your computer.
6. Open the SD card drive.
7. Open the file `CSM_mac_address.txt`.
8. Go to `netreg.mines.edu` while connected `CSMwireless`.
9. Agree to the terms and conditions.
10. On the next page, enter the MAC address from the file in step 7.
11. Enter the rest of your information and click register.
12. The Raspberry Pi's MAC address is now registered. 

### Device Registration
1. Connect the SD card to your computer.
2. Open the SD card drive in file explorer.
3. Open the file `CSM_device_id.txt`
4. Connect to the web server at `https://SERVER.mines.edu/`. 
5. Login with multipass.
6. If you have not previously registered a Raspberry Pi, click `Register`.
7. Copy the `DEVID` into the file opened in step 3.
8. Save the file.
9. Eject the SD card and plug it into the Raspberry Pi.
10. Boot the Raspberry Pi. 
11. Device registration should be complete.

### Home Network Registration
There are two methods for adding a Home network to the RPi.
- The first method is as follows:
  1. Run `CSM_setup_home_network` on the RPi.
  2. Follow the prompts and enter network information.
  3. Once completed, network settings will reconfigure.

- Alternative method
  1. Insert SD card into Windows machine.
  2. Find file `CSM_new_network.txt`.
  3. Fill out listed fields.
  4. Remove SD card from Windows machine.
  5. Insert SD card into RPi.
  6. Boot RPi, network settings will reconfigure.
  7. `CSM_new_network.txt` will be reset to blank parameters.

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
