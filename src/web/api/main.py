"""API server."""

from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse

from .config import Config
from .core import StatusModel
from .db import PiDBConnection, connect
from .generate_html import Klass, Row, RowItem, build_homepage_content, build_page, construct_row

app = FastAPI()


def user_login(db: PiDBConnection, username: str):
    """Perform user login tasks."""
    if not db.user_exists(username):
        db.add_user(username)
    else:
        db.update_user_login(username)


@app.get("/", response_class=HTMLResponse)
def root(uid: Optional[str] = Header(None)):
    """Serve raspi list."""
    username = uid
    if username is None or username == '':
        raise HTTPException(status_code=401, detail="Not logged in")  # TODO A redirect would probably be better
    with connect() as db:
        user_login(db, username)

        is_admin = db.is_admin(username)
        raspis = db.get_raspis(username if not is_admin else None)
        warnings = db.get_user_warnings(username, get_alias=True)
    warning_ids = [warning[1] for warning in warnings]
    warning_rows = tuple(
        Row(
            items=(
                RowItem("Name", warning[0], Klass.WARNING),
                RowItem("Warning Description", warning[2], Klass.WARNING),
            )
        )
        for warning in warnings
    )

    if not is_admin:
        columns = ["Name", "IP Address", "SSID", "SSH", "VNC", "Last Updated"]
        raspi_rows = [
            construct_row(zip(columns, items[1:]), items[0], hw_warning=items[0] in warning_ids) for items in raspis
        ]
        body = build_homepage_content(raspi_rows, warning_rows)
    else:
        owned_raspis = [raspi for raspi in raspis if raspi[-2] == username]
        other_raspis = [raspi for raspi in raspis if raspi[-2] != username]
        columns = ["Name", "IP Address", "SSID", "SSH", "VNC", "Last Updated"]
        raspi_rows = [
            construct_row(zip(columns, items[1:]), items[0], hw_warning=items[0] in warning_ids)
            for items in owned_raspis
        ]
        columns = ["Name", "IP Address", "SSID", "SSH", "VNC", "Last Updated", "Username"]
        other_raspi_rows = [
            construct_row(zip(columns, items[1:]), items[0], hw_warning=items[0] in warning_ids)
            for items in other_raspis
        ]
        body = build_homepage_content(raspi_rows, warning_rows, other_raspi_rows)

    if Config.homepageAutoRefresh:
        content = build_page(title="Autopi", body_content=str(body), style_file="/app/style.css", refresh_after=30)
    else:
        content = build_page(title="Autopi", body_content=str(body), style_file="/app/style.css")
    return HTMLResponse(content=content, status_code=200)


@app.get("/help", response_class=HTMLResponse)
def help():
    """Serve help page."""
    with open("/app/help.html") as f:
        content = f.read()

    content = build_page(title="Autopi Help", body_content=content, style_file="/app/style.css")
    return HTMLResponse(content=content, status_code=200)


@app.get("/register", response_class=HTMLResponse)
def register(uid: Optional[str] = Header(None)):
    """Serve register page."""
    if uid is None or uid == '':
        raise HTTPException(status_code=401, detail="Please log in...")  # TODO A redirect would probably be better

    username = uid
    devid = None
    with connect() as db:
        user_login(db, username)
        devid = db.get_unregistered_devid(username)

    # FIXME Return a nicer page!
    # TODO The contents of the page have a baked in assumption about the device file name
    filename = "/boot/CSM_device_id.txt"
    content = f"""
        <p>Enter the following ID in '{filename}'. Visit the <a href="help">help page</a> for more in-depth instructions.</p>
        <h1>{devid}</h1>
    """
    content = build_page(title="Autopi Registration", body_content=content, style_file="/app/style.css")

    return HTMLResponse(content=content, status_code=200)


@app.post("/api/status")
def update_status(status: StatusModel):
    """Print status received."""
    with connect() as db:
        if not db.devid_exists(status.devid):
            raise HTTPException(
                status_code=403
            )  # TODO ascertain proper response to bad id; minimal information is preferable

        prev_hwid = db.get_hardware_id(status.devid)
        if prev_hwid != status.hwid and prev_hwid:
            # TODO message should maybe not be defined in code??
            msg = "The hardware of this device has changed. If this was not you, contact your instructor."
            db.add_raspi_warning(status.devid, msg)

        if status.event == "shutdown":
            db.update_status_shutdown(status)
        else:
            db.update_status_general(status)
        print(status)  # TODO Maybe don't do this...
        return {}
