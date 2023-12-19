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

prun(["mkdir", VAR["path"]["out"]], check=False)
prun(["mkdir", VAR["path"]["out.surge"]], check=False)
prun(["mkdir", VAR["path"]["out.clash"]], check=False)


def rmt(loc, lnk):
    with open(VAR["path"]["out"] + loc, "tw", encoding="utf-8") as file:
        file.write(requests.get(lnk, timeout=1000).text)


def cp(fo, to):
    prun(["cp", VAR["path"]["src"] + fo, VAR["path"]["out"] + to], check=True)


def do(dat):
    var = dat.pop("dump")
    if var["id"] != "":
        var["id"] += "-"

    if "quantumult" in var["tar"]:
        with open(
            VAR["path"]["out"] + var["id"] + "quantumult.conf",
            "tw",
            encoding="utf-8",
        ) as out:
            quantumult_profile(
                dat,
                out,
                locFilter=var["uri"]
                + VAR["path"]["out.uri"]
                + var["id"]
                + "quantumult-filter.txt",
                locParse=var["uri"] + VAR["path"]["out.uri"] + "quantumult-parser.js",
            )
        with open(
            VAR["path"]["out"] + var["id"] + "quantumult-filter.txt",
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
            VAR["path"]["out.clash"] + var["id"] + "stash.yml",
            "tw",
            encoding="utf-8",
        ) as out:
            clash_stash(dat, out)
        with open(
            VAR["path"]["out.clash"] + var["id"] + "scv.ini",
            "tw",
            encoding="utf-8",
        ) as out:
            clash_scv_ini(
                dat, out, locYml=var["uri"] + "clash/" + var["id"] + "scv.yml"
            )
        with open(
            VAR["path"]["out.clash"] + var["id"] + "scv.yml",
            "tw",
            encoding="utf-8",
        ) as out:
            clash_scv_yml(dat, out)
    if "surge" in var["tar"]:
        with open(
            VAR["path"]["out.surge"] + var["id"] + "base.conf",
            "tw",
            encoding="utf-8",
        ) as out:
            surge_base(dat, out, locUp=var["uri"] + "surge/" + var["id"] + "base.conf")
        cp("surge/profile.conf", "../surge/" + var["id"] + "Profile.conf")
        with open(
            VAR["path"]["out.surge"] + var["id"] + "Server.conf",
            "tw",
            encoding="utf-8",
        ) as out:
            surge_server(dat, out)
        cp("other/scv.ini", "scv.ini")
    if "shadowrocket" in var["tar"]:
        with open(
            VAR["path"]["out"] + var["id"] + "shadowrocket.conf",
            "tw",
            encoding="utf-8",
        ) as out:
            shadowrocket(
                dat,
                out,
                locUp=var["uri"]
                + VAR["path"]["out.uri"]
                + var["id"]
                + "shadowrocket.conf",
            )
    if "loon" in var["tar"]:
        with open(
            VAR["path"]["out"] + var["id"] + "loon.conf", "tw", encoding="utf-8"
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
