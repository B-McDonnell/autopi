from dataclasses import dataclass

@dataclass(frozen=True)
class Config: 
    homepageAutoRefresh: bool = True
    homepageAutoRefreshTime: int = 30
