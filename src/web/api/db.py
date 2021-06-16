"""Test API server."""

import os
from contextlib import contextmanager
from typing import Optional

import psycopg2

from .core import StatusModel


def get_db_credentials() -> dict:
    """Get db credentials from environment."""
    with open(os.environ["POSTGRES_PASSWORD_FILE"], "r") as fin:
        password = fin.read().strip()
    return {
        "host": os.environ["POSTGRES_HOST"],
        "database": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": password,
    }


class PiDBConnection:
    """An object representing a single connection with the database, providing needed database queries."""

    def __init__(self, credentials: dict = get_db_credentials()):
        """Initialize members and opens database connection.

        Args:
            credentials (dict): dictionary with database credentials for opening connection.
        """
        self._connection = None
        self.connect(credentials)

    def __del__(self):
        """Close connection on delete."""
        if self._connection is not None and not self._connection.closed:
            self.close()

    def connect(self, credentials: dict = get_db_credentials()):
        """Open a new connection, closing the previouus connection if applicable.

        Args:
            credentials (dict): dictionary with database credentials for opening connection.
        """
        self._credentials = credentials

        if self._connection is not None and not self._connection.closed:
            self.close()
        self._connection = psycopg2.connect(**credentials)

    def close(self):
        """Close database connection."""
        if self._connection is not None and not self._connection.closed:
            self._connection.close()
            self._connection = None

    def _commit(self, query: str, data: Optional[tuple] = None):
        """Execute query.

        Opens cursor and commits transaction. Intended for modification queries.

        Args:
            query (str): the query to be executed.
            data (Optional[tuple]): parameters to be used (safely) in the query. It is passed directly to the execute call.
        """
        with self._connection:
            with self._connection.cursor() as cur:
                if data is None:
                    cur.execute(query)
                else:
                    cur.execute(query, data)

    def _fetch_first_cell(self, query: str, data: Optional[tuple] = None) -> Optional:
        """Execute query, returning query result.

        Opens cursor and commits transaction. Intended for use with "SELECT" queries.

        Args:
            query (str): the query to be executed.
            data (Optional[tuple]): parameters to be used (safely) in the query. It is passed directly to the execute call.

        Returns:
            tuple: all response rows.
        """
        with self._connection:
            with self._connection.cursor() as cur:
                if data is None:
                    cur.execute(query)
                else:
                    cur.execute(query, data)
                result = cur.fetchone()
                return result[0] if result is not None else None

    def _fetchall(self, query: str, data: Optional[tuple] = None) -> list[tuple]:
        """Execute query, returning query result.

        Opens cursor and commits transaction. Intended for use with "SELECT" queries.

        Args:
            query (str): the query to be executed.
            data (Optional[tuple]): parameters to be used (safely) in the query. It is passed directly to the execute call.

        Returns:
            list: all response rows.
        """
        with self._connection:
            with self._connection.cursor() as cur:
                if data is None:
                    cur.execute(query)
                else:
                    cur.execute(query, data)
                return cur.fetchall()

    def add_user(self, username: str):
        """Add new user to database on first login.

        Args:
            username (str): the username it will be connected to.

        Raises:
            pyscopg2.errors.UniqueViolation (derived from pyscopg2.IntegrityError): on user exists
        """
        query = """
            INSERT INTO autopi.user (username)
            VALUES (%s);
        """
        print(username)
        self._commit(query, (username,))

    def user_exists(self, username: str) -> bool:
        """Check if user exists.

        Args:
            username (str): the username to check.

        Returns:
            bool: user exists.
        """
        query = """
            SELECT true FROM autopi.user
            WHERE username = %s LIMIT 1;
        """
        return self._fetch_first_cell(query, (username,))

    def is_admin(self, username: str) -> bool:
        """Check if user is an admin.

        Args:
            username (str): the username to check.

        Returns:
            bool: user is an admin.

        Raises:
            ValueError: on user does not exist.
        """
        query = """
            SELECT is_admin FROM autopi.user
            WHERE username = %s LIMIT 1;
        """
        result = self._fetch_first_cell(query, (username,))
        if result is not None:
            return result
        raise ValueError("invalid username supplied")

    def add_raspi(self, username: str) -> str:
        """Add a new row to the raspi table for a given user.

        Args:
            username (str): the username it will be connected to.

        Returns:
            str: the new device's UUID.
        """
        query = """
            INSERT INTO autopi.raspi (username)
            VALUES (%s)
            RETURNING device_id;
        """
        return self._fetch_first_cell(query, (username,))

    def get_raspis(self, username: Optional[str] = None, registered_only=True) -> list[tuple]:
        """Return a list of Raspberry Pis.

        Args:
            username (optional, str): restrict list to Pis belonging to a specific user.
            registered (bool, default: True): restrict list to those Pis that are registered.

        Returns:
            list: Raspberry Pis (device_id: str, alias: str, ip_addrress: str, ssid: str, ssh: str, vnc: str, updated_at: datetime, power: str).
        """
        # build query
        data = tuple()
        condition = ""
        if username is not None:
            data = (username,)
            condition = "WHERE username = %s"
            if registered_only:
                condition += " AND registered = true"
        elif registered_only:
            condition = "WHERE registered = true"
        query = f"""
            SELECT device_id, alias, ip_addr, ssid, ssh, vnc, updated_at, power FROM autopi.raspi {condition};
        """
        # execute query
        return self._fetchall(query, data)

    def get_unregistered_devid(self, username: str) -> str:
        """Obtain an unregistered ID, creating one if none exist.

        Args:
            username (str)

        Returns:
            str: the device UUID.
        """
        fetch_query = """SELECT device_id FROM autopi.raspi WHERE username=%s AND registered=false;"""
        result = self._fetch_first_cell(fetch_query, (username,))
        # TODO could check that only one id is unregistered, maybe log it
        # TODO expire unregistered device IDs after 2-3 days for improved security
        if result is not None:
            return result

        # no un-registered entry yet; add one
        return self.add_raspi(username)

    def devid_exists(self, devid: str) -> bool:
        """Check if the given device ID is present in the table.

        Args:
            devid (str): the device ID.

        Returns:
            bool: whether the device exists (false if invalid ID).
        """
        query = """
            SELECT device_id FROM autopi.raspi WHERE device_id=%s;
        """
        try:
            result = self._fetch_first_cell(query, (devid,))
            return result is not None
        except psycopg2.errors.InvalidTextRepresentation:
            # Not a valid ID
            return False

    def get_hardware_id(self, devid: str) -> str:
        """Get the hardware ID for a given device.

        Args:
            devid (str): the device ID.

        Returns:
            str: the device's hardware ID.

        Raises:
            ValueError: on device id does not exist.
        """
        query = """
            SELECT hardware_id FROM autopi.raspi WHERE device_id=%s LIMIT 1;
        """
        results = self._fetchall(query, (devid,))
        if len(results) == 0:
            raise ValueError("device ID does not exist")
        return results[0][0]

    def update_status_general(self, status: StatusModel):
        """Update device row in database.

        Args:
            status (StatusModel): the POST data from the API request, containing at least the device and hardware IDs.
        """
        query = """
            UPDATE autopi.raspi
            SET hardware_id=%s, power='on'
        """
        data = [status.hwid]
        if status.ip is not None:
            query += ", ip_addr=%s"
            data.append(status.ip)
        if status.ssh is not None:
            query += ", ssh=%s"
            data.append(status.ssh)
        if status.vnc is not None:
            query += ", vnc=%s"
            data.append(status.vnc)
        if status.ssid is not None:
            query += ", ssid=%s"
            data.append(status.ssid)
        query += " WHERE device_id=%s;"
        data.append(status.devid)

        self._commit(query, tuple(data))

    def update_status_shutdown(self, status: StatusModel):
        """Update device row in database with device shutdown.

        Args:
            status (StatusModel): the POST data from the API request, containing at least the device and hardware IDs.
        """
        query = """
            UPDATE autopi.raspi
            SET hardware_id=%s, power='off'
            WHERE device_id=%s;
        """
        self._commit(query, (status.hwid, status.devid))

    def add_raspi_warning(self, devid: str, warning: str):
        """Add warning for specific device.

        Args:
            devid (str): device ID.
            warning (str): warning string to add.
        """
        query = """
            INSERT INTO autopi.raspi_warning (device_id, warning)
            VALUES (%s, %s)
            ON CONFLICT (device_id, warning) DO UPDATE SET added_at=NOW();
        """
        self._commit(query, (devid, warning))

    def get_device_warnings(self, devid: str) -> list:
        """Return list of warnings for a specific device.

        Args:
            devid (str): device ID.

        Returns:
            list[(warning: str, added_at: datetime.datetime)]: the list of warnings if any
        """
        query = """
            SELECT warning, added_at FROM autopi.raspi_warning
            WHERE device_id=%s;
        """
        return self._fetchall(query, (devid,))

    def get_user_warnings(self, username: str) -> list:
        """Return list of warnings for a specific device.

        Returns:
            list[(device_id: str, warning: str, added_at: datetime.datetime)]: the list of warnings if any
        """
        query = """
            SELECT w.device_id, w.warning, w.added_at
            FROM autopi.raspi_warning as w, autopi.raspi as r
            WHERE w.device_id = r.device_id AND r.username = %s;
        """
        return self._fetchall(query, (username,))


@contextmanager
def connect(credentials: list = get_db_credentials()) -> PiDBConnection:
    """Create PIDBConnection instance for 'with' statement."""
    db = PiDBConnection(credentials)
    try:
        yield db
    finally:
        db.close()
