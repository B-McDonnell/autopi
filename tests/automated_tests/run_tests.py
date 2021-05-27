#!/usr/bin/env python3

"""Run and display all automated tests in /tests/automated_tests."""

import os
import sys
import unittest
from importlib import import_module
from pathlib import Path
from unittest import TestLoader, TestSuite


def get_dirs(p: Path) -> list:
    """
    Get all subdirectories under a directory.

    Args:
        p (pathlib.Path): directory to search.

    Returns:
        list[Path]: list of directories under p.
    """
    return [x for x in p.iterdir() if x.is_dir() and x.name != "__pycache__"]


def get_test_files(p: Path) -> list:
    """
    Get all files name according to the pattern *_test.py in the specified folder. Does not recurse.

    Args:
        p (pathlib.Path): directory to search.

    Returns:
        list[Path]: list of test files under p.
    """
    flist = [x for x in p.iterdir() if x.is_file()]
    return [x for x in flist if x.name.endswith("_test.py")]


def print_header(contents: str, character="="):
    """
    Print a header.

    Args:
        contents (str): header contents.
        character (str): character to build the header brackets with. Default "=".
    """
    bracket = character * (len(contents) + 4)
    print(bracket)
    print("  " + contents)
    print(bracket)


def main():
    """Run all unit tests. Returns 0 if all succeed, non-zero otherwise."""
    abs_path = Path(sys.argv[0]).absolute().parent

    test_dirs = get_dirs(abs_path)
    runner = unittest.TextTestRunner()
    nerrors = 0
    nfailures = 0
    nskipped = 0
    for p in test_dirs:
        # Load all scripts under directory p, run tests in them

        print_header("Running tests for script: " + p.name)

        testfiles = get_test_files(p)
        if len(testfiles) == 0:
            continue

        os.chdir(abs_path)
        modules = [import_module(p.name + "." + x.stem) for x in testfiles]
        os.chdir(p)
        for i, module in enumerate(modules):
            # Run all unittest tests in each file

            print_header(
                "Running tests for script: " + testfiles[i].name, character="_"
            )
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
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print_header("Tests completed", character="^")
    if nfailures > 0:
        print(nfailures, "Failed Tests")
    if nerrors > 0:
        print(nerrors, "Tests with Errors")
    if nskipped > 0:
        print(nskipped, "Skipped Tests")
    print()

    if nfailures > 0 or nerrors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
