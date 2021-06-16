# Table of contents
The table of contents can be accessed from the dropdown menu to the left of `README.md`'s title.

# Installation instructions
## Build image
1. `cd /path/to/autopi/`
2. `chmod +x install`
3. `./install`
4. Remove autopi project: `cd ..; rm -rf autopi`


## Setting up the web server
The server is managed by Docker Compose. 
While most of the server setup is internal to the container system and does not require setup on the host side, there are some important exceptions.

### Database password
Setting the database password requires two steps: creating the password file and updating `docker-compose.yaml` to the password file.

1. Add a strong unique password to a password file. This is, by default, `.db_password.secret`. For a random password, the following command can be run:

    `cat /dev/urandom | head --bytes 64 | sha256sum - | cut -d ' ' -f 1 | tee .db_password.secret`

2. If you used a password file other than  `.db_password.secret`, that must be changed in `docker-compose.yaml`. If the respository is managed by Git, add the file to `.gitignore` (`.gitignore` already contains `*.secret`):

    ```yaml
    secrets:
      db_password:
        file: your_file_here
      ```

An alternative strategy is to use [Docker Swarm](https://docs.docker.com/engine/swarm/secrets/) instead of Docker Compose, so that secrets are stored in a vault, can be rotated, et cetera, but this is not how this project was developed.

### Database backups
Database backups are managed by the [prodrigestivill/postgres-backup-local](https://hub.docker.com/r/prodrigestivill/postgres-backup-local) image.

Unlike other Docker data, the database backups are not kept in a named Docker volume, but instead in a bind mount. This prevents accidental backup deletion during Docker volume management (e.g. `docker-compose down --volume`) and can simplify remote backups if necessary.

The bind must be configured:

1. Create the directory. By default, `docker-compose.yaml` assumes `/var/opt/pgbackups` is used:

    `sudo mkdir -p /var/opt/pgbackups && sudo chown -R 999:999 /var/opt/pgbackups`

2. If you used a directory other than `/var/opt/pgbackups`, update `docker-compose.yaml`:

    ```yaml
    db_backup:
      volumes:
        - your_dir_here:/backups

Backup timings are set in the `db_backup.env` file. Currently, standard defaults are used:
 - backups are made daily
 - daily backups are kept 7 days
 - weekly backups are kept 4 weeks
 - monthly backups are kept 6 months

### TLS certificates
TODO

T

O

D

O

### Firewall rules
The only port that must be exposed is port `:443`. Only the `proxy` service exposes external ports, and it only accepts `https` traffic; all other traffic are in segmented internally managed networks that cannot be accessed from outside the Docker service stack.

## Migrating the web server
Migration is simple, as the Docker containers are ephemeral. Migrating each volume ensures the server state remains constant.

For each named volume (whcih can be found under the global `volumes` directive in `docker-compose.yaml`), follow the [official Docker documentation](https://docs.docker.com/storage/volumes/#backup-restore-or-migrate-data-volumes) on backing up, migrating, and restoring with named volumes.

For the database backups, it is as simple as copying the contents of the backup directory from the old host machine to the new host machine


# Usage instructions
## Running the server
The server is managed by Docker Compose and most images are built from local resources. Thus, there are two steps to running the server:

1. `sudo docker-compose build` builds the necessary images.
2. `sudo docker-compose up [--build] [-d]` starts the server. The `--build` flag combines steps 1 and 2. The `-d` flag runs the services as a daemon. `-d` is usually the desired behavior.

See `docker-compose --help` for more details usage instructions.

Other useful commands include `sudo docker-compose logs` to view the service logs and `sudo docker-compose down` to stop the server.

## Database administration
To access the database, `sudo docker exec -it autopi_db psql -U autopi -d autopi` should be run. This will put you into `psql` inside the database service. Some useful administrative commands are described in `docs/web/database/admin.md`.

For example, `INSERT INTO autopi.user (username, is_admin) VALUES ('minesusername', true);` will add an administrator.

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
20. Copy the `ID` into the file opened in step 16.
21. Save and close the file.
22. Eject the SD card and plug it into the Raspberry Pi.
23. Plug in the Raspberry Pi, lights will turn on.
24. See *Get IP/status information* to confirm successful registration. 
25. To add additional networks, see *Home Network Registration* procedure.

### Home Network Registration
There are two methods for adding a Home network to the Raspberry Pi.
- If you *can* SSH into Raspberry Pi:
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
5. Note that Raspberry Pis highlighted in yellow are off or cannot be contacted for some other reason. If this occurs, try restarting the Raspberry Pi.

## Common issues

# Development instructions
Run `pip3 install -r requirements.txt` and `pip3 install -r requirements-dev.txt`.
Run `pre-commit install`.
When `pre-commit` fails (and a hook states that files have changed), run `git add --update` to update the git staging area.
