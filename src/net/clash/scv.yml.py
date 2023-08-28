import yaml

with open("src/net/clash/base.yml", "tr", encoding="utf-8") as file:
    raw = yaml.safe_load(file)
raw["dns"]["default-nameserver"] = [item + ":53" for item in src["meta"]["dns"]]
raw["dns"]["nameserver"] = [src["meta"]["doh"]]

if "pre" in src["filter"]:
    raw["rule-providers"] = {}
    for item in src["filter"]["pre"]["clash"]:
        if item[0] == 1:
            raw["rule-providers"][item[3]] = {
                "behavior": "domain",
                "type": "http",
                "interval": src["meta"]["interval"],
                "url": item[1],
                "path": "./filter/" + item[3],
            }

yaml.safe_dump(raw, out)
