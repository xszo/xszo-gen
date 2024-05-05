from copy import deepcopy

import yaml

from .clash import MISC


class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}

    def __init__(self, araw: dict) -> None:
        self.__src = deepcopy(araw)
        for item in self.__src["node"]:
            if "icon" in item:
                item["name"] = item["icon"]["emoji"] + item["name"]
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def config(self, out, loc: dict) -> None:
        raw = [
            "[custom]",
            "clash_rule_base=" + loc["yml"],
            "enable_rule_generator=false",
        ]

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
                        line += "`[]" + self.__map_node[val[1:]]
                    else:
                        line += "`[]" + val
            if "regx" in item:
                line += "`" + item["regx"]
            if item["type"] == "test":
                line += "`" + self.__src["misc"]["test"] + "`600"
            return line

        raw.extend([conv(item) for item in self.__src["node"]])

        out.writelines([x + "\n" for x in raw])

    def base(self, out) -> None:
        raw = deepcopy(MISC)

        raw["dns"]["default-nameserver"] = [
            item + ":53" for item in self.__src["misc"]["dns"]
        ]
        if "doh" in self.__src["misc"]:
            raw["dns"]["nameserver"] = [self.__src["misc"]["doh"]]
        else:
            raw["dns"]["nameserver"] = deepcopy(raw["dns"]["default-nameserver"])

        raw["rules"] = [
            "RULE-SET, dn" + x[1] + ", " + self.__map_node[x[3]]
            for x in self.__src["filter"]["dn"]["clash"]
            if x[0] in set([1, 2])
        ] + [
            "RULE-SET, ip" + x[1] + ", " + self.__map_node[x[3]]
            for x in self.__src["filter"]["ip"]["clash"]
            if x[0] == 1
        ]
        raw["rules"].append("MATCH, " + self.__map_node[self.__src["filter"]["main"]])

        raw["rule-providers"] = {}
        for item in self.__src["filter"]["dn"]["clash"]:
            if item[0] in set([1, 2]):
                raw["rule-providers"]["dn" + item[1]] = {
                    "behavior": "domain",
                    "type": "http",
                    "interval": self.__src["misc"]["interval"],
                    "url": item[2],
                    "path": "./filter/dn" + item[1] + ".yml",
                }
        for item in self.__src["filter"]["ip"]["clash"]:
            if item[0] == 1:
                raw["rule-providers"]["ip" + item[1]] = {
                    "behavior": "classical",
                    "type": "http",
                    "interval": self.__src["misc"]["interval"],
                    "url": item[2],
                    "path": "./filter/ip" + item[3] + ".yml",
                }

        yaml.safe_dump(raw, out)
