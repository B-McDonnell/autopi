"""Test API server."""

from fastapi import Cookie, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .core import StatusModel
from .db import connect

app = FastAPI()


def compose_homepage(username: str) -> str:  # TODO Temporary
    """Return homepage."""

    def add_pi_rows(pi_list: list):
        table = "\n".join([str(pi) for pi in pi_list])
        return table + "\n"

    body = ""
    with connect() as db:
        if db.user_exists(username):
            db.add_user(username)

        user_pis = db.get_raspis(username)
        body += add_pi_rows(user_pis)

        if db.is_admin(username):
            other_pis = [pi for pi in db.get_raspis() if pi not in user_pis]
            body += add_pi_rows(other_pis)

    title = "RaspberryPi List"
    content = f"""
    <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            {body}
        </body>
    </html>
    """
    return content


# TODO it may simplify things to have Caddy/Apache guarantee that the user is authenticated before reaching this point
@app.get("/", response_class=HTMLResponse)
def root(
    username: str = Cookie(None),
):
    """Serve raspi list."""
    if username is None:
        raise HTTPException(
            status_code=401, detail="Please log in..."
        )  # TODO A redirect would probably be better

    content = compose_homepage(username)
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
            Enter the following ID in '{filename}'
            <h1>{devid}</h1>
        </body>
    </html>
    """
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
