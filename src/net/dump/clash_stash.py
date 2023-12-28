from copy import deepcopy

import yaml


class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}

    def __init__(self, i_src):
        self.__src = deepcopy(i_src)
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def yml(self, out):
        with open("src/net/dump/clash_base.yml", "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)

        raw["dns"]["default-nameserver"] = [
            item + ":53" for item in self.__src["misc"]["dns"]
        ]
        if "doh" in self.__src["misc"]:
            raw["dns"]["nameserver"] = [self.__src["misc"]["doh"]]
        else:
            raw["dns"]["nameserver"] = raw["dns"]["default-nameserver"]

        raw["proxy-providers"] = {}
        proxy_list = []
        for idx, item in enumerate(self.__src["proxy"]["link"]):
            lo_name = "Proxy" + str(idx)
            proxy_list.append(lo_name)
            raw["proxy-providers"][lo_name] = {"url": item, "interval": 86400}

        raw["proxy-groups"] = []
        for item in self.__src["node"]:
            line = {"name": item["name"]}
            if item["type"] == "static":
                line["type"] = "select"
            elif item["type"] == "test":
                line.update(
                    {
                        "type": "url-test",
                        "lazy": True,
                        "hidden": True,
                        "interval": 600,
                        "url": self.__src["misc"]["test"],
                    }
                )
            else:
                continue
            if "icon" in item:
                line["icon"] = item["icon"]["emoji"]
            if "list" in item:
                line["proxies"] = [
                    self.__map_node[x[1:]] if x[0] == "-" else x for x in item["list"]
                ]
            if "regx" in item:
                line["include-all"] = True
                line["use"] = deepcopy(proxy_list)
                line["filter"] = item["regx"]
            raw["proxy-groups"].append(line)

        raw["rules"] = [
            "DST-PORT," + str(x[1]) + "," + self.__map_node[x[2]] if x[0] == 1 else None
            for x in self.__src["filter"]["port"]
        ] + [
            "DOMAIN-SUFFIX," + x[1] + "," + self.__map_node[x[2]]
            if x[0] == 1
            else "DOMAIN," + x[1] + "," + self.__map_node[x[2]]
            if x[0] == 2
            else None
            for x in self.__src["filter"]["domain"]
        ]
        if "pre" in self.__src["filter"]:
            raw["rules"] += [
                "RULE-SET," + x[3] + "," + self.__map_node[x[2]] if x[0] == 1 else None
                for x in self.__src["filter"]["pre"]["clash"]
            ]
        raw["rules"] += (
            [
                "IP-CIDR," + x[1] + "," + self.__map_node[x[2]]
                if x[0] == 1
                else "IP-CIDR6," + x[1] + "," + self.__map_node[x[2]]
                if x[0] == 2
                else None
                for x in self.__src["filter"]["ipcidr"]
            ]
            + [
                "GEOIP," + x[1] + "," + self.__map_node[x[2]] if x[0] == 1 else None
                for x in self.__src["filter"]["ipgeo"]
            ]
            + ["MATCH, " + self.__map_node[self.__src["filter"]["main"]]]
        )

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
