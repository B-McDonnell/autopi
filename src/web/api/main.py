"""Test API server."""

from fastapi import Cookie, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .core import StatusModel
from .db import connect

app = FastAPI()


# TODO it may simplify things to have Caddy guarantee that the user is authenticated
@app.get("/", response_class=HTMLResponse)
def root():
    """Serve homepage."""
    content = """
    <html>
        <head>
            <title>Hello world home page</title>
        </head>
        <body>
            <h1>Hello world! This is the home page</h1>
        </body>
    </html>
    """
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

    with connect() as db:
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


@app.post("/api/status")
def update_status(status: StatusModel):
    """Print status received."""
    with connect() as db:
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
