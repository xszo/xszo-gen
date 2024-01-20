import yaml

from .dodump import Do as do_dump
from .doget import Do as load_get
from .domix import Do as do_mix
from .dovlc import Do as load_vlc
from .ren import Var


def run() -> None:
    with open(Var.PATH["var.list"], "tr", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    res = {}
    res.update(load_get(data["var"]).get(data["get"]))
    res.update(load_vlc().get(data["vlc"]))
    do_dump(do_mix(res).mix(data["list"])).dump(data["tar"])

    if "gen" in data["tar"]:
        load_get(data["var"]).gen(data["get"])
        load_vlc().gen(data["vlc"])
