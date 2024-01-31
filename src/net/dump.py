from shutil import copyfile

import requests

from . import ren
from .dumps.clash import dump as clash
from .dumps.clash_convert import dump as clash_convert
# from .dumps.loon import dump as loon
from .dumps.quantumult import dump as quantumult
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
        if not "dump" in araw:
            return
        var = araw.pop("dump")
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
        # if "loon" in var["tar"]:
        #     self.__loon(var["id"])

    def __rmt(self, loc: str, lnk: str) -> None:
        with open(ren.PATH_OUT / loc, "tw", encoding="utf-8") as file:
            file.write(requests.get(lnk, timeout=8).text)

    def __quantumult(self, alia: str) -> None:
        dp = quantumult(self.__raw)

        with open(
            ren.PATH_OUT / ("quantumult" + alia + ".conf"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.profile(
                out,
                {
                    "filter": ren.URI_NET + "quantumult-filter" + alia + ".txt",
                    "parse": ren.URI_NET + "quantumult-parser.js",
                },
            )

        with open(
            ren.PATH_OUT / ("quantumult-filter" + alia + ".txt"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.filter(out)

        if not "qp" in self.__tmp_set:
            self.__tmp_set.add("qp")
            self.__rmt(
                "quantumult-parser.js",
                ren.EXT_QUANTUMULT_PARSER,
            )

    def __clash(self, alia: str) -> None:
        dp = clash(self.__raw)

        with open(
            ren.PATH_OUT_CLASH / ("profile" + alia + ".yml"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.config(out)

        dp = clash_convert(self.__raw)

        with open(
            ren.PATH_OUT_CLASH / ("conv" + alia + ".conf"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.config(out, {"yml": ren.URI_CLASH + "conv-base" + alia + ".yml"})

        with open(
            ren.PATH_OUT_CLASH / ("conv-base" + alia + ".yml"),
            "tw",
            encoding="utf-8",
        ) as out:
            dp.base(out)

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

    # def __loon(self, alia: str) -> None:
    #     dp = loon(self.__raw)

    #     with open(
    #         ren.PATH_OUT / ("loon" + alia + ".conf"),
    #         "tw",
    #         encoding="utf-8",
    #     ) as out:
    #         dp.profile(
    #             out,
    #             {
    #                 "parse": ren.URI_NET + "loon-parser.js",
    #             },
    #         )

    #     if not "lp" in self.__tmp_set:
    #         self.__tmp_set.add("lp")
    #         self.__rmt(
    #             "loon-parser.js",
    #             ren.EXT_LOON_PARSER,
    #         )
