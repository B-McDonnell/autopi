"""Test API server."""

from psycopg2 import connect
from typing import Optional
from .core import StatusModel, UserModel

# FIXME plaintext credentials
def connect_default():
    return connect(host='autopi_db', database='autopi', user='autopi', password='password')


def commit_simple_query(query: str, data: Optional[tuple] = None):
    with connect_default() as conn:
        with conn.cursor() as cur:
            if data is None:
                cur.execute(query)
            else:
                cur.execute(query, data)
            conn.commit()


def fetch_simple_query(query: str, data: Optional[tuple] = None):
    with connect_default() as conn:
        with conn.cursor() as cur:
            if data is None:
                cur.execute(query)
            else:
                cur.execute(query, data)
            return cur.fetchall()


def add_user_query(username: str):
    """Add new user to database on first login. 
    
    Raises: 
        SOME type of exceptioN??? on user exists
    """
    query = """
        INSERT INTO autopi.user (username)
        VALUES (%s);
    """
    commit_simple_query(query, (username, ))


def add_raspi(username: str) -> str:
    query = """
        INSERT INTO autopi.raspi (username)
        VALUES (%s)
        RETURNING device_id;
    """
    with connect_default() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (username, ))
            conn.commit()
            return cur.fetchone()[0] # Ensure this works

def get_unregistered_devid(username: str) -> str:
    fetch_query = """SELECT device_id FROM autopi.raspi WHERE username=%s AND registered=false;"""
    result = fetch_simple_query(fetch_query, (username, ))
    # TODO could check that only one id is unregistered, maybe log it
    if len(result) != 0:
        return result[0][0]

    # no un-registered entry yet; add one
    return add_raspi(username)


def devid_exists(devid: str) -> bool:
    query = """
        SELECT device_id FROM autopi.raspi WHERE device_id=%s; 
    """
    results = fetch_simple_query(query, (devid, ))
    return len(results)


def query_hardware_id(devid: str) -> str:
    query = """
        SELECT hardware_id FROM autopi.raspi WHERE device_id=%s;
    """
    results = fetch_simple_query(query, (devid, ))
    #FIXME does not check that the id exists; assumes that it does
    return results[0][0]


def update_status_general(status: StatusModel):
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

    commit_simple_query(query, tuple(data))


def update_status_shutdown(status: StatusModel):
    query = """
        UPDATE autopi.raspi
        SET hardware_id=%s, power='off'
        WHERE device_id=%s;
    """
    commit_simple_query(query, (status.hwid, status.devid))


def has_timed_out(devid: str) -> bool:
    TIMEOUT_DURATION = '5 minute' # TODO maybe this shouldn't be defined here...
    query = """
        SELECT true FROM autopi.raspi
        WHERE device_id=%s 
        AND updated_at + interval %s < now();
    """ # TODO perhaps the timeout should not be handled by the 
    result = fetch_simple_query(query, (devid, TIMEOUT_DURATION))
    return len(result) > 0
    

def add_raspi_warning(devid: str, warning: str):
    query = """
        INSERT INTO autopi.raspi_warning (device_id, warning)
        VALUES (%s, %s);
    """
    commit_simple_query(query, (devid, warning))

def get_raspi_warnings(devid: str) -> list:
    """Return list of warnings for a specific device.

    Returns:
        list[(warning: str, added_at: datetime.datetime)]: the list of warnings if any
    """
    query = """
        SELECT warning, added_at FROM autopi.raspi_warning 
        WHERE device_id=%s;
    """
    return fetch_simple_query(query, (devid, ))
