from pathlib import Path
from subprocess import run as prun

import requests
from clash.scv_ini import dump as clash_scv_ini
from clash.scv_yml import dump as clash_scv_yml
from clash.stash import dump as clash_stash
from other.loon import dump as loon
from other.shadowrocket import dump as shadowrocket
from quantumult.filter import dump as quantumult_filter
from quantumult.profile import dump as quantumult_profile
from surge.base import dump as surge_base
from surge.server import dump as surge_server

from var import VAR

Path(VAR["path"]["out"]).mkdir(parents=True, exist_ok=True)
Path(VAR["path"]["out.surge"]).mkdir(parents=True, exist_ok=True)
Path(VAR["path"]["out.clash"]).mkdir(parents=True, exist_ok=True)


def rmt(loc, lnk):
    with open(VAR["path"]["out"] + loc, "tw", encoding="utf-8") as file:
        file.write(requests.get(lnk, timeout=1000).text)


def cp(fo, to):
    prun(["cp", VAR["path"]["src"] + fo, VAR["path"]["out"] + to], check=True)


def do(dat):
    var = dat.pop("dump")
    if var["id"] != "":
        var["id"] = "-" + var["id"]

    if "quantumult" in var["tar"]:
        with open(
            VAR["path"]["out"] + "quantumult" + var["id"] + ".conf",
            "tw",
            encoding="utf-8",
        ) as out:
            quantumult_profile(
                dat,
                out,
                locFilter=var["uri"]
                + VAR["path"]["out.uri"]
                + "quantumult-filter"
                + var["id"]
                + ".txt",
                locParse=var["uri"] + VAR["path"]["out.uri"] + "quantumult-parser.js",
            )
        with open(
            VAR["path"]["out"] + "quantumult-filter" + var["id"] + ".txt",
            "tw",
            encoding="utf-8",
        ) as out:
            quantumult_filter(dat, out)
        rmt(
            "quantumult-parser.js",
            "https://raw.githubusercontent.com/KOP-XIAO/QuantumultX/master/Scripts/resource-parser.js",
        )
    if "clash" in var["tar"]:
        with open(
            VAR["path"]["out.clash"] + "Stash" + var["id"] + ".yml",
            "tw",
            encoding="utf-8",
        ) as out:
            clash_stash(dat, out)
        with open(
            VAR["path"]["out.clash"] + "scv" + var["id"] + ".ini",
            "tw",
            encoding="utf-8",
        ) as out:
            clash_scv_ini(
                dat, out, locYml=var["uri"] + "clash/scv" + var["id"] + ".yml"
            )
        with open(
            VAR["path"]["out.clash"] + "scv" + var["id"] + ".yml",
            "tw",
            encoding="utf-8",
        ) as out:
            clash_scv_yml(dat, out)
    if "surge" in var["tar"]:
        with open(
            VAR["path"]["out.surge"] + "base" + var["id"] + ".conf",
            "tw",
            encoding="utf-8",
        ) as out:
            surge_base(dat, out, locUp=var["uri"] + "surge/base" + var["id"] + ".conf")
        cp("surge/profile.conf", "../surge/Profile" + var["id"] + ".conf")
        with open(
            VAR["path"]["out.surge"] + "Server" + var["id"] + ".conf",
            "tw",
            encoding="utf-8",
        ) as out:
            surge_server(dat, out)
        cp("other/scv.ini", "scv.ini")
    if "shadowrocket" in var["tar"]:
        with open(
            VAR["path"]["out"] + "shadowrocket" + var["id"] + ".conf",
            "tw",
            encoding="utf-8",
        ) as out:
            shadowrocket(
                dat,
                out,
                locUp=var["uri"]
                + VAR["path"]["out.uri"]
                + "shadowrocket"
                + var["id"]
                + ".conf",
            )
    if "loon" in var["tar"]:
        with open(
            VAR["path"]["out"] + "loon" + var["id"] + ".conf", "tw", encoding="utf-8"
        ) as out:
            loon(
                dat,
                out,
                locParse=var["uri"] + VAR["path"]["out.uri"] + "loon-parser.js",
            )
        rmt(
            "loon-parser.js",
            "https://github.com/sub-store-org/Sub-Store/releases/latest/download/sub-store-parser.loon.min.js",
        )
