# Entering `psql`
Run `sudo docker exec -it autopi_db psql -U autopi -d autopi`

# Automation
Some administration is automated.

All timestamps are created and update automatically, and should never need to be written directly.

There are `CASCADE` deletion rules set so that a Raspberry Pi's deletion removes its warnings and a user's deletion removes their Raspberry Pis.

Users that have not logged in at least a year are deleted when new users are added. This strategy is much easier than setting up scheduled tasks inside a Docker container and should not cause storage issues, as additional users remove expired ones. However, expired users can also be removed explicitely with `DELETE FROM autopi.user WHERE (NOW() - last_login) >= INTERVAL '365 days' AND (autopi.user.is_admin = False);`

# Example commands

## Users

```
                          Table "autopi.user"
   Column   |           Type           | Collation | Nullable | Default 
------------+--------------------------+-----------+----------+---------
 last_login | timestamp with time zone |           | not null | now()
 username   | text                     |           | not null | 
 is_admin   | boolean                  |           | not null | false
Indexes:
    "user_pkey" PRIMARY KEY, btree (username)
Referenced by:
    TABLE "raspi" CONSTRAINT "raspi_username_fkey" FOREIGN KEY (username) REFERENCES "user"(username) ON DELETE CASCADE
Triggers:
    expired AFTER INSERT ON "user" FOR EACH STATEMENT EXECUTE FUNCTION delete_expired_users()
```

### Adding a normal user:

`INSERT INTO autopi.user (username) VALUES ('minesusername');`

### Adding an admin user:

`INSERT INTO autopi.user (username, is_admin) VALUES('minesusername', true);`

### Removing a specific user:

`DELETE FROM autopi.user WHERE username = 'minesusername';`

### Getting a list of users:

`SELECT username[, last_login] FROM autopi.user;`

## Raspberry Pis

```
                                                 Table "autopi.raspi"
   Column    |           Type           | Collation | Nullable |                       Default                        
-------------+--------------------------+-----------+----------+------------------------------------------------------
 device_id   | uuid                     |           | not null | uuid_generate_v4()
 ssid        | text                     |           |          | 
 hardware_id | text                     |           |          | 
 registered  | boolean                  |           | not null | generated always as (hardware_id IS NOT NULL) stored
 ip_addr     | text                     |           |          | 
 alias       | text                     |           |          | 
 updated_at  | timestamp with time zone |           | not null | now()
 added_at    | timestamp with time zone |           | not null | now()
 vnc         | text                     |           |          | 
 ssh         | text                     |           |          | 
 power       | text                     |           |          | 
 username    | text                     |           |          | 
Indexes:
    "raspi_pkey" PRIMARY KEY, btree (device_id)
Foreign-key constraints:
    "raspi_username_fkey" FOREIGN KEY (username) REFERENCES "user"(username) ON DELETE CASCADE
Referenced by:
    TABLE "raspi_warning" CONSTRAINT "raspi_warning_device_id_fkey" FOREIGN KEY (device_id) REFERENCES raspi(device_id) ON DELETE CASCADE
Triggers:
    onupdate BEFORE UPDATE ON raspi FOR EACH ROW EXECUTE FUNCTION update_user_time()
```

### Warnings

```
                     Table "autopi.raspi_warning"
  Column   |           Type           | Collation | Nullable | Default 
-----------+--------------------------+-----------+----------+---------
 warning   | text                     |           | not null | 
 added_at  | timestamp with time zone |           | not null | now()
 device_id | uuid                     |           | not null | 
Indexes:
    "raspi_warning_pkey" PRIMARY KEY, btree (device_id, warning)
Foreign-key constraints:
    "raspi_warning_device_id_fkey" FOREIGN KEY (device_id) REFERENCES raspi(device_id) ON DELETE CASCADE
```