import re
from os import system

import yaml

from . import ren

# Var
res = {}
__var = {
    "rex-com": re.compile("^\\s*(#|!)"),
    "rex-incl": (re.compile("^include:([A-Za-z0-9\\-\\!]+)\\s*(?:#.*)?$"), "\\1"),
    "rex": [
        (
            re.compile(
                "^full:((?:[a-z0-9\\*](?:[a-z0-9\\-\\*]*[a-z0-9\\*])?\\.)*(?:[a-z]+|xn--[a-z0-9]+))(?:$|\\s)"
            ),
            "\\1",
        ),
        (
            re.compile(
                "^(?:domain:)?((?:[a-z0-9\\*](?:[a-z0-9\\-\\*]*[a-z0-9\\*])?\\.)*(?:[a-z]+|xn--[a-z0-9]+))(?:$|\\s)"
            ),
            ".\\1",
        ),
    ],
}


# Init
def init():
    # pull vlc repo
    if ren.VLC_REPO.exists():
        system("cd " + str(ren.VLC_REPO) + "; git pull -r --depth=1;")
    else:
        ren.VLC_REPO.mkdir(parents=True)
        system("git clone --depth=1 " + str(ren.VLC_URI) + " " + str(ren.VLC_REPO))


def __incl(loc: str) -> list:
    with open(ren.VLC_DATA / loc, "tr", encoding="utf-8") as file:
        dat = file.read().splitlines()
    return dat


def get(dat: list) -> dict:
    no = {}
    for name, val in dat.items():
        # parse lists
        raw = []
        for item in val:
            raw.extend(__incl(item))
        ret = []
        lo_no = []

        while True:
            tmp = []
            for item in raw:
                # comment
                if re.match(__var["rex-com"], item):
                    continue
                item = item.lower()
                # include
                if line := re.match(__var["rex-incl"][0], item):
                    tmp.extend(__incl(line.expand(__var["rex-incl"][1])))
                # parse
                else:
                    for pat in __var["rex"]:
                        if line := re.match(pat[0], item):
                            ret.append(line.expand(pat[1]))
                            break
                    else:
                        lo_no.append(item)
            # loop include
            if tmp:
                raw = tmp
            else:
                break
        # store list
        res["vlc" + name] = ret
        no[name] = lo_no

    with open(ren.PATH_TMP / "no-vlc.yml", "tw", encoding="utf-8") as file:
        yaml.safe_dump(no, file)

    return res
