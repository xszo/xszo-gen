import re
from pathlib import Path
from subprocess import run as prun

import yaml
from ren import Var


class Do:
    res = {}

    __var = {"rex": []}
    # __session = None

    def __init__(self) -> None:
        self.__var["com"] = re.compile(Var.REX["comment"])
        for key, val in Var.REX.items():
            if key == "incl":
                self.__var["incl"] = (re.compile(val[0]), val[1])
            elif isinstance(val, list):
                self.__var["rex"].append((re.compile(val[0]), val[1]))

        # self.__session = requests.Session()
        if Path(Var.PATH["var.vlc"]).exists():
            prun(
                "cd " + Var.PATH["var.vlc"] + "; git pull -r;",
                shell=True,
                check=True,
            )
        else:
            Path(Var.PATH["tmp.vlc"]).mkdir(parents=True, exist_ok=True)
            prun(
                ["git", "clone", Var.EXT["vlc"], Var.PATH["tmp.vlc"]],
                check=True,
            )

    def get(self, dat: list) -> dict:
        for unit in dat:
            if len(unit := unit.split(" ")) < 2:
                continue
            raw = []
            for item in unit[1:]:
                raw.extend(self.__incl(item))
            res = []

            while True:
                tmp = []
                for item in raw:
                    if re.match(self.__var["com"], item):
                        continue
                    if line := re.match(self.__var["incl"][0], item):
                        tmp.extend(self.__incl(line.expand(self.__var["incl"][1])))
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

    def __incl(self, name: str) -> list:
        # raw = self.__session.get(Var.EXT["vlc"] + name, timeout=4).text.splitlines()
        with open(Var.PATH["var.vlc"] + name, "tr", encoding="utf-8") as file:
            raw = file.read().splitlines()
        return raw

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
                raw.extend(self.__incl(item))
            res = []
            lo_no = []

            while True:
                tmp = []
                for item in raw:
                    if re.match(self.__var["com"], item):
                        continue
                    if line := re.match(self.__var["incl"][0], item):
                        tmp.extend(self.__incl(line.expand(self.__var["incl"][1])))
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
