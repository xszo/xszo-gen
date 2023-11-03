import yaml

MapNode = {"direct": "DIRECT", "reject": "REJECT"}
for item in src["node"]:
    if "icon" in item:
        item["name"] = item["icon"]["emoji"] + item["name"]
    if "id" in item:
        MapNode[item["id"]] = item["name"]

with open("src/net/clash/base.yml", "tr", encoding="utf-8") as file:
    raw = yaml.safe_load(file)
raw["dns"]["default-nameserver"] = [item + ":53" for item in src["meta"]["dns"]]
if "doh" in src["meta"]:
    raw["dns"]["nameserver"] = [src["meta"]["doh"]]
else:
    raw["dns"]["nameserver"] = raw["dns"]["default-nameserver"]

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
    if "regx" in item:
        line["include-all"] = True
        line["filter"] = item["regx"]
    raw["proxy-groups"].append(line)

raw["rules"] = []
for item in src["filter"]["port"]:
    if item[0] == 1:
        raw["rules"].append("DST-PORT," + str(item[1]) + "," + MapNode[item[2]])
if "pre" in src["filter"]:
    for item in src["filter"]["pre"]["clash"]:
        if item[0] == 1:
            raw["rules"].append("RULE-SET," + item[3] + "," + MapNode[item[2]])
for item in src["filter"]["domain"]:
    if item[0] == 1:
        raw["rules"].append("DOMAIN-SUFFIX," + item[1] + "," + MapNode[item[2]])
    elif item[0] == 2:
        raw["rules"].append("DOMAIN," + item[1] + "," + MapNode[item[2]])
for item in src["filter"]["ipcidr"]:
    if item[0] == 1:
        raw["rules"].append("IP-CIDR," + item[1] + "," + MapNode[item[2]])
    elif item[0] == 2:
        raw["rules"].append("IP-CIDR6," + item[1] + "," + MapNode[item[2]])
for item in src["filter"]["ipgeo"]:
    if item[0] == 1:
        raw["rules"].append("GEOIP," + item[1] + "," + MapNode[item[2]])
raw["rules"].append("MATCH, " + MapNode[src["filter"]["main"]])

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

raw["proxy-providers"] = {}
for idx, item in enumerate(src["proxy"]["link"]):
    raw["proxy-providers"]["Proxy" + str(idx)] = {"url": item, "interval": 86400}

yaml.safe_dump(raw, out)
