"""Test API server."""

from fastapi import Cookie, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .core import StatusModel
from .db import connect
from .generate_html import Klass, Row, RowItem, build_homepage_content, build_page, construct_row

app = FastAPI()


# TODO it may simplify things to have Caddy/Apache guarantee that the user is authenticated before reaching this point
@app.get("/", response_class=HTMLResponse)
def root(
    username: str = Cookie(None),
):
    """Serve raspi list."""
    if username is None:
        raise HTTPException(status_code=401, detail="Please log in...")  # TODO A redirect would probably be better

    with connect() as db:
        raspis = db.get_raspis(username if not db.is_admin(username) else None)
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

    columns = ["Name", "IP Address", "SSID", "SSH", "VNC", "Last Updated"]
    raspi_rows = [
        construct_row(zip(columns, items[1:]), items[0], hw_warning=items[0] in warning_ids) for items in raspis
    ]

    body = build_homepage_content(raspi_rows, warning_rows)
    content = build_page(title="Autopi", body_content=str(body), style_file="/app/style.css")
    return HTMLResponse(content=content, status_code=200)


# TODO: This comment block is just to remind me when this is implemented properly
# @app.post("/api/add_user")
# def add_user(user: UserModel):
# try:
#     with connect() as db:
#         db.add_user_query(user.username)
# except Exception as e:
#     # Ensure proper error logging
#     print("Error:", e)
# return {"response text": "It didn't crash!!"}


@app.get("/help", response_class=HTMLResponse)
def help():
    """Serve help page."""
    with open("/app/help.html") as f:
        content = f.read()

    content = build_page(title="Autopi Help", body_content=content, style_file="/app/style.css")
    return HTMLResponse(content=content, status_code=200)


@app.get("/register", response_class=HTMLResponse)
def register(
    username: str = Cookie(None),
):  # FIXME this is probably not how the username cookie is passed, if that is how shibboleth works
    """Serve register page."""
    if username is None:
        raise HTTPException(status_code=401, detail="Please log in...")  # TODO A redirect would probably be better

    devid = None
    with connect() as db:
        devid = db.get_unregistered_devid(username)

    # FIXME Return a nicer page!
    # TODO The contents of the page have a baked in assumption about the device file name
    filename = "/boot/CSM_device_id.txt"
    content = f"""
    <html>
        <head>
            <title>Register</title>
        </head>
        <body>
            <p>Enter the following ID in '{filename}'. Visit the <a href="help">help page</a> for more in-depth instructions.</p>
            <h1>{devid}</h1>
        </body>
    </html>
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
        if prev_hwid != status.hwid:
            # TODO message should maybe not be defined in code??
            msg = "The hardware of this device has changed. If this was not you, contact your instructor."
            db.add_raspi_warning(status.devid, msg)

        if status.event == "shutdown":
            db.update_status_shutdown(status)
        else:
            db.update_status_general(status)
        print(status)  # TODO Maybe don't do this...
        return {}
