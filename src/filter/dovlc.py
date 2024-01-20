import re
from os import system
from pathlib import Path

import yaml

from .ren import Var


class Do:
    res = {}

    __var = {"rex": []}

    def __init__(self) -> None:
        self.__var["com"] = re.compile(Var.REX["comment"])
        for key, val in Var.REX.items():
            if key == "incl":
                self.__var["incl"] = (re.compile(val[0]), val[1])
            elif isinstance(val, list):
                self.__var["rex"].append((re.compile(val[0]), val[1]))

        if Path(Var.PATH["var.vlc"]).exists():
            system("cd " + Var.PATH["var.vlc"] + "; git pull --depth=1 -r;")
        else:
            Path(Var.PATH["tmp.vlc"]).mkdir(parents=True, exist_ok=True)
            system("git clone --depth=1 " + Var.EXT["vlc"] + " " + Var.PATH["tmp.vlc"])

    def get(self, dat: list) -> dict:
        for unit in dat:
            if len(unit := unit.split(" ")) < 2:
                continue
            raw = []
            for item in unit[1:]:
                with open(Var.PATH["var.vlc"] + item, "tr", encoding="utf-8") as file:
                    raw.extend(file.read().splitlines())
            res = []

            while True:
                tmp = []
                for item in raw:
                    if re.match(self.__var["com"], item):
                        continue
                    if line := re.match(self.__var["incl"][0], item):
                        with open(
                            Var.PATH["var.vlc"] + line.expand(self.__var["incl"][1]),
                            "tr",
                            encoding="utf-8",
                        ) as file:
                            tmp.extend(file.read().splitlines())
                    else:
                        for pat in self.__var["rex"]:
                            if line := re.match(pat[0], item):
                                res.append(line.expand(pat[1]))
                                break
                if tmp:
                    raw = tmp
                else:
                    break

            self.res["vlc" + unit[0]] = res
        return self.res

    def gen(self, dat: list) -> None:
        rex = []
        for item in self.__var["rex"]:
            if item[1][0] == "+":
                rex.append((item[0], item[1][2:]))
            else:
                rex.append((item[0], "-" + item[1]))

        no = {}
        for unit in dat:
            if len(unit := unit.split(" ")) < 2:
                continue
            raw = []
            for item in unit[1:]:
                with open(Var.PATH["var.vlc"] + item, "tr", encoding="utf-8") as file:
                    raw.extend(file.read().splitlines())
            res = []
            lo_no = []

            while True:
                tmp = []
                for item in raw:
                    if re.match(self.__var["com"], item):
                        continue
                    if line := re.match(self.__var["incl"][0], item):
                        with open(
                            Var.PATH["var.vlc"] + line.expand(self.__var["incl"][1]),
                            "tr",
                            encoding="utf-8",
                        ) as file:
                            tmp.extend(file.read().splitlines())
                    else:
                        for pat in rex:
                            if line := re.match(pat[0], item):
                                res.append(
                                    "- " + line.expand(pat[1]) + " # " + item + "\n"
                                )
                                break
                        else:
                            lo_no.append(item)
                if tmp:
                    raw = tmp
                else:
                    break

            no[unit[0]] = lo_no
            with open(
                Var.PATH["tmp"] + "vlc" + unit[0] + ".yml", "tw", encoding="utf-8"
            ) as file:
                file.write("domain:\n")
                file.writelines(res)

        with open(Var.PATH["tmp"] + "no-vlc.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(no, file)
