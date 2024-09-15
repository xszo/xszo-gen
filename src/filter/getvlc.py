import re
from os import system

import yaml

from . import ren

# Var
res = {}
__rex = []
__rex_incl = (re.compile(ren.VLC_REX_INCL[0]), ren.VLC_REX_INCL[1])
__rex_com = re.compile(ren.REX_COM)

# Init
for item in ren.VLC_REX:
    __rex.append((re.compile(item[0]), item[1]))
# pull vlc repo
if ren.VLC_VAR.exists():
    system("cd " + str(ren.VLC_VAR) + "; git pull --depth=1 -r;")
else:
    ren.VLC_TMP.mkdir(parents=True, exist_ok=True)
    system("git clone --depth=1 " + str(ren.VLC_EXT) + " " + str(ren.VLC_TMP))


def __incl(loc: str) -> list:
    with open(ren.VLC_VAR / loc, "tr", encoding="utf-8") as file:
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
                if re.match(__rex_com, item):
                    continue
                item = item.lower()
                # include
                if line := re.match(__rex_incl[0], item):
                    tmp.extend(__incl(line.expand(__rex_incl[1])))
                # parse
                else:
                    for pat in __rex:
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
