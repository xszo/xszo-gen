from pathlib import Path
from shutil import copyfile

import requests

from .dump.clash import dump as clash
from .dump.clash_convert import dump as clash_convert
from .dump.loon import dump as loon
from .dump.quantumult import dump as quantumult
from .dump.shadowrocket import dump as shadowrocket
from .dump.surge import dump as surge
from .ren import Var


class do:
    def __init__(self):
        Path(Var.PATH["out"]).mkdir(parents=True, exist_ok=True)
        Path(Var.PATH["out.surge"]).mkdir(parents=True, exist_ok=True)
        Path(Var.PATH["out.clash"]).mkdir(parents=True, exist_ok=True)

    def __rmt(self, loc: str, lnk: str):
        with open(Var.PATH["out"] + loc, "tw", encoding="utf-8") as file:
            file.write(requests.get(lnk, timeout=8).text)

    def dump(self, src: dict):
        var = src.pop("dump")
        if var["id"] != "":
            var["id"] = "+" + var["id"]

        if "quantumult" in var["tar"]:
            dp = quantumult(src)
            with open(
                Var.PATH["out"] + "quantumult" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.profile(
                    out,
                    {
                        "filter": var["uri"]
                        + Var.PATH["out.uri"]
                        + "quantumult-filter"
                        + var["id"]
                        + ".txt",
                        "parse": var["uri"]
                        + Var.PATH["out.uri"]
                        + "quantumult-parser.js",
                    },
                )
            with open(
                Var.PATH["out"] + "quantumult-filter" + var["id"] + ".txt",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.filter(out)
            self.__rmt(
                "quantumult-parser.js",
                Var.EXT["quantumult-parser"],
            )
        if "clash" in var["tar"]:
            dp = clash(src)
            with open(
                Var.PATH["out.clash"] + "profile" + var["id"] + ".yml",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.config(out)
            dp = clash_convert(src)
            with open(
                Var.PATH["out.clash"] + "conv" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.config(
                    out, {"yml": var["uri"] + "clash/conv-base" + var["id"] + ".yml"}
                )
            with open(
                Var.PATH["out.clash"] + "conv-base" + var["id"] + ".yml",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.base(out)
        if "surge" in var["tar"]:
            dp = surge(src)
            with open(
                Var.PATH["out.surge"] + "base" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.base(out, {"up": var["uri"] + "surge/base" + var["id"] + ".conf"})
            with open(
                Var.PATH["out.surge"] + "profile" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.profile(out, {"base": "base" + var["id"] + ".conf"})
            copyfile(Var.PATH["src"] + "dump/conv.conf", Var.PATH["out"] + "conv.conf")
        if "shadowrocket" in var["tar"]:
            dp = shadowrocket(src)
            with open(
                Var.PATH["out"] + "shadowrocket" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.config(
                    out,
                    {
                        "up": var["uri"]
                        + Var.PATH["out.uri"]
                        + "shadowrocket"
                        + var["id"]
                        + ".conf",
                    },
                )
        if "loon" in var["tar"]:
            dp = loon(src)
            with open(
                Var.PATH["out"] + "loon" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.profile(
                    out,
                    {
                        "parse": var["uri"] + Var.PATH["out.uri"] + "loon-parser.js",
                    },
                )
            self.__rmt(
                "loon-parser.js",
                Var.EXT["loon-parser"],
            )
