import yaml

from . import ren


class GetVar:
    res = {"domain": {}, "ip4": {}, "ip6": {}, "ipgeo": {}}

    def get(self) -> dict:
        for ls in ren.PATH_VAR.iterdir():
            if ls == ren.PATH_VAR_LIST:
                continue
            loc = ls.name.split(".")[0]

            with open(
                ls,
                "tr",
                encoding="utf-8",
            ) as file:
                raw = yaml.safe_load(file)

            if "domain" in raw:

                def conv_domain(item: str) -> str:
                    if item[0] == "-":
                        return item[1:]
                    else:
                        return "." + item

                self.res["domain"][loc] = [conv_domain(item) for item in raw["domain"]]

            if "ipcidr" in raw:
                tmp = [line for line in raw["ipcidr"] if not line[0] == "["]
                if len(tmp) > 0:
                    self.res["ip4"][loc] = tmp

                tmp = [line[1:-1] for line in raw["ipcidr"] if line[0] == "["]
                if len(tmp) > 0:
                    self.res["ip6"][loc] = tmp

            if "ipgeo" in raw:
                self.res["ipgeo"][loc] = [item.upper() for item in raw["ipgeo"]]

        return self.res


class Mixer:
    res = {}

    __raw = {}

    def __init__(self, araw: dict) -> None:
        for k1, v1 in araw.items():
            self.__raw[k1] = {}
            for k2, v2 in v1.items():
                self.__raw[k1][k2] = set(v2)

    def mix(self, dat: list) -> None:
        keys = self.__raw.keys()
        for k in keys:
            self.res[k] = {}

        for unit in dat:
            # format list desc
            if len(unit := unit.split(" ")) < 2:
                continue

            tmp = unit[0]
            tmp_excl = []

            for item in unit[1:]:
                if item[0] == "-":
                    tmp_excl.append(item[1:])
                else:
                    for k in keys:
                        if item in self.__raw[k]:
                            if tmp in self.res[k]:
                                self.res[k][tmp].update(self.__raw[k][item])
                            else:
                                self.res[k][tmp] = self.__raw[k][item]

            for item in tmp_excl:
                for k in keys:
                    if item in self.__raw[k]:
                        self.res[k][tmp].difference(self.__raw[k][item])

    def get(self) -> dict:
        res = {}
        for k1, v1 in self.res.items():
            res[k1] = {}
            for k2, v2 in v1.items():
                res[k1][k2] = tuple(v2)
        return res
