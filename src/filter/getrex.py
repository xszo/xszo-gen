import re
from base64 import b64decode

import yaml

from ..lib import net
from . import ren

# Var
res = {}
__rex_var = []
__rex_com = re.compile(ren.REX_COM)

# Init
ren.PATH_TMP.mkdir(parents=True, exist_ok=True)


def var(avar: dict) -> None:
    # compile variable pattern
    for name, line in avar.items():
        __rex_var.append((re.compile("\\\\=" + name + "\\\\"), line))
    __rex_var.append((re.compile("\\\\=\\w*\\\\"), ""))


def get(dat: list) -> dict:
    no = {}
    for unit in dat:
        # load patterns and out
        rex = []
        for key, val in unit["reg"].items():
            # each sublist
            for item in val:
                # insert variables
                for v in __rex_var:
                    item = re.sub(v[0], v[1], item)
                # compile pattern
                item = item.split("  ")
                rex.append((re.compile(item[0]), item[1], key))
            # init res
            res[key] = []
        lo_no = []

        # get remote filter
        raw = net.get(unit["uri"])

        # pre process
        if "b64" in unit["pre"]:
            raw = b64decode(raw).decode("utf-8")

        # loop lines
        for item in raw.splitlines():
            if re.match(__rex_com, item):
                continue
            item = item.lower()
            for pat in rex:
                # find 1 and rewrite 2
                if line := re.match(pat[0], item):
                    res[pat[2]].append(line.expand(pat[1]))
                    break
            else:
                lo_no.append(item)
        no[unit["uri"]] = lo_no

    # dump no match
    with open(ren.PATH_TMP / "no-rex.yml", "tw", encoding="utf-8") as file:
        yaml.safe_dump(no, file)

    return res
