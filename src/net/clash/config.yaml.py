import yaml

with open("src/net/clash/base.yml", "tr", encoding="utf-8") as file:
    raw = yaml.safe_load(file)
raw["dns"]["default-nameserver"] = [item + ":53" for item in src["meta"]["dns"]]
raw["dns"]["nameserver"] = [src["meta"]["doh"]]

raw["proxy-groups"] = []
for item in src["node"]:
    line = {"name": item["name"]}
    if item["type"] == "static":
        line["type"] = "select"
    elif item["type"] == "test":
        line.update(
            {
                "type": "url-test",
                "lazy": True,
                "interval": 600,
                "url": src["meta"]["test"],
            }
        )
    else:
        continue
    if "list" in item:
        line["proxies"] = item["list"]
    if "regex" in item:
        line["include-all"] = True
        line["filter"] = item["regex"]
    raw["proxy-groups"].append(line)

raw["rules"] = []
for item in src["filter"]["port"]:
    match item[0]:
        case 1:
            raw["rules"].append("DST-PORT," + item[1] + "," + item[2])
if "pre" in src["filter"]:
    for item in src["filter"]["pre"]["clash"]:
        match item[0]:
            case 1:
                raw["rules"].append("RULE-SET," + item[1] + "," + item[2])
for item in src["filter"]["domain"]:
    match item[0]:
        case 1:
            raw["rules"].append("DOMAIN-SUFFIX," + item[1] + "," + item[2])
        case 2:
            raw["rules"].append("DOMAIN," + item[1] + "," + item[2])
for item in src["filter"]["ipcidr"]:
    match item[0]:
        case 1:
            raw["rules"].append("IP-CIDR," + item[1] + "," + item[2])
        case 2:
            raw["rules"].append("IP-CIDR6," + item[1] + "," + item[2])
for item in src["filter"]["ipgeo"]:
    match item[0]:
        case 1:
            raw["rules"].append("GEOIP," + item[1] + "," + item[2])
raw["rules"].append("MATCH, " + src["filter"]["main"])

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
