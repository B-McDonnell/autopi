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
There are two required setup steps. First, the Raspberry Pi must have its MAC address registered with the school so it can connect to the internet on `CSMwireless`. Second, the Raspberry Pi must be registered with the IP/Status discovery system. This registration can only occur once the Raspberry Pi is connected to the network (i.e. has performed network registration).

Custom networks can also be added to the Raspberry Pi.


### Device and MAC Registration
1. Insert the SD card into the Raspberry Pi.
2. Plug in the Raspberry Pi, lights will turn on.
3. Wait for 2 minutes.
4. Unplug the Raspberry Pi.
5. Remove the SD card from Raspberry Pi.
6. Insert SD card into your computer.
7. Open the SD card drive on your file explorer (named `boot`).
8. Open the file `CSM_mac_address.txt`.
9. Go to `netreg.mines.edu` while connected to `CSMwireless`.
10. Agree to the terms and conditions.
11. On the next page, enter the MAC address from the file in step 7.
12. Enter the rest of your information and click register.
13. The Raspberry Pi's MAC address is now registered.
14. The Raspberry Pi will be able to access internet in up to 5 minutes, meanwhile, continue steps.
15. Reopen the SD card drive on your file explorer (named `boot`).
16. Open the file `CSM_device_id.txt`.
17. Go to `https://autopi.mines.edu/`. 
18. Login with your Mines MultiPass.
19. Click `Register` at the top of the page.
20. Copy the `ID` into the file opened in step 3.
21. Save an close the close file.
22. Eject the SD card and plug it into the Raspberry Pi.
23. Plug in the Raspberry Pi, lights will turn on.
24. See *Get IP/status information* to confirm successful registration. 
25. To add additional networks, see *Home Network Registration* procedure.

### Home Network Registration
There are two methods for adding a Home network to the Raspberry Pi.
- If you can SSH into Raspberry Pi:
  1. Type `CSM_add_home_network` into a terminal window on the Raspberry Pi.
  2. Follow the prompts and enter network information.
  3. Once completed, network settings will reconfigure.

- If you *cannot* SSH into the Raspberry Pi:
  1. Insert SD card into your computer.
  2. Open the SD card drive on your file explorer (named `boot`).
  3. Find file `CSM_new_network.txt`.
  4. Read comments and fill out listed fields.
  5. Eject SD card from your computer.
  6. Insert SD card into Raspberry Pi.
  7. Turn on Raspberry Pi, and network settings will reconfigure.
  8. `CSM_new_network.txt` will be reset to blank parameters for adding additional networks.

## Get IP/status information
In order to see the IP and status information for the Raspberry Pi, do the following:
1. Go to `https://autopi.mines.edu/`. 
2. Login with your Mines MultiPass.
3. Your registered Raspberry Pi will be displayed with all corresponding IP, network, and status information.
   If you have multiple Raspberry Pi's, they will all be displayed.
4. Refresh page for status changes.
5. Note that Raspberry Pis highlighted in yellow are off or cannot be contacted for some other reason. If this occurs, try      restarting the Raspberry Pi.

## Common issues

# Development instructions
Run `pip3 install -r requirements.txt` and `pip3 install -r requirements-dev.txt`.
Run `pre-commit install`.
When `pre-commit` fails (and a hook states that files have changed), run `git add --update` to update the git staging area.
