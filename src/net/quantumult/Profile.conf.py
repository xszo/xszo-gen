def o(line=""):
    out.write(line + "\n")


MapNode = {"direct": "DIRECT", "reject": "REJECT"}
for item in src["node"]:
    if "id" in item:
        MapNode[item["id"]] = item["name"]

o("[general]")
o("profile_img_url = " + src["meta"]["icon"])
o("resource_parser_url = " + src["meta"]["path"] + "quantumult/parser.js")
o("network_check_url = " + src["meta"]["test"])
o("server_check_url = " + src["meta"]["test"])
o()
o("[dns]")
if "dns" in src["meta"]:
    for item in src["meta"]["dns"]:
        o("server = " + item)
if "doh" in src["meta"]:
    o("doh-server = " + src["meta"]["doh"])
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
    src["meta"]["path"]
    + "quantumult/"
    + src["id"]
    + "filter.txt, tag=Filter, update-interval="
    + str(src["meta"]["interval"])
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
                + str(src["meta"]["interval"])
                + ", opt-parser=false, enabled=true"
            )
o()
o("[rewrite_local]")
o("[rewrite_remote]")
