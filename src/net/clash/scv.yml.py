import yaml

with open("src/net/clash/base.yml", "tr", encoding="utf-8") as file:
    raw = yaml.safe_load(file)
raw["dns"]["default-nameserver"] = [item + ":53" for item in src["meta"]["dns"]]
raw["dns"]["nameserver"] = [src["meta"]["doh"]]

if "pre" in src["filter"]:
    raw["rule-providers"] = {}
    for item in src["filter"]["pre"]["clash"]:
        match item[0]:
            case 1:
                raw["rule-providers"][item[1]] = {
                    "behavior": "domain",
                    "type": "http",
                    "interval": src["meta"]["int"],
                    "url": src["meta"]["path"] + "clash/" + item[1],
                    "path": "./filter/" + item[1],
                }

yaml.safe_dump(raw, out)
