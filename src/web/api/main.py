"""Test API server."""

from fastapi import FastAPI, HTTPException, Cookie
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from .core import StatusModel, UserModel
from . import db


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
def register(username: str = Cookie(None)): # FIXME this is probably not how the username cookie is passed, if that is how shibboleth works
    """Serve register page."""
    if username is None:
        raise HTTPException(status_code=401, detail="Please log in...") # TODO A redirect would probably be better

    devid = db.get_unregistered_devid(username)

    # FIXME Return a nicer page!
    # TODO The contents of the page have a baked in assumption about the device file name
    content = f"""
    <html>
        <head>
            <title>Help page</title>
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
        db.add_user_query(user.username)
    except Exception as e:
        # Ensure proper error logging
        print("Error:", e)
    return {"response text": "It didn't crash!!"}


@app.post("/api/status")
def update_status(status: StatusModel):
    """Print status received."""
    if not db.devid_exists(status.devid):
        raise HTTPException(status_code=403) # TODO ascertain proper response to bad id; minimal information is preferable

    prev_hwid = db.query_hardware_id(status.devid)
    if prev_hwid != status.hwid:
        db.add_raspi_warning(status.devid, "New hardware ID detected!") # TODO handle message properly

    if status.event == 'shutdown':
        db.update_status_shutdown(status)
    else:
        db.update_status_general(status)
    print(status)
    return {"response text": "I got the status update!", "status": status}
