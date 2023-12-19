import yaml
from dodump import do as do_dump
from doload import do as do_load

from var import VAR

# load runtime data
with open(VAR["path"]["var.list"], "tr", encoding="utf-8") as file:
    Data = yaml.safe_load(file)

proLoad = do_load()

for item in Data["list"]:
    with open(VAR["path"]["var"] + item, "tr", encoding="utf-8") as file:
        proLoad.load(yaml.safe_load(file))
    do_dump(proLoad.res)
