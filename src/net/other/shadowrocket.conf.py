def o(line=""):
    out.write(line + "\n")


o("[General]")
o("update-url = " + src["meta"]["path"] + "other/" + src["id"] + "shadowrocket.conf")
o()
o("[Proxy Group]")
for item in src["node"]:
    line = item["name"] + " = "
    if item["type"] == "static":
        line += "select"
    elif item["type"] == "test":
        line += "url-test, url=" + src["meta"]["test"]
    else:
        continue
    if "list" in item:
        for val in item["list"]:
            line += ", " + val
    if "regex" in item:
        line += ", policy-regex-filter=" + item["regex"]
    o(line)
o()
o("[Rule]")
for item in src["filter"]["port"]:
    match item[0]:
        case 1:
            o("DEST-PORT," + item[1] + "," + item[2])
for item in src["filter"]["domain"]:
    match item[0]:
        case 1:
            o("DOMAIN-SUFFIX," + item[1] + "," + item[2])
        case 2:
            o("DOMAIN," + item[1] + "," + item[2])
for item in src["filter"]["ipcidr"]:
    match item[0]:
        case 1:
            o("IP-CIDR," + item[1] + "," + item[2])
        case 2:
            o("IP-CIDR6," + item[1] + "," + item[2])
for item in src["filter"]["ipgeo"]:
    match item[0]:
        case 1:
            o("GEOIP," + item[1] + "," + item[2])
o("FINAL, " + src["filter"]["main"])
