import yaml


def dump(src, out):
    with open("src/net/clash/base.yml", "tr", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
    raw["dns"]["default-nameserver"] = [item + ":53" for item in src["misc"]["dns"]]
    if "doh" in src["misc"]:
        raw["dns"]["nameserver"] = [src["misc"]["doh"]]
    else:
        raw["dns"]["nameserver"] = raw["dns"]["default-nameserver"]

    if "pre" in src["filter"]:
        raw["rule-providers"] = {}
        for item in src["filter"]["pre"]["clash"]:
            if item[0] == 1:
                raw["rule-providers"][item[3]] = {
                    "behavior": "domain",
                    "type": "http",
                    "interval": src["misc"]["interval"],
                    "url": item[1],
                    "path": "./filter/" + item[3],
                }

    yaml.safe_dump(raw, out)
