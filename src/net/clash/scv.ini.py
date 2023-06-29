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
    if "regex" in item:
        line += "`" + item["regex"]
    if item["type"] == "test":
        line += "`" + src["meta"]["test"] + "`600"
    o(line)
o("enable_rule_generator=true")
o("overwrite_original_rules=true")
for item in src["filter"]["port"]:
    match item[0]:
        case 1:
            o("ruleset=" + item[2] + ",[]DST-PORT," + item[1])
if "pre" in src["filter"]:
    for item in src["filter"]["pre"]["clash"]:
        match item[0]:
            case 1:
                o("ruleset=" + item[2] + ",[]RULE-SET," + item[1])
for item in src["filter"]["domain"]:
    match item[0]:
        case 1:
            o("ruleset=" + item[2] + ",[]DOMAIN-SUFFIX," + item[1])
        case 2:
            o("ruleset=" + item[2] + ",[]DOMAIN," + item[1])
for item in src["filter"]["ipcidr"]:
    match item[0]:
        case 1:
            o("ruleset=" + item[2] + ",[]IP-CIDR," + item[1])
        case 2:
            o("ruleset=" + item[2] + ",[]IP-CIDR6," + item[1])
for item in src["filter"]["ipgeo"]:
    match item[0]:
        case 1:
            o("ruleset=" + item[2] + ",[]GEOIP," + item[1])
o("ruleset=" + src["filter"]["main"] + ",[]MATCH")
