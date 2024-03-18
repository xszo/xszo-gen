import yaml

from . import ren


class GetVar:
    res = {}

    def get(self) -> dict:
        for ls in ren.PATH_VAR.iterdir():
            if ls == ren.PATH_VAR_LIST:
                continue

            with open(
                ls,
                "tr",
                encoding="utf-8",
            ) as file:
                raw = yaml.safe_load(file)
            if "domain" in raw:

                def conv(item):
                    if item[0] == "-":
                        return item[1:]
                    else:
                        return "." + item

                tmp_res = [conv(item) for item in raw["domain"]]
            else:
                continue

            self.res[ls.name.split(".")[0]] = tmp_res

        return self.res


class Mixer:
    res = {}

    __raw = {}

    def __init__(self, araw: dict) -> None:
        # store source filters
        for key, val in araw.items():
            self.__raw[key] = set(val)

    def mix(self, dat: list) -> dict:
        for unit in dat:
            # format list desc
            if len(unit := unit.split(" ")) < 2:
                continue
            # mix filters
            line = set()
            tmp_excl = []
            # include
            for item in unit[1:]:
                if item[0] == "-":
                    tmp_excl.append(item[1:])
                else:
                    line.update(self.__raw[item])
            # exclude
            for item in tmp_excl:
                line.difference(self.__raw[item])
            # return
            self.__raw[unit[0]] = line
            self.res[unit[0]] = tuple(line)
        return self.res
