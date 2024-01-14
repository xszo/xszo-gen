from pathlib import Path

import yaml
from dodump import Do as do_dump
from doget import Do as load_get
from domix import Do as do_mix
from dovlc import Do as load_vlc
from ren import Var

with open(Var.PATH["var.list"], "tr", encoding="utf-8") as file:
    data = yaml.safe_load(file)
Path(Var.PATH["tmp"]).mkdir(parents=True, exist_ok=True)

res = {}
res.update(load_get(data["var"]).get(data["get"]))
res.update(load_vlc().get(data["vlc"]))

do_dump(do_mix(res).mix(data["list"])).dump(data["tar"])
