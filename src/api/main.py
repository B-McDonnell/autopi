"""Test API server."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


class Status(BaseModel):
    """Base class for status JSON."""

    hwid: str
    devid: str
    event: str
    ip: str
    ssid: str
    ssh: str
    vnc: str


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


@app.post("/api/status")
def update_status(status: Status):
    """Print status received."""
    print(status)
    return {"response text": "I got the status update!", "status": status}
