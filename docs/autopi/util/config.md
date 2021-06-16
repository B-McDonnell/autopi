# Implementation
Uses a frozen `dataclass.dataclass` instance to set and control application defaults and settings.

# Dependencies
N/A

# Technical considerations
While all the settings are set directly in `config.py`, it would not be an especially difficult refactor to switch to a more normal config.
For example, using `pydantic` instead of `dataclasses` would make a JSON configuration file trivial.