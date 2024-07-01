from shutil import copyfile

import requests

from . import ren
from .dumps import clash_conv, quantumult
from .dumps.shadowrocket import dump as shadowrocket
from .dumps.surge import dump as surge


class Dump:
    __raw = None
    __tmp_set = set()

    def __init__(self) -> None:
        ren.PATH_OUT.mkdir(parents=True, exist_ok=True)
        ren.PATH_OUT_SURGE.mkdir(parents=True, exist_ok=True)
        ren.PATH_OUT_CLASH.mkdir(parents=True, exist_ok=True)

    def dump(self, araw: dict) -> None:
        if not "ref" in araw:
            return
        var = araw.pop("ref")
        if var["id"] != "":
            var["id"] = "+" + var["id"]
        self.__raw = araw

        if "quantumult" in var["tar"]:
            self.__quantumult(var["id"])
        if "clash" in var["tar"]:
            self.__clash(var["id"])
        if "surge" in var["tar"]:
            self.__surge(var["id"])
        if "shadowrocket" in var["tar"]:
            self.__shadowrocket(var["id"])

    def __rmt(self, loc: str, lnk: str) -> None:
        with open(ren.PATH_OUT / loc, "tw", encoding="utf-8") as file:
            file.write(requests.get(lnk, timeout=8).text)

    def __quantumult(self, alia: str) -> None:
        quantumult.init(self.__raw)

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

        if not "qp" in self.__tmp_set:
            self.__tmp_set.add("qp")
            self.__rmt(
                "quantumult-parser.js",
                ren.EXT_QUANTUMULT_PARSER,
            )

    def __clash(self, alia: str) -> None:
        clash_conv.init(self.__raw)

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

    def __surge(self, alia: str) -> None:
        dp = surge(self.__raw)

        with open(
            ren.PATH_OUT_SURGE / ("base" + alia + ".conf"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.base(out, {"up": ren.URI_SURGE + "base" + alia + ".conf"})

        with open(
            ren.PATH_OUT_SURGE / ("profile" + alia + ".conf"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.profile(out, {"base": "base" + alia + ".conf"})

        if not "sc" in self.__tmp_set:
            self.__tmp_set.add("sc")
            copyfile(ren.PATH_SRC / "dumps" / "conv.conf", ren.PATH_OUT / "conv.conf")

    def __shadowrocket(self, alia: str) -> None:
        dp = shadowrocket(self.__raw)

        with open(
            ren.PATH_OUT / ("shadowrocket" + alia + ".conf"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.config(
                out,
                {
                    "up": ren.URI_NET + "shadowrocket" + alia + ".conf",
                },
            )
