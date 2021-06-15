"""Get configuration settings."""

from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass(frozen=True, init=False)
class Config(object):
    """Contains configuration settings."""

    API_URL: ClassVar[str] = "https://autopi.mines.edu/api/status"
    WPA_CONFIG_FILE: ClassVar[str] = "/etc/wpa_supplicant/wpa_supplicant.conf"
    ROOT_DIR: ClassVar[str] = "/var/opt/autopi"
    NEW_NETWORK_FILE: ClassVar[str] = "/boot/CSM_new_network.txt"
    DEV_ID_FILE: ClassVar[str] = "/boot/CSM_device_id.txt"
    HW_ID_SOURCE_FILE: ClassVar[str] = "/proc/cpuinfo"
    HW_ID_START_LINE: ClassVar[Optional[int]] = -4
    HW_ID_STOP_LINE: ClassVar[Optional[int]] = None
    DEFAULT_COUNTRY: ClassVar[str] = "US"
    SSH_SERVICE: ClassVar[str] = "sshd"
    VNC_SERVICE: ClassVar[str] = "vncserver-x11-serviced"
    DEFAULT_WIRELESS_INTERFACE: ClassVar[str] = "wlan0"
    DEFAULT_WIRED_INTERFACE: ClassVar[str] = "eth0"
