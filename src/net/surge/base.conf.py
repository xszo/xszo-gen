def o(line=""):
    out.write(line + "\n")


MapNode = {"direct": "DIRECT", "reject": "REJECT"}
for item in src["node"]:
    if "id" in item:
        MapNode[item["id"]] = item["name"]

o(
    "#!MANAGED-CONFIG "
    + src["meta"]["path"]
    + "surge/"
    + src["id"]
    + "base.conf"
    + " interval="
    + str(src["meta"]["interval"])
    + " strict=false"
)
o()
o("[General]")
o("loglevel = warning")
o("ipv6 = true")
o("ipv6-vif = auto")
# o("udp-priority = true")
# o("udp-policy-not-supported-behaviour = REJECT")
# o("exclude-simple-hostnames = true")
if "dns" in src["meta"]:
    o("hijack-dns = *:53")
    line = "dns-server = "
    for item in src["meta"]["dns"]:
        line += item + ", "
    o(line[:-2])
if "doh" in src["meta"]:
    o("encrypted-dns-server = " + src["meta"]["doh"])
o("internet-test-url = " + src["meta"]["test"])
o("proxy-test-url = " + src["meta"]["test"])
o("proxy-test-udp = " + src["meta"]["t-dns"])
o()
o("[Proxy Group]")
for item in src["node"]:
    line = item["name"]
    if item["type"] == "static":
        line += " = select"
    elif item["type"] == "test":
        line += " = url-test, hidden=true"
    else:
        continue
    if "list" in item:
        for val in item["list"]:
            if val[0] == "-":
                line += ", " + MapNode[val[1:]]
            else:
                line += ", " + val
    if "regx" in item:
        line += ', include-all-proxies=true, policy-regex-filter="' + item["regx"] + '"'
    o(line)
o()
o("[Rule]")
for item in src["filter"]["port"]:
    if item[0] == 1:
        o("DEST-PORT," + str(item[1]) + "," + MapNode[item[2]])
for item in src["filter"]["domain"]:
    if item[0] == 1:
        o("DOMAIN-SUFFIX," + item[1] + "," + MapNode[item[2]])
    elif item[0] == 2:
        o("DOMAIN," + item[1] + "," + MapNode[item[2]])
if "pre" in src["filter"]:
    for item in src["filter"]["pre"]["surge"]:
        if item[0] == 1:
            o("DOMAIN-SET," + item[1] + "," + MapNode[item[2]])
for item in src["filter"]["ipcidr"]:
    if item[0] == 1:
        o("IP-CIDR," + item[1] + "," + MapNode[item[2]])
    elif item[0] == 2:
        o("IP-CIDR6," + item[1] + "," + MapNode[item[2]])
for item in src["filter"]["ipgeo"]:
    if item[0] == 1:
        o("GEOIP," + item[1] + "," + MapNode[item[2]])
o("FINAL, " + MapNode[src["filter"]["main"]] + ", dns-failed")
