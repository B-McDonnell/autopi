"""API configuration."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Frozen API configuation."""

    homepageAutoRefresh: bool = True
    homepageAutoRefreshTime: int = 30
