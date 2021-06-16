"""Utilities to interact with the user in a consistent manner."""
import math
from typing import Callable, Optional

import stdiomask


def print_header(header: str, pattern: str = "="):
    """Display a header centered within brackets.

    Args:
        header (str): contents of the header
        pattern (str, optional): string to be repeated to bracket the header contents. Defaults to '='.
    """
    # center header contents with a minimum indent of 2
    header_lines = header.splitlines()
    header_length = max((len(line) for line in header_lines))
    minimum_indent = 2
    pattern_count = math.ceil((minimum_indent * 2 + header_length) / len(pattern))
    indent = (pattern_count * len(pattern) - header_length) // 2

    print(pattern_count, indent)
    print(pattern * pattern_count)
    for line in header_lines:
        print(" " * indent + line)
    print(pattern * pattern_count)


def _get_valid_input(
    inputer: Callable,
    validator: Callable[[str], bool],
    error_message: Optional[str] = "Invalid input",
) -> str:
    """Get input validated by a predicate, re-asking on failure.

    Args:
        inputer (Callable): function that gets input
        validator (Callable[str, bool]): function that validates input
        error_message (Optional[str], optional): message to display before a retry when validation failes. Defaults to None.
        *args: positional arguments for inputer
        **kwargs: keyword arguments for inputer

    Returns:
        (str): user input
    """
    while True:
        user_input = inputer()
        if validator(user_input):
            return user_input

        message = error_message if error_message is not None else ""
        print("\n", message, "\n", end="")


def get_input(
    query: str,
    newline: bool = True,
    validator: Optional[Callable[str, bool]] = None,
    error_message: Optional[str] = None,
) -> str:
    """Get input from user.

    Args:
        query (str): input prompt
        newline (bool, optional): get input on new line. Defaults to True.
        validator (Callable[str, bool] | None, optional): predicate to validate input. Input will be retried until success. Defaults to None.
        error_message (str | None, optional): message to display when input is invalid. Defaults to None.

    Returns:
        str: user input
    """
    query = query + "\n" if newline else query
    if validator is None:
        return input(query)
    return _get_valid_input(lambda: input(query), validator, error_message)


def get_secret(
    query: str,
    newline: bool = True,
    validator: Optional[Callable[[str], bool]] = None,
    error_message: Optional[str] = None,
    mask: str = "*",
    get_twice: bool = True,
) -> str:
    """Get masked input from user.

    Args:
        query (str): input prompt
        newline (bool, optional): get input on new line. Defaults to True.
        validator (Callable[str, bool] | None, optional): predicate to validate input. Defaults to None.
        error_message (str | None, optional): message to display when input is invalid. Defaults to None.
        mask (str, optional): character to mask input with. Defaults to "*".
        get_twice (bool, optional): confirm masked input by comparing two separate inputs. Defaults to True.

    Returns:
        str: user input
    """

    def _input(query: str, mask: str) -> str:
        if validator is None:
            return stdiomask.getpass(query, mask=mask)
        return _get_valid_input(lambda: stdiomask.getpass(query, mask=mask), validator, error_message)

    query = query + "\n" if newline else query
    while True:
        user_input = _input(query, mask)

        if not get_twice:
            return user_input

        user_input_check = _input("Re-type:", mask)

        if user_input != user_input_check:
            print("Inputs don't match\n")
            continue

        return user_input
