import yaml

from . import ren


class GetVar:
    res = {"domain": {}, "ip4": {}, "ip6": {}, "ipasn": {}, "ipgeo": {}}

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

            if "ipasn" in raw:
                self.res["ipasn"][loc] = [str(item) for item in raw["ipasn"]]

        return self.res


class Mixer:
    res = {}

    __raw = {}
    __dn_lv = range(1, 5)

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
            name = unit[0]

            tmp_excl = []
            for item in unit[1:]:
                if item[0] == "-":
                    tmp_excl.append(item[1:])
                else:
                    for k in keys:
                        if item in self.__raw[k]:
                            if name in self.res[k]:
                                self.res[k][name].update(self.__raw[k][item])
                            else:
                                self.res[k][name] = self.__raw[k][item]
            self.res["domain"][name] = self.__dn_mini(self.res["domain"][name])

            tmp_exdn = set()
            for item in tmp_excl:
                for k in keys:
                    if name in self.res[k]:
                        if item in self.__raw[k]:
                            if k == "domain":
                                tmp_exdn.update(self.__raw[k][item])
                            else:
                                self.res[k][name].difference(self.__raw[k][item])
                        elif item in self.res[k]:
                            if k == "domain":
                                tmp_exdn.update(self.res[k][item])
                            else:
                                self.res[k][name].difference(self.res[k][item])
            if len(tmp_exdn) > 0:
                self.res["domain"][name] = self.__dn_rm(
                    self.res["domain"][name], tmp_exdn
                )

    def get(self) -> dict:
        res = {}
        for k1, v1 in self.res.items():
            res[k1] = {}
            for k2, v2 in v1.items():
                res[k1][k2] = tuple(sorted(v2))
        return res

    def __dn_mini(self, raw: set | list) -> set:
        res = set()
        for i in self.__dn_lv:
            suffix = set(x for x in raw if x[0] == "." and x.count(".") == i)
            res.update(suffix)
            raw = set(
                x for x in raw if not ("." + ".".join(x.split(".")[-i:])) in suffix
            )
        res.update(raw)
        return res

    def __dn_rm(self, raw: set, rm: set):
        for i in self.__dn_lv:
            suffix = set(x for x in rm if x[0] == "." and x.count(".") == i)
            raw.difference(suffix)
            raw = set(
                x for x in raw if not ("." + ".".join(x.split(".")[-i:])) in suffix
            )
        return raw
