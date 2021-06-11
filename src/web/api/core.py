"""Test API server core functionality."""

from pydantic import BaseModel
from typing import Optional

class StatusModel(BaseModel):
    """Base class for status JSON."""

    hwid: str
    devid: str
    event: str
    ip: Optional[str]
    ssid: Optional[str]
    ssh: Optional[str]
    vnc: Optional[str]


class UserModel(BaseModel):
    """Base class for user JSON."""

    username: str
