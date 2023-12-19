def dump(src, out, locFilter, locParse):
    def o(line=""):
        out.write(line + "\n")

    MapNode = {"direct": "DIRECT", "reject": "REJECT"}
    for item in src["node"]:
        if "id" in item:
            MapNode[item["id"]] = item["name"]

    o("[general]")
    o("profile_img_url = " + src["misc"]["icon"])
    o("resource_parser_url = " + locParse)
    o("network_check_url = " + src["misc"]["test"])
    o("server_check_url = " + src["misc"]["test"])
    o()
    o("[dns]")
    if "dns" in src["misc"]:
        for item in src["misc"]["dns"]:
            o("server = " + item)
    if "doh" in src["misc"]:
        o("doh-server = " + src["misc"]["doh"])
    o()
    o("[mitm]")
    o()
    o("[server_local]")
    o("[server_remote]")
    for idx, item in enumerate(src["proxy"]["link"]):
        o(
            item
            + ", tag=Proxy"
            + str(idx)
            + ", update-interval=86400, opt-parser=true, enabled=true"
        )
    o()
    o("[policy]")
    for item in src["node"]:
        if item["type"] == "static":
            line = "static = "
        elif item["type"] == "test":
            line = "url-latency-benchmark = "
        else:
            continue
        line += item["name"]
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += ", " + MapNode[val[1:]]
                else:
                    line += ", " + val
        elif "regx" in item:
            line += ", server-tag-regex=" + item["regx"]
        if "icon" in item:
            line += ", img-url=" + item["icon"]["sf"]
        o(line)
    o()
    o("[filter_local]")
    o("final, " + MapNode[src["filter"]["main"]])
    o("[filter_remote]")
    o(
        locFilter
        + ", tag=Filter, update-interval="
        + str(src["misc"]["interval"])
        + ", opt-parser=false, enabled=true"
    )
    if "pre" in src["filter"]:
        for item in src["filter"]["pre"]["quantumult"]:
            if item[0] == 1:
                o(
                    item[1]
                    + ", tag="
                    + item[3]
                    + ", force-policy="
                    + MapNode[item[2]]
                    + ", update-interval="
                    + str(src["misc"]["interval"])
                    + ", opt-parser=false, enabled=true"
                )
    o()
    o("[rewrite_local]")
    o("[rewrite_remote]")
