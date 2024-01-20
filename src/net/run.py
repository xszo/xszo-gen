import yaml

from .dodump import do as do_dump
from .doload import do as do_load
from .ren import Var


def run() -> None:
    # load runtime data
    with open(Var.PATH["var.list"], "tr", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    loader = do_load()
    dumper = do_dump()

    for item in data["list"]:
        with open(Var.PATH["var"] + item, "tr", encoding="utf-8") as file:
            dumper.dump(loader.load(yaml.safe_load(file)))
