import yaml

from . import ren
from .dump import Dump
from .getrex import GetRex
from .getvlc import GetVlc
from .load import GetVar, Mixer


def run() -> None:
    with open(ren.PATH_VAR_LIST, "tr", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    res = {}
    res.update(GetRex(data["var"]).get(data["get"]))
    res.update(GetVlc().get(data["vlc"]))
    res.update(GetVar().get())

    res = Mixer(res).mix(data["list"])
    Dump().dump(res)
