import yaml

from . import ren
from .dump import Dump
from .getrex import GetRex
from .getvlc import GetVlc
from .load import GetVar, Mixer


def run() -> None:
    with open(ren.PATH_VAR_LIST, "tr", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    val = GetVar().get()

    val["domain"].update(GetRex(data["var"]).get(data["get"]))
    val["domain"].update(GetVlc().get(data["vlc"]))

    mixer = Mixer(val)
    mixer.mix(data["list"])
    val = mixer.get()

    Dump().dump(val)
