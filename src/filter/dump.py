import yaml

from . import ren


class Dump:
    __raw = None

    def __init__(self, araw: dict) -> None:
        # store raw {name: list}
        self.__raw = araw

    def dump(self, loc: list) -> None:
        for key, val in self.__raw.items():
            # dump clash
            if "clash" in loc:
                with open(
                    ren.PATH_OUT_CLASH / ("filter-" + key + ".yml"),
                    "tw",
                    encoding="utf-8",
                ) as file:
                    yaml.safe_dump({"payload": val}, file)
            # dump surge
            if "surge" in loc:
                with open(
                    ren.PATH_OUT_SURGE / ("filter-" + key + ".txt"),
                    "tw",
                    encoding="utf-8",
                ) as file:
                    file.writelines(
                        [x[1:] + "\n" if x[0] == "+" else x + "\n" for x in val]
                    )
