#!/usr/bin/env python3

import sys
from importlib import import_module
import os
import pathlib
from pathlib import Path
from unittest import TestLoader, TestSuite
import unittest


def get_dirs(p: Path):
    """
    Get all subdirectories under a directory
    Assumes that p is a directory
    Returns a list of Path objects for each directory
    """
    return [x for x in p.iterdir() if x.is_dir() and x.name != '__pycache__']


def get_test_files(p: Path):
    """
    Get all files named according to the pattern *_test.py in the specified folder (non-recursive).
    Returns a list of Path objects for each test file
    """
    flist = [x for x in p.iterdir() if x.is_file()]
    return [x for x in flist if x.name.endswith('_test.py')]


abs_path = Path(sys.argv[0]).absolute().parent

test_dirs = get_dirs(abs_path)
runner = unittest.TextTestRunner()
nerrors = 0
nfailures = 0
nskipped = 0
for p in test_dirs:
    # Load all scripts under directory p, run tests in them

    print("===================================")
    print("Running tests for script:", p.name)
    print("===================================")

    testfiles = get_test_files(p)
    if len(testfiles) == 0:
        continue

    os.chdir(abs_path)
    modules = [import_module(p.name + '.' + x.stem) for x in testfiles]
    os.chdir(p)
    for i, module in enumerate(modules):
        # Run all unittest tests in each file

        print("-----------------------------------")
        print("Running tests for script:", testfiles[i].name)
        print("-----------------------------------")
        t = TestLoader()
        tests = t.loadTestsFromModule(module)
        suite = TestSuite(tests)
        result = runner.run(suite)
        nerrors += len(result.errors)
        nfailures += len(result.failures)
        nskipped += len(result.skipped)
        print()
    print()
    print()

# Print results
print("------------------------------------------------")
print("================================================")
print()
print("Tests completed")
if nfailures > 0:
    print(nfailures, "Failed Tests")
if nerrors > 0:
    print(nerrors, "Tests with Errors")
if nskipped > 0:
    print(nerrors, "Skipped Tests")
print()
