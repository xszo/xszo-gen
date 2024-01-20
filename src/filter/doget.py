import re
from base64 import b64decode

import requests
import yaml

from .ren import Var


class Do:
    res = {}

    __var = {}

    def __init__(self, i_var: dict) -> None:
        # compile variable pattern
        tmp_re = []
        for name, line in i_var.items():
            tmp_re.append((re.compile("\\\\=" + name + "\\\\"), line))
        self.__var["var"] = tmp_re + [(re.compile("\\\\=\\w*\\\\"), "")]
        # comment line
        self.__var["com"] = re.compile(Var.REX["comment"])

    def get(self, dat: list) -> dict:
        for unit in dat:
            # load patterns and out
            rex = []
            for key, val in unit["reg"].items():
                # each sublist
                for item in val:
                    # insert variables
                    for v in self.__var["var"]:
                        item = re.sub(v[0], v[1], item)
                    # compile pattern
                    item = item.split("  ")
                    rex.append((re.compile(item[0]), item[1], key))
                self.res[key] = []

            # get remote filter
            raw = requests.get(unit["uri"], timeout=8).text

            # pre process
            if "b64" in unit["pre"]:
                raw = b64decode(raw).decode("utf-8")

            # loop lines
            for item in raw.splitlines():
                if re.match(self.__var["com"], item):
                    continue
                for pat in rex:
                    # find 1 and rewrite 2
                    if line := re.match(pat[0], item):
                        self.res[pat[2]].append(line.expand(pat[1]))
                        break

        return self.res

    def gen(self, dat: list) -> None:
        cc = {}
        cc_no = {}
        for unit in dat:
            lo_no = []
            rex = []
            for key, val in unit["reg"].items():
                for item in val:
                    for v in self.__var["var"]:
                        item = re.sub(v[0], v[1], item)
                    item = item.split("  ")
                    if item[1][0] == "+":
                        rex.append((re.compile(item[0]), item[1][2:], key))
                    else:
                        rex.append((re.compile(item[0]), "-" + item[1], key))
                cc[key] = []

            raw = requests.get(unit["uri"], timeout=8).text

            if "b64" in unit["pre"]:
                raw = b64decode(raw).decode("utf-8")

            for item in raw.splitlines():
                if re.match(self.__var["com"], item):
                    continue
                for pat in rex:
                    if line := re.match(pat[0], item):
                        cc[pat[2]].append(
                            "- " + line.expand(pat[1]) + " # " + item + "\n"
                        )
                        break
                else:
                    lo_no.append(item)

            for key, val in cc.items():
                with open(
                    Var.PATH["tmp"] + key + ".yml",
                    "tw",
                    encoding="utf-8",
                ) as file:
                    file.write("domain:\n")
                    file.writelines(val)

            cc_no[unit["uri"]] = lo_no
        with open(Var.PATH["tmp"] + "no-get.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(cc_no, file)
