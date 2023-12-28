import yaml
from dodump import do as do_dump
from doload import do as do_load

from var import VAR

# load runtime data
with open(VAR["path"]["var.list"], "tr", encoding="utf-8") as file:
    data = yaml.safe_load(file)

loader = do_load()
dumper = do_dump()

for item in data["list"]:
    with open(VAR["path"]["var"] + item, "tr", encoding="utf-8") as file:
        loader.load(yaml.safe_load(file))
    dumper.dump(loader.res)
