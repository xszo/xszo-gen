import yaml

from . import ren


class Dump:
    __raw = None

    def __init__(self) -> None:
        (ren.PATH_OUT / "surge").mkdir(parents=True, exist_ok=True)
        (ren.PATH_OUT / "clash").mkdir(parents=True, exist_ok=True)

    def __ref(self) -> None:
        keys = tuple(self.__raw["domain"].keys())
        ref = {
            "list": {
                "domain": keys,
                "ipcidr": tuple(
                    set(list(self.__raw["ip4"].keys()) + list(self.__raw["ip6"].keys()))
                ),
            },
            "domain": {},
            "ipcidr": "ipcidr.yml",
            "misc": "misc.yml",
        }
        for k in keys:
            ref["domain"]["surge-" + k] = "surge/filter-" + k + ".txt"
            ref["domain"]["clash-" + k] = "clash/filter-" + k + ".yml"

        with open(ren.PATH_TMP / "list.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(ref, file)

    def __domain(self) -> None:
        for key, val in self.__raw["domain"].items():
            # dump clash
            with open(
                ren.PATH_OUT / "clash" / ("filter-" + key + ".yml"),
                "tw",
                encoding="utf-8",
            ) as file:
                yaml.safe_dump(
                    {"payload": ["+" + x if x[0] == "." else x for x in val]}, file
                )
            # dump surge
            with open(
                ren.PATH_OUT / "surge" / ("filter-" + key + ".txt"),
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines([x + "\n" for x in val])

    def __ipcidr(self) -> None:
        raw = {}
        for key, val in self.__raw["ip4"].items():
            raw[key] = [(1, item) for item in val]
        for key, val in self.__raw["ip6"].items():
            if not key in raw:
                raw[key] = []
            raw[key].extend([(2, item) for item in val])

        with open(ren.PATH_TMP / "ipcidr.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(raw, file)

    def __misc(self) -> None:
        raw = {}
        for key, val in self.__raw["ipgeo"].items():
            raw[key] = {}
            raw[key]["ipgeo"] = val

        with open(ren.PATH_TMP / "misc.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(raw, file)

    def dump(self, araw: dict) -> None:
        self.__raw = araw

        self.__ref()
        self.__domain()
        self.__ipcidr()
        self.__misc()
