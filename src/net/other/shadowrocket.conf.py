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
    if "regx" in item:
        line += ", policy-regex-filter=" + item["regx"]
    o(line)
o()
o("[Rule]")
for item in src["filter"]["port"]:
    if item[0] == 1:
        o("DEST-PORT," + str(item[1]) + "," + item[2])
for item in src["filter"]["domain"]:
    if item[0] == 1:
        o("DOMAIN-SUFFIX," + item[1] + "," + item[2])
    elif item[0] == 2:
        o("DOMAIN," + item[1] + "," + item[2])
for item in src["filter"]["ipcidr"]:
    if item[0] == 1:
        o("IP-CIDR," + item[1] + "," + item[2])
    elif item[0] == 2:
        o("IP-CIDR6," + item[1] + "," + item[2])
for item in src["filter"]["ipgeo"]:
    if item[0] == 1:
        o("GEOIP," + item[1] + "," + item[2])
o("FINAL, " + src["filter"]["main"])
