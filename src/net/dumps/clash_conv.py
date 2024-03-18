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

        def conv(x: tuple) -> str:
            match x[0]:
                case 1:
                    return "DOMAIN," + x[1] + "," + self.__map_node[x[2]]
                case 2:
                    return "DOMAIN-SUFFIX," + x[1] + "," + self.__map_node[x[2]]
                case 9:
                    return "IP-CIDR," + x[1] + "," + self.__map_node[x[2]]
                case 10:
                    return "IP-CIDR6," + x[1] + "," + self.__map_node[x[2]]
                case 17:
                    return "GEOIP," + x[1] + "," + self.__map_node[x[2]]
                case _:
                    return None

        if "pre" in self.__src["filter"]:
            raw["rules"] = [
                "RULE-SET, " + x[3] + ", " + self.__map_node[x[2]]
                for x in self.__src["filter"]["pre"]["clash"]
                if x[0] in set([1, 2])
            ] + [conv(item) for item in self.__src["filter"]["misc"]]
        else:
            raw["rules"] = [conv(item) for item in self.__src["filter"]["list"]]
        raw["rules"].append("MATCH, " + self.__map_node[self.__src["filter"]["main"]])

        if "pre" in self.__src["filter"]:
            raw["rule-providers"] = {}
            for item in self.__src["filter"]["pre"]["clash"]:
                if item[0] in set([1, 2]):
                    raw["rule-providers"][item[3]] = {
                        "behavior": "domain",
                        "type": "http",
                        "interval": self.__src["misc"]["interval"],
                        "url": item[1],
                        "path": "./filter/" + item[3] + ".yml",
                    }

        yaml.safe_dump(raw, out)
