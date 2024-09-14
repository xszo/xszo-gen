import yaml

from . import dump, load, ren


def run() -> None:
    # load runtime data
    with open(ren.PATH_VAR_LIST, "tr", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    with open(ren.PATH_VAR / data["base"], "tr", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
        raw["proxy"] = data["proxy"]
        load.base(raw)
    # generate files
    for item in data["list"]:
        with open(ren.PATH_VAR / item, "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
            dump.dump(load.load(raw))
