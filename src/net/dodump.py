from pathlib import Path
from subprocess import run as prun

import requests
from dump.clash_scv import dump as clash_scv
from dump.clash_stash import dump as clash_stash
from dump.loon import dump as loon
from dump.quantumult import dump as quantumult
from dump.shadowrocket import dump as shadowrocket
from dump.surge import dump as surge
from ren import Var


class do:
    def __init__(self):
        Path(Var.PATH["out"]).mkdir(parents=True, exist_ok=True)
        Path(Var.PATH["out.surge"]).mkdir(parents=True, exist_ok=True)
        Path(Var.PATH["out.clash"]).mkdir(parents=True, exist_ok=True)

    def __rmt(self, loc: str, lnk: str):
        with open(Var.PATH["out"] + loc, "tw", encoding="utf-8") as file:
            file.write(requests.get(lnk, timeout=4).text)

    def __cp(self, fo: str, to: str):
        prun(["cp", Var.PATH["src"] + fo, Var.PATH["out"] + to], check=True)

    def dump(self, src: dict):
        var = src.pop("dump")
        if var["id"] != "":
            var["id"] = "-" + var["id"]

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
                "https://raw.githubusercontent.com/KOP-XIAO/QuantumultX/master/Scripts/resource-parser.js",
            )
        if "clash" in var["tar"]:
            dp = clash_stash(src)
            with open(
                Var.PATH["out.clash"] + "stash" + var["id"] + ".yml",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.yml(out)
            dp = clash_scv(src)
            with open(
                Var.PATH["out.clash"] + "scv" + var["id"] + ".ini",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.ini(out, {"yml": var["uri"] + "clash/scv" + var["id"] + ".yml"})
            with open(
                Var.PATH["out.clash"] + "scv" + var["id"] + ".yml",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.yml(out)
        if "surge" in var["tar"]:
            dp = surge(src)
            with open(
                Var.PATH["out.surge"] + "base" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.base(out, {"up": var["uri"] + "surge/base" + var["id"] + ".conf"})
            with open(
                Var.PATH["out.surge"] + "Profile" + var["id"] + ".conf",
                "tw",
                encoding="utf-8",
            ) as out:
                dp.profile(out, {"base": "base" + var["id"] + ".conf"})
            self.__cp("dump/scv.ini", "scv.ini")
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
                "https://github.com/sub-store-org/Sub-Store/releases/latest/download/sub-store-parser.loon.min.js",
            )
