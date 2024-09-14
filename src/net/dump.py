from shutil import copyfile

import requests

from . import ren
from .dumps import clash_conv, quantumult, shadowrocket, surge

__raw = None
__tmp_set = set()

ren.PATH_OUT.mkdir(parents=True, exist_ok=True)
ren.PATH_OUT_SURGE.mkdir(parents=True, exist_ok=True)
ren.PATH_OUT_CLASH.mkdir(parents=True, exist_ok=True)


def dump(araw: dict) -> None:
    global __raw
    if not "ref" in araw:
        return
    var = araw.pop("ref")
    if var["id"] != "":
        var["id"] = "+" + var["id"]
    __raw = araw

    if "quantumult" in var["tar"]:
        __quantumult(var["id"])
    if "clash" in var["tar"]:
        __clash(var["id"])
    if "surge" in var["tar"]:
        __surge(var["id"])
    if "shadowrocket" in var["tar"]:
        __shadowrocket(var["id"])


def __rmt(loc: str, lnk: str) -> None:
    with open(ren.PATH_OUT / loc, "tw", encoding="utf-8") as file:
        file.write(requests.get(lnk, timeout=8).text)


def __quantumult(alia: str) -> None:
    quantumult.load(__raw)

    with open(
        ren.PATH_OUT / ("quantumult" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        quantumult.profile(
            out,
            {
                "parse": ren.URI_NET + "quantumult-parser.js",
            },
        )

    global __tmp_set
    if not "qp" in __tmp_set:
        __tmp_set.add("qp")
        __rmt(
            "quantumult-parser.js",
            ren.EXT_QUANTUMULT_PARSER,
        )


def __clash(alia: str) -> None:
    clash_conv.load(__raw)

    with open(
        ren.PATH_OUT_CLASH / ("conv" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        clash_conv.config(out, {"yml": ren.URI_CLASH + "conv-base" + alia + ".yml"})

    with open(
        ren.PATH_OUT_CLASH / ("conv-base" + alia + ".yml"),
        "tw",
        encoding="utf-8",
    ) as out:
        clash_conv.base(out)


def __surge(alia: str) -> None:
    surge.load(__raw)

    with open(
        ren.PATH_OUT_SURGE / ("base" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        surge.base(out, {"up": ren.URI_SURGE + "base" + alia + ".conf"})

    with open(
        ren.PATH_OUT_SURGE / ("profile" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        surge.profile(out, {"base": "base" + alia + ".conf"})

    global __tmp_set
    if not "sc" in __tmp_set:
        __tmp_set.add("sc")
        copyfile(ren.PATH_SRC / "dumps" / "conv.conf", ren.PATH_OUT / "conv.conf")


def __shadowrocket(alia: str) -> None:
    shadowrocket.load(__raw)

    with open(
        ren.PATH_OUT / ("shadowrocket" + alia + ".conf"),
        "tw",
        encoding="utf-8",
    ) as out:
        shadowrocket.config(
            out,
            {
                "up": ren.URI_NET + "shadowrocket" + alia + ".conf",
            },
        )
