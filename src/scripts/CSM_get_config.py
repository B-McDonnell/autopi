#!/usr/bin/env python3
"""Temporary module for reading a dummy configuration."""

import os

# TODO REPLACE ME
def get_api_url() -> str:
    api_url = "http://localhost:8000/"
    if "API_URL" in os.environ: 
        api_url = os.environ["API_URL"]
    else:
        try:
            with open('/autopi.config') as f:
                lines = f.readlines()
        except OSError:
            pass  # TODO what should happen here?
        else:
            for line in lines:
                l = line.strip()
                if line.startswith('API_URL='):
                    api_url = line[8:].strip()
    return api_url


if __name__ == "__main__":
    print(get_api_url())
