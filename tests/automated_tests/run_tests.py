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
    """
    return [x for x in p.iterdir() if x.is_dir() and x.name != '__pycache__']


def get_test_files(p: Path):
    flist = [x for x in p.iterdir() if x.is_file()]
    return [x for x in flist if x.name.endswith('_test.py')]


abs_path = Path(sys.argv[0]).absolute().parent

test_dirs = get_dirs(abs_path)
save_dir = os.getcwd()
runner = unittest.TextTestRunner()
nerrors = 0
nfailures = 0
nskipped = 0
for p in test_dirs:
    print("===================================")
    print("Running tests for script:", p.name)
    print("===================================")

    testfiles = get_test_files(p)
    if len(testfiles) == 0:
        continue

    os.chdir(save_dir)
    modules = [import_module(p.name + '.' + x.stem) for x in testfiles]
    os.chdir(str(p))
    for i,module in enumerate(modules):
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
