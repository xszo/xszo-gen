from copy import deepcopy

import yaml

MISC = {
    "redir-port": 8421,
    "mixed-port": 8422,
    "allow-lan": True,
    "bind-address": "*",
    "mode": "rule",
    "log-level": "warning",
    "external-controller": "0.0.0.0:8420",
    "secret": "00000000",
    "profile": {"store-selected": True, "store-fake-ip": True, "tracing": False},
    "dns": {
        "enable": True,
        "listen": "0.0.0.0:53",
        "use-hosts": True,
        "enhanced-mode": "fake-ip",
        "fake-ip-range": "198.18.0.1/16",
        "fake-ip-filter": ["+.lan", "+.local"],
        "default-nameserver": ["1.1.1.1"],
        "nameserver": ["1.1.1.1"],
        "nameserver-policy": {"captive.apple.com": "1.1.1.1"},
    },
    "tun": {
        "enable": True,
        "stack": "system",
        "dns-hijack": ["any:53"],
        "auto-route": True,
        "auto-redir": True,
        "auto-detect-interface": True,
    },
}


class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}

    def __init__(self, araw: dict) -> None:
        self.__src = deepcopy(araw)
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def config(self, out) -> None:
        raw = deepcopy(MISC)

        raw["dns"]["default-nameserver"] = [
            item + ":53" for item in self.__src["misc"]["dns"]
        ]
        if "doh" in self.__src["misc"]:
            raw["dns"]["nameserver"] = [self.__src["misc"]["doh"]]
        else:
            raw["dns"]["nameserver"] = deepcopy(raw["dns"]["default-nameserver"])

        raw["proxy-providers"] = {}
        proxy_list = []
        for idx, item in enumerate(self.__src["proxy"]["link"]):
            lo_name = "Proxy" + str(idx)
            proxy_list.append(lo_name)
            raw["proxy-providers"][lo_name] = {"url": item, "interval": 86400}

        def conv_n(item: dict) -> str:
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
                return None
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
            return line

        raw["proxy-groups"] = [conv_n(item) for item in self.__src["node"]]

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
                    "path": "./filter/ip" + item[1] + ".yml",
                }

        yaml.safe_dump(raw, out)
