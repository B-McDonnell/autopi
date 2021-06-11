"""Test API server."""

from fastapi import Cookie, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .core import StatusModel, UserModel
from .db import PiDB
from .generate_table import Klass, Row, RowItem, build_page, construct_row

app = FastAPI()


# TODO it may simplify things to have Caddy guarantee that the user is authenticated
@app.get("/", response_class=HTMLResponse)
def root(username: str = Cookie(None)):
    with PiDB as db:
        warnings = db.get_user_wanings(username)
        raspis = db.get_raspis()
    warning_ids = [warning[0] for warning in warnings]
    warning_rows = tuple(
        Row(
            items=(
                RowItem("Name", warning[1], Klass.WARNING),
                RowItem("Warning Description", warning[2], Klass.WARNING),
            )
        )
        for warning in warnings
    )

    columns = ["Name", "IP Address", "SSID", "SSH", "VNC", "Last Updated", "Power"]
    rows = [
        construct_row(
            zip(columns, items[1:]), items[0], hw_warning=items[0] in warning_ids
        )
        for items in raspis
    ]

    content = build_page(rows, warning_rows)
    return HTMLResponse(content=content, status_code=200)


@app.get("/help", response_class=HTMLResponse)
def help():
    """Serve help page."""
    content = """
    <html>
        <head>
            <title>Help page</title>
        </head>
        <body>
            <h1>Hello world! This is the help page</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=content, status_code=200)


@app.get("/register", response_class=HTMLResponse)
def register(
    username: str = Cookie(None),
):  # FIXME this is probably not how the username cookie is passed, if that is how shibboleth works
    """Serve register page."""
    if username is None:
        raise HTTPException(
            status_code=401, detail="Please log in..."
        )  # TODO A redirect would probably be better

    devid = None
    with PiDB() as db:
        print("test")
        devid = db.get_unregistered_devid(username)

    # FIXME Return a nicer page!
    # TODO The contents of the page have a baked in assumption about the device file name
    content = f"""
    <html>
        <head>
            <title>Register</title>
        </head>
        <body>
            Enter the following ID in '/boot/CSM_device_id.txt'
            <h1>{devid}</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=content, status_code=200)


# TODO this endpoint is primarily for testing; may not be in final product
@app.post("/api/add_user")
def add_user(user: UserModel):
    try:
        with PiDB() as db:
            db.add_user_query(user.username)
    except Exception as e:
        # Ensure proper error logging
        print("Error:", e)
    return {"response text": "It didn't crash!!"}


@app.post("/api/status")
def update_status(status: StatusModel):
    """Print status received."""
    with PiDB() as db:
        if not db.devid_exists(status.devid):
            raise HTTPException(
                status_code=403
            )  # TODO ascertain proper response to bad id; minimal information is preferable

        prev_hwid = db.query_hardware_id(status.devid)
        if prev_hwid != status.hwid:
            msg = "New hardware ID detected!"
            db.add_raspi_warning(status.devid, msg)  # TODO handle message properly

        if status.event == "shutdown":
            db.update_status_shutdown(status)
        else:
            db.update_status_general(status)
        print(status)
        return {"response text": "I got the status update!", "status": status}
