def dump(src, out, locParse):
    def o(line=""):
        out.write(line + "\n")

    o("[General]")
    o("resource-parser = " + locParse)
    if "dns" in src["misc"]:
        o("hijack-dns = *:53")
        line = "dns-server = "
        for item in src["misc"]["dns"]:
            line += item + ", "
        o(line[:-2])
    if "doh" in src["misc"]:
        o("doh-server = " + src["misc"]["doh"])
    o("proxy-test-url = " + src["misc"]["test"])
    o()
    o("[MITM]")
    o()
    o("[Proxy]")
    o()
    o("[Remote Proxy]")
    ProxyAll = ""
    for idx, item in enumerate(src["proxy"]["link"]):
        o("Proxy" + str(idx) + " = " + item)
        ProxyAll += "Proxy" + str(idx) + ", "
    o()
    o("[Remote Filter]")
    tmpReg = []
    for item in src["node"]:
        if "regx" in item:
            tmpReg.append(item["regx"])
    for idx, item in enumerate(tmpReg):
        o(
            "RegExp"
            + str(idx)
            + " = NameRegex, "
            + ProxyAll
            + 'FilterKey="'
            + item
            + '"'
        )
    o()
    o("[Proxy Group]")
    MapNode = {"direct": "DIRECT", "reject": "REJECT"}
    for item in src["node"]:
        if "id" in item:
            MapNode[item["id"]] = item["name"]
    tmpReg = 0
    for item in src["node"]:
        line = item["name"]
        if item["type"] == "static":
            line += " = select"
        elif item["type"] == "test":
            line += " = url-test"
        else:
            continue
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += ", " + MapNode[val[1:]]
                else:
                    line += ", " + val
        if "regx" in item:
            line += ", RegExp" + str(tmpReg)
            tmpReg += 1
        o(line)
    o()
    o("[Rule]")
    for item in src["filter"]["domain"]:
        if item[0] == 1:
            o("DOMAIN-SUFFIX," + item[1] + "," + MapNode[item[2]])
        elif item[0] == 2:
            o("DOMAIN," + item[1] + "," + MapNode[item[2]])
    for item in src["filter"]["ipcidr"]:
        if item[0] == 1:
            o("IP-CIDR," + item[1] + "," + MapNode[item[2]])
        elif item[0] == 2:
            o("IP-CIDR6," + item[1] + "," + MapNode[item[2]])
    for item in src["filter"]["ipgeo"]:
        if item[0] == 1:
            o("GEOIP," + item[1] + "," + MapNode[item[2]])
    o("FINAL, " + MapNode[src["filter"]["main"]])
    o()
    o("[Remote Rule]")
    if "pre" in src["filter"]:
        for item in src["filter"]["pre"]["surge"]:
            if item[0] == 1:
                o(item[1] + ", policy=" + MapNode[item[2]] + ", enabled=true")
