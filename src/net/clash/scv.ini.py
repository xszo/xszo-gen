def o(line=""):
    out.write(line + "\n")


o("[custom]")
o("clash_rule_base=" + src["meta"]["path"] + "clash/" + src["id"] + "scv.yml")
for item in src["node"]:
    line = "custom_proxy_group=" + item["name"]
    if item["type"] == "static":
        line += "`select"
    elif item["type"] == "test":
        line += "`url-test"
    else:
        continue
    if "list" in item:
        for val in item["list"]:
            line += "`[]" + val
    if "regx" in item:
        line += "`" + item["regx"]
    if item["type"] == "test":
        line += "`" + src["meta"]["test"] + "`600"
    o(line)
o("enable_rule_generator=true")
o("overwrite_original_rules=true")
for item in src["filter"]["port"]:
    if item[0] == 1:
        o("ruleset=" + item[2] + ",[]DST-PORT," + str(item[1]))
if "pre" in src["filter"]:
    for item in src["filter"]["pre"]["clash"]:
        if item[0] == 1:
            o("ruleset=" + item[2] + ",[]RULE-SET," + item[3])
for item in src["filter"]["domain"]:
    if item[0] == 1:
        o("ruleset=" + item[2] + ",[]DOMAIN-SUFFIX," + item[1])
    elif item[0] == 2:
        o("ruleset=" + item[2] + ",[]DOMAIN," + item[1])
for item in src["filter"]["ipcidr"]:
    if item[0] == 1:
        o("ruleset=" + item[2] + ",[]IP-CIDR," + item[1])
    elif item[0] == 2:
        o("ruleset=" + item[2] + ",[]IP-CIDR6," + item[1])
for item in src["filter"]["ipgeo"]:
    if item[0] == 1:
        o("ruleset=" + item[2] + ",[]GEOIP," + item[1])
o("ruleset=" + src["filter"]["main"] + ",[]MATCH")
