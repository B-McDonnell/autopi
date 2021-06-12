import datetime
import enum
import os
from dataclasses import dataclass
from pprint import pprint
from tempfile import NamedTemporaryFile
from typing import Iterable, List, Union

from airium import Airium


@enum.unique
class Klass(enum.Enum):
    GOOD = "table_good"  # positive value
    NEUTRAL = "table_neutral"  # neutral value
    BAD = "table_bad"  # bad value
    WARNING = "table_warning"  # user warning
    DEAD = "table_dead"  # entire row is dead


@dataclass(frozen=True)
class RowItem:
    key: str
    text: str
    klass: Klass


@dataclass(frozen=True)
class Row:
    items: tuple[RowItem]

    @classmethod
    def from_dict(cls, dictionary: dict):
        raise NotImplementedError()

    @property
    def columns(self) -> tuple[str]:
        return tuple((item.key for item in self.items))

    @property
    def is_dead(self) -> bool:
        return Klass.DEAD in (item.klass for item in self.items)


def check_html(html_str: str, print_out: bool = False):
    if print_out:
        print(html_str)
    with NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(html_str)
        os.system(f"firefox --new-window {tmp.name}")


def _table_klassify(s: str) -> str:
    s = "_".join(s.lower().split())
    if not s.startswith("table_"):
        return "table_" + s
    return s


def make_klass(s: Union[str, List[str]]) -> str:
    if isinstance(s, str):
        return _table_klassify(s)
    return " ".join([_table_klassify(c) for c in s])


def build_table(a: Airium, rows: Iterable[Row]):
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


def _pretty_datetime(iso_datetime: datetime.datetime) -> str:
    return iso_datetime.strftime("%B %d, %Y %I:%M %p")


def _seconds_since_iso(iso_datetime: str) -> int:
    dt = datetime.datetime.now(iso_datetime.tzinfo) - iso_datetime
    return dt.total_seconds()


def construct_row(
    items: tuple[tuple[str]], device_id: str, hw_warning: bool = False
) -> Row:
    row_items: list[RowItem] = []
    for key, value in items:
        if key == "Name":
            row_items.append(
                RowItem(key, value, Klass.WARNING if hw_warning else Klass.NEUTRAL)
            )
        elif key in ("IP Address", "SSID"):
            row_items.append(RowItem(key, value, Klass.NEUTRAL))
        elif key in ("SSH", "VNC"):
            row_items.append(
                RowItem(key, value, Klass.GOOD if value == "up" else Klass.BAD)
            )
        elif key == "Last Updated":
            row_items.append(
                RowItem(
                    key,
                    _pretty_datetime(value),
                    Klass.NEUTRAL
                    if _seconds_since_iso(value) < 5 * 60
                    else Klass.WARNING,
                )
            )  # TODO get delta from config
        elif key == "Power":
            row_items.append(
                RowItem(key, value, Klass.GOOD if value == "on" else Klass.DEAD)
            )
    return Row(items=row_items)


def get_raspis() -> list[tuple[str]]:
    # TEMP
    return [
        (
            "qwertyuiop",
            "hyper_bunny",
            "10.0.0.69",
            "SomeFunnyJoke",
            "ON",
            "ON",
            "2021-06-20 08:01:39.123456+00",
            "ON",
        ),
        (
            "asdfghjkl",
            "lazy_dog",
            "192.168.1.52",
            "SomeLameJokeWith32CharactersLmao",
            "OFF",
            "OFF",
            "2021-01-10 08:01:02.987654+22",
            "ON",
        ),
        (
            "zxcvbnm",
            "cute_kitten",
            "172.16.13.37",
            "Another SSID",
            "OFF",
            "OFF",
            "2021-08-10 00:00:00.000000+00",
            "OFF",
        ),
    ]


def get_warnings() -> list[tuple[str]]:
    # TEMP
    return [
        # ("asdfghjkl", "lazy_dog", "An unrecognized device is using the ID of this Pi. If this is not you, contact your instructor")
    ]


def build_page(rows, warnings):
    with open("/app/style.css") as fin:
        style = fin.read()

    a = Airium()
    with a.html():
        with a.head():
            a.style(_t=style)
            a.meta(
                http_equiv="content-type",
                content="text/html; charset=UTF-8;charset=utf-8",
            )
        with a.body():
            with a.div(klass="topnav"):
                with a.ul():
                    a.li().a(href="/").h2(_t="Home")
                    a.li().a(href="register").h2(_t="Register")
                    a.li().a(href="help").h2(_t="Help")
            with a.div(klass="content-wrapper"):
                if len(warnings) > 0:
                    a.h1(_t="Warnings")
                    a = build_table(a, warnings)
                a.h1(_t="Raspberry Pis")
                a = build_table(a, rows)
    return str(a)
