from dataclasses import dataclass

@dataclass(frozen=True)
class Config: 
    homepageAutoRefresh: bool = True
