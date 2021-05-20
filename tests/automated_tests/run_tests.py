#!/usr/bin/env python3

import subprocess
import sys
import os
import pathlib
from pathlib import Path

def get_dirs(p: Path):
    """
    Get all subdirectories under a directory
    Assumes that p is a directory
    """
    return [x for x in p.iterdir() if x.is_dir()]

def get_tests(p: Path):
    flist = [x for x in p.iterdir() if x.is_file()]
    return [x for x in flist if x.suffix == '.py']

abs_path = Path(sys.argv[0]).absolute().parent

test_dirs = get_dirs(abs_path)
for p in test_dirs:
    print("===================================")
    print("Running tests for script:", p.name)
    print("===================================")
    os.chdir(str(p))
    tests = get_tests(p)
    for test in tests:
        print("------------------------")
        print("Running test set:", test.stem);
        print("------------------------")
        subprocess.run(['python3', '-m', 'unittest', str(test.name)])
