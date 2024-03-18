import yaml

from . import ren


class Dump:
    def __init__(self) -> None:
        ren.PATH_OUT_CLASH.mkdir(parents=True, exist_ok=True)
        ren.PATH_OUT_SURGE.mkdir(parents=True, exist_ok=True)

    def dump(self, araw: dict) -> None:
        for key, val in araw.items():
            # dump clash
            with open(
                ren.PATH_OUT_CLASH / ("filter-" + key + ".yml"),
                "tw",
                encoding="utf-8",
            ) as file:
                yaml.safe_dump(
                    {"payload": ["+" + x if x[0] == "." else x for x in val]}, file
                )
            # dump surge
            with open(
                ren.PATH_OUT_SURGE / ("filter-" + key + ".txt"),
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines([x + "\n" for x in val])
