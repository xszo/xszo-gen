from pathlib import Path

import yaml


def let(key, val) -> None:
    with open(Path(key), "tw", encoding="utf-8") as __file:
        yaml.safe_dump(val, __file)


def get(key):
    with open(Path(key), "tr", encoding="utf-8") as __file:
        __res = yaml.safe_load(__file)
    return __res
