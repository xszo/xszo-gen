from copy import deepcopy

import yaml


class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}

    def __init__(self, i_src):
        self.__src = deepcopy(i_src)
        for item in self.__src["node"]:
            if "icon" in item:
                item["name"] = item["icon"]["emoji"] + item["name"]
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def ini(self, out, loc):
        def o(line=""):
            out.write(line + "\n")

        o("[custom]")
        o("clash_rule_base=" + loc["yml"])
        for item in self.__src["node"]:
            line = "custom_proxy_group=" + item["name"]
            if item["type"] == "static":
                line += "`select"
            elif item["type"] == "test":
                line += "`url-test"
            else:
                continue
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
            o(line)

        o("enable_rule_generator=true")
        o("overwrite_original_rules=true")
        for item in self.__src["filter"]["port"]:
            if item[0] == 1:
                o("ruleset=" + self.__map_node[item[2]] + ",[]DST-PORT," + str(item[1]))
        for item in self.__src["filter"]["domain"]:
            if item[0] == 1:
                o("ruleset=" + self.__map_node[item[2]] + ",[]DOMAIN-SUFFIX," + item[1])
            elif item[0] == 2:
                o("ruleset=" + self.__map_node[item[2]] + ",[]DOMAIN," + item[1])
        if "pre" in self.__src["filter"]:
            for item in self.__src["filter"]["pre"]["clash"]:
                if item[0] == 1:
                    o("ruleset=" + self.__map_node[item[2]] + ",[]RULE-SET," + item[3])
        for item in self.__src["filter"]["ipcidr"]:
            if item[0] == 1:
                o("ruleset=" + self.__map_node[item[2]] + ",[]IP-CIDR," + item[1])
            elif item[0] == 2:
                o("ruleset=" + self.__map_node[item[2]] + ",[]IP-CIDR6," + item[1])
        for item in self.__src["filter"]["ipgeo"]:
            if item[0] == 1:
                o("ruleset=" + self.__map_node[item[2]] + ",[]GEOIP," + item[1])
        o("ruleset=" + self.__map_node[self.__src["filter"]["main"]] + ",[]MATCH")

    def yml(self, out):
        with open("src/net/dump/clash_base.yml", "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)

        raw["dns"]["default-nameserver"] = [
            item + ":53" for item in self.__src["misc"]["dns"]
        ]
        if "doh" in self.__src["misc"]:
            raw["dns"]["nameserver"] = [self.__src["misc"]["doh"]]
        else:
            raw["dns"]["nameserver"] = deepcopy(raw["dns"]["default-nameserver"])

        if "pre" in self.__src["filter"]:
            raw["rule-providers"] = {}
            for item in self.__src["filter"]["pre"]["clash"]:
                if item[0] == 1:
                    raw["rule-providers"][item[3]] = {
                        "behavior": "domain",
                        "type": "http",
                        "interval": self.__src["misc"]["interval"],
                        "url": item[1],
                        "path": "./filter/" + item[3],
                    }

        yaml.safe_dump(raw, out)
