"""Test API server."""

from typing import Optional, Type

from psycopg2 import connect

from .core import StatusModel


# FIXME plaintext credentials
def connect_default():
    return connect(
        host="autopi_db", database="autopi", user="autopi", password="password"
    )


def default_credentials() -> dict:
    return {
        "host": "autopi_db",
        "database": "autopi",
        "user": "autopi",
        "password": "password",
    }


class PiDB:
    def __init__(self, credentials: list = default_credentials()):
        self._connection = None
        self._credentials = credentials

    def __enter__(self):
        self.connect(self._credentials)
        return self

    def __exit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        # exctb: Optional[TracebackType]) -> bool:
        exctb: Optional,
    ) -> bool:
        # FIXME This code is wrong... gobbles all exceptions
        self.close()
        if excinst is not None:
            print(excinst)
            raise excinst
        return True

    def connect(self, credentials: dict):
        self._connection = connect(**credentials)

    def close(self):
        # FIXME these functions may be poorly architected
        self._connection.close()
        self._connection = None

    def _commit_simple_query(self, query: str, data: Optional[tuple] = None):
        with self._connection:
            with self._connection.cursor() as cur:
                if data is None:
                    cur.execute(query)
                else:
                    cur.execute(query, data)

    def _fetch_simple_query(self, query: str, data: Optional[tuple] = None):
        with self._connection:
            with self._connection.cursor() as cur:
                if data is None:
                    cur.execute(query)
                else:
                    cur.execute(query, data)
                return cur.fetchall()

    def add_user_query(self, username: str):
        """Add new user to database on first login.

        Raises:
            SOME type of exceptioN??? on user exists
        """
        query = """
            INSERT INTO autopi.user (username)
            VALUES (%s);
        """
        self._commit_simple_query(query, (username,))

    def add_raspi(self, username: str) -> str:
        query = """
            INSERT INTO autopi.raspi (username)
            VALUES (%s)
            RETURNING device_id;
        """
        with self._connection:
            with self._connection.cursor() as cur:
                cur.execute(query, (username,))
                return cur.fetchone()[0]  # Ensure this works

    def get_unregistered_devid(self, username: str) -> str:
        fetch_query = """SELECT device_id FROM autopi.raspi WHERE username=%s AND registered=false;"""
        result = self._fetch_simple_query(fetch_query, (username,))
        # TODO could check that only one id is unregistered, maybe log it
        if len(result) != 0:
            return result[0][0]

        # no un-registered entry yet; add one
        return self.add_raspi(username)

    def devid_exists(self, devid: str) -> bool:
        query = """
            SELECT device_id FROM autopi.raspi WHERE device_id=%s;
        """
        results = self._fetch_simple_query(query, (devid,))
        return len(results)

    def query_hardware_id(self, devid: str) -> str:
        query = """
            SELECT hardware_id FROM autopi.raspi WHERE device_id=%s;
        """
        results = self._fetch_simple_query(query, (devid,))
        # FIXME does not check that the id exists; assumes that it does
        return results[0][0]

    def update_status_general(self, status: StatusModel):
        query = """
            UPDATE autopi.raspi
            SET hardware_id=%s, power='on'
        """
        data = [status.hwid]
        if status.ip is not None:
            query += """, ip_addr=%s"""
            data.append(status.ip)
        if status.ssh is not None:
            query += """, ssh=%s"""
            data.append(status.ssh)
        if status.vnc is not None:
            query += """, vnc=%s"""
            data.append(status.vnc)
        if status.ssid is not None:
            query += """, ssid=%s"""
            data.append(status.ssid)
        query += """ WHERE device_id=%s;"""
        data.append(status.devid)

        self._commit_simple_query(query, tuple(data))

    def update_status_shutdown(self, status: StatusModel):
        query = """
            UPDATE autopi.raspi
            SET hardware_id=%s, power='off'
            WHERE device_id=%s;
        """
        self._commit_simple_query(query, (status.hwid, status.devid))

    def has_timed_out(self, devid: str) -> bool:
        TIMEOUT_DURATION = "5 minute"  # TODO maybe this shouldn't be defined here...
        query = """
            SELECT true FROM autopi.raspi
            WHERE device_id=%s
            AND updated_at + interval %s < now();
        """  # TODO perhaps the timeout should not be handled by the
        result = self._fetch_simple_query(query, (devid, TIMEOUT_DURATION))
        return len(result) > 0

    def add_raspi_warning(self, devid: str, warning: str):
        query = """
            INSERT INTO autopi.raspi_warning (device_id, warning)
            VALUES (%s, %s);
        """
        self._commit_simple_query(query, (devid, warning))

    def get_raspi_warnings(self, devid: str) -> list:
        """Return list of warnings for a specific device.

        Returns:
            list[(warning: str, added_at: datetime.datetime)]: the list of warnings if any
        """
        query = """
            SELECT warning, added_at FROM autopi.raspi_warning
            WHERE device_id=%s;
        """
        return self._fetch_simple_query(query, (devid,))

    def get_user_wanings(self, username: str) -> list:
        query = """
            SELECT w.device_id, r.alias, w.warning
            FROM autopi.raspi_warning w, autopi.raspi r
            WHERE w.device_id = r.device_id and r.username = %s
        """
        return self._fetch_simple_query(query, (username,))
