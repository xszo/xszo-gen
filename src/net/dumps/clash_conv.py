from copy import deepcopy

import yaml

from .clash import MISC, __var, misc, rule

res = {}
__src = {}


def node(src: dict, res: dict) -> None:
    def conv(item: dict) -> str:
        line = "custom_proxy_group=" + item["name"]
        if item["type"] == "static":
            line += "`select"
        elif item["type"] == "test":
            line += "`url-test"
        else:
            return None
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += "`[]" + __var["map-node"][val[1:]]
                else:
                    line += "`[]" + val
        if "regx" in item:
            line += "`" + item["regx"]
        if item["type"] == "test":
            line += "`" + __src["misc"]["test"] + "`600"
        return line

    res.extend([conv(item) for item in src["node"]])


def let(lsrc: dict) -> None:
    global __src
    __src = deepcopy(lsrc)
    for item in __src["node"]:
        if "icon" in item:
            item["name"] = item["icon"]["emoji"] + item["name"]
        if "id" in item:
            __var["map-node"][item["id"]] = item["name"]


def config(out, loc: dict) -> None:
    global res
    res = [
        "[custom]",
        "clash_rule_base=" + loc["yml"],
        "enable_rule_generator=false",
    ]
    node(__src, res)

    out.writelines([x + "\n" for x in res])


def base(out) -> None:
    global res
    res = deepcopy(MISC)

    misc(__src, res)
    rule(__src, res)

    yaml.safe_dump(res, out)
