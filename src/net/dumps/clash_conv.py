from copy import deepcopy

import yaml

from .clash import MISC, map_node, misc, rule

__src = {}


def node(src: dict, raw: dict) -> None:
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
                    line += "`[]" + map_node[val[1:]]
                else:
                    line += "`[]" + val
        if "regx" in item:
            line += "`" + item["regx"]
        if item["type"] == "test":
            line += "`" + __src["misc"]["test"] + "`600"
        return line

    raw.extend([conv(item) for item in src["node"]])


def init(araw: dict) -> None:
    global __src, map_node
    __src = deepcopy(araw)
    for item in __src["node"]:
        if "icon" in item:
            item["name"] = item["icon"]["emoji"] + item["name"]
        if "id" in item:
            map_node[item["id"]] = item["name"]


def config(out, loc: dict) -> None:
    raw = [
        "[custom]",
        "clash_rule_base=" + loc["yml"],
        "enable_rule_generator=false",
    ]
    node(__src, raw)

    out.writelines([x + "\n" for x in raw])


def base(out) -> None:
    raw = deepcopy(MISC)

    misc(__src, raw)
    rule(__src, raw)

    yaml.safe_dump(raw, out)
