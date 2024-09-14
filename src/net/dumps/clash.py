from copy import deepcopy

import yaml

__src = {}

MISC = {
    "allow-lan": True,
    "bind-address": "*",
    "mode": "rule",
    "log-level": "warning",
    "ipv6": True,
    "external-controller": "0.0.0.0:9090",
    "secret": "00000000",
    "unified-delay": True,
    "tcp-concurrent": True,
    "geodata-mode": False,
    "geo-auto-update": True,
    "profile": {"store-selected": True, "store-fake-ip": True, "tracing": False},
    "dns": {
        "enable": True,
        "prefer-h3": True,
        "listen": "0.0.0.0:53",
        "use-hosts": True,
        "use-system-hosts": True,
        "default-nameserver": ["1.1.1.1"],
        "enhanced-mode": "fake-ip",
        "fake-ip-range": "198.18.0.1/16",
        "fake-ip-filter": ["+.lan", "+.local"],
        "nameserver": ["1.1.1.1"],
        "nameserver-policy": {"captive.apple.com": "1.1.1.1"},
        # "proxy-server-nameserver": None,
    },
    "sniffer": {
        "enable": True,
        "force-dns-mapping": True,
        "parse-pure-ip": True,
        "override-destination": False,
    },
    "port": 7890,
    "socks-port": 7891,
    "mixed-port": 7892,
    "redir-port": 7893,
    "tproxy-port": 7894,
    "tun": {
        "enable": True,
        "stack": "system",
        "auto-route": True,
        "auto-redir": True,
        "auto-detect-interface": True,
        "dns-hijack": ["udp://any:53", "tcp://any:53"],
    },
    "ntp": {
        "enable": True,
        "write-to-system": False,
        "server": "time.cloudflare.com",
        "port": 123,
        "interval": 60,
    },
}

map_node = {"direct": "DIRECT", "reject": "REJECT"}


def misc(src: dict, raw: dict) -> None:
    raw["dns"]["default-nameserver"] = [item + ":53" for item in src["misc"]["dns"]]
    if "doh" in src["misc"]:
        raw["dns"]["nameserver"] = [src["misc"]["doh"]]
    else:
        raw["dns"]["nameserver"] = deepcopy(raw["dns"]["default-nameserver"])


def node(src: dict, raw: dict) -> None:
    def conv(item: dict) -> str:
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
                    "url": src["misc"]["test"],
                }
            )
        else:
            return None
        if "icon" in item:
            line["icon"] = item["icon"]["emoji"]
        if "list" in item:
            line["proxies"] = [
                map_node[x[1:]] if x[0] == "-" else x for x in item["list"]
            ]
        if "regx" in item:
            line["include-all"] = True
            line["filter"] = item["regx"]
        return line

    raw["proxy-groups"] = [conv(item) for item in src["node"]]


def rule(src: dict, raw: dict) -> None:
    raw["rules"] = [
        "RULE-SET, dn" + x[1] + ", " + map_node[x[3]]
        for x in src["filter"]["dn"]["clash"]
        if x[0] in set([1, 2])
    ] + [
        "RULE-SET, ip" + x[1] + ", " + map_node[x[3]]
        for x in src["filter"]["ip"]["clash"]
        if x[0] == 1
    ]
    raw["rules"].append("MATCH, " + map_node[src["filter"]["main"]])

    raw["rule-providers"] = {}
    for item in src["filter"]["dn"]["clash"]:
        if item[0] in set([1, 2]):
            raw["rule-providers"]["dn" + item[1]] = {
                "behavior": "domain",
                "type": "http",
                "format": "text",
                "interval": src["misc"]["interval"],
                "url": item[2],
            }
    for item in src["filter"]["ip"]["clash"]:
        if item[0] == 1:
            raw["rule-providers"]["ip" + item[1]] = {
                "behavior": "classical",
                "type": "http",
                "format": "text",
                "interval": src["misc"]["interval"],
                "url": item[2],
            }


def load(araw: dict) -> None:
    global __src, map_node
    __src = deepcopy(araw)
    for item in __src["node"]:
        if "id" in item:
            map_node[item["id"]] = item["name"]


def config(out) -> None:
    raw = deepcopy(MISC)

    misc(__src, raw)
    node(__src, raw)
    rule(__src, raw)

    raw["proxy-providers"] = {}
    for idx, item in enumerate(__src["proxy"]["link"]):
        raw["proxy-providers"]["Proxy" + str(idx)] = {
            "type": "http",
            "url": item,
            "interval": 86400,
        }

    yaml.safe_dump(raw, out)
