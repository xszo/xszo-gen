import re
from base64 import b64decode

import requests

from . import ren


class GetRex:
    res = {}

    __rex_var = []
    __rex_com = None

    def __init__(self, avar: dict) -> None:
        # compile variable pattern
        for name, line in avar.items():
            self.__rex_var.append((re.compile("\\\\=" + name + "\\\\"), line))
        self.__rex_var.append((re.compile("\\\\=\\w*\\\\"), ""))
        # comment line
        self.__rex_com = re.compile(ren.REX_COM)

    def get(self, dat: list) -> dict:
        for unit in dat:
            # load patterns and out
            rex = []
            for key, val in unit["reg"].items():
                # each sublist
                for item in val:
                    # insert variables
                    for v in self.__rex_var:
                        item = re.sub(v[0], v[1], item)
                    # compile pattern
                    item = item.split("  ")
                    rex.append((re.compile(item[0]), item[1], key))
                # init res
                self.res[key] = []

            # get remote filter
            raw = requests.get(unit["uri"], timeout=8).text

            # pre process
            if "b64" in unit["pre"]:
                raw = b64decode(raw).decode("utf-8")

            # loop lines
            for item in raw.splitlines():
                if re.match(self.__rex_com, item):
                    continue
                for pat in rex:
                    # find 1 and rewrite 2
                    if line := re.match(pat[0], item):
                        self.res[pat[2]].append(line.expand(pat[1]))
                        break

        return self.res
