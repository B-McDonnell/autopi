"""Generate webpage and webpage content."""
import datetime
import enum
from dataclasses import dataclass
from typing import Iterable, List, Optional, Union

from airium import Airium


@enum.unique
class Klass(enum.Enum):
    """Klass categories with CSS styling."""

    GOOD = "table_good"  # positive value
    NEUTRAL = "table_neutral"  # neutral value
    BAD = "table_bad"  # bad value
    WARNING = "table_warning"  # user warning
    DEAD = "table_dead"  # entire row is dead


@dataclass(frozen=True)
class RowItem:
    """Item of a row."""

    key: str
    text: str
    klass: Klass


@dataclass(frozen=True)
class Row:
    """Class containing RowItems."""

    items: tuple[RowItem]

    @property
    def columns(self) -> tuple[str]:
        """Get columns of container RowItems."""
        return tuple((item.key for item in self.items))

    @property
    def is_dead(self) -> bool:
        """Check if any RowItem is Klass.DEAD."""
        return Klass.DEAD in (item.klass for item in self.items)


def _table_klassify(s: str) -> str:
    """Preface CSS class with 'table_' if it is not not prefixed already.

    Args:
        s (str): CSS class to add prefix to. Must be a single class.

    Returns:
        str: new CSS class
    """
    s = "_".join(s.lower().split())
    if not s.startswith("table_"):
        return "table_" + s
    return s


def _pretty_datetime(iso_datetime: datetime.datetime) -> str:
    return iso_datetime.strftime("%B %d, %Y %I:%M %p")


def _seconds_since_iso(iso_datetime: datetime.datetime) -> int:
    dt = datetime.datetime.now(iso_datetime.tzinfo) - iso_datetime
    return dt.total_seconds()


def construct_row(items: tuple[tuple[str]], device_id: str, hw_warning: bool = False) -> Row:
    """Construct a Row from a tuple of column headers/values.

    Args:
        items (tuple[tuple[str]]): sequence of row items (key: str, value: str)
        device_id (str): device ID of the RasPi
        hw_warning (bool, optional): row has a warning. Defaults to False.

    Returns:
        Row: [description]
    """
    row_items: list[RowItem] = []
    for key, value in items:
        if key == "Name":
            row_items.append(RowItem(key, value, Klass.WARNING if hw_warning else Klass.NEUTRAL))
        elif key in ("IP Address", "SSID"):
            row_items.append(RowItem(key, value, Klass.NEUTRAL))
        elif key in ("SSH", "VNC"):
            row_items.append(RowItem(key, value, Klass.GOOD if value == "up" else Klass.BAD))
        elif key == "Last Updated":
            age = _seconds_since_iso(value)
            row_items.append(
                RowItem(
                    key,
                    _pretty_datetime(value),
                    Klass.NEUTRAL if age < 2.5 * 60 else Klass.BAD if age < 5 * 60 else Klass.DEAD,
                )
            )  # TODO get delta from config
        elif key == "Username":
            row_items.append(RowItem(key, value, Klass.NEUTRAL))
        elif key == "Power":
            row_items.append(RowItem(key, value, Klass.GOOD if value == "on" else Klass.DEAD))
    return Row(items=row_items)


def make_klass(s: Union[str, List[str]]) -> str:
    """Create a CSS class string.

    Args:
        s (str | list[str]): string or multiple strings to make class string from

    Returns:
        str: class string
    """
    if isinstance(s, str):
        return _table_klassify(s)
    return " ".join([_table_klassify(c) for c in s])


def build_table(a: Airium, rows: Iterable[Row]) -> Airium:
    """Add a table from Rows.

    Args:
        a (Airium): html constructor to add table to
        rows (Iterable[Row]): rows to generate table from

    Raises:
        ValueError: Rows don't have all the same column headers in the same order

    Returns:
        Airium: Airium instance with table added
    """
    if len(rows) < 1:
        a.table()
        return a

    with a.table():
        table_cols = rows[0].columns

        # add header
        with a.tr(klass="table_header"):
            for column in table_cols:
                a.th(klass=make_klass(column), _t=column)

        # add content
        for row in rows:
            if row.columns != table_cols:
                raise ValueError("Row item keys much match in order")
            dead_row = row.is_dead
            with a.tr():
                for item in row.items:
                    a.td(
                        klass=make_klass(
                            [
                                Klass.DEAD.value if dead_row else item.klass.value,
                                item.key,
                            ]
                        ),
                        _t=item.text,
                    )

    return a


def build_homepage_content(
    pi_rows: list[Row], warning_rows: list[Row], admin_pi_rows: list[Row] = [], airium: Optional[Airium] = None
) -> Airium:
    """Construct the warning and raspi tables.

    Args:
    Args:
        pi_rows (list[Row]): RasPi rows
        warning_rows (list[Row]): warning rows
        airium (Airium | None, optional): existing Airium builder to add to. Defaults to None.

    Returns:
        Airium: object containing HTML information
    """
    if airium is None:
        airium = Airium()
    if len(warning_rows) > 0:
        airium.h1(_t="Warnings")
        airium = build_table(airium, warning_rows)
    airium.h1(_t="Raspberry Pis")
    airium = build_table(airium, pi_rows)
    if len(admin_pi_rows) > 0:
        airium.h1(_t="All Other Raspberry Pis")
        airium = build_table(airium, admin_pi_rows)
    return airium


def build_page(title: str, body_content: str, style_file: Optional[str] = None) -> str:
    """Construct a page with the navigation header and styling.

    Args:
        title (str): title of the page
        body_content (str): content of the page
        style_file (str | None, optional): path to a CSS style file. Defaults to None.

    Returns:
        str: string representation of the page's HTML
    """
    if style_file is not None:
        with open(style_file) as fin:
            style = fin.read()

    a = Airium()
    with a.html():
        with a.head():
            if style_file is not None:
                a.style(_t=style)
            a.meta(http_equiv="content-type", content="text/html", charset="utf-8")
            a.title(_t=title)
        with a.body():
            with a.div(klass="topnav"):
                with a.ul():
                    a.li().a(href="/").h2(_t="Home")
                    a.li().a(href="register").h2(_t="Register")
                    a.li().a(href="help").h2(_t="Help")
            a.div(klass="content-wrapper", _t=body_content)
    return str(a)
