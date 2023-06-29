def o(line=""):
    out.write(line + "\n")


o("[general]")
o("profile_img_url = " + src["meta"]["ico"])
o("resource_parser_url = " + src["meta"]["path"] + "quantumult/parser.js")
o("network_check_url = " + src["meta"]["test"])
o("server_check_url = " + src["meta"]["test"])
o()
o("[dns]")
for item in src["meta"]["dns"]:
    o("server = " + item)
o("doh-server = " + src["meta"]["doh"])
o()
o("[mitm]")
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
            line += ", " + val
    elif "regex" in item:
        line += ", server-tag-regex=" + item["regex"]
    o(line + ", img-url=" + item["ico-sf"])
o()
o("[filter_local]")
o("final, " + src["filter"]["main"])
o("[filter_remote]")
o(
    src["meta"]["path"]
    + "quantumult/"
    + src["id"]
    + "filter.txt, update-interval="
    + str(src["meta"]["int"])
)
if "pre" in src["filter"]:
    for item in src["filter"]["pre"]["quantumult"]:
        match item[0]:
            case 1:
                o(
                    src["meta"]["path"]
                    + "quantumult/"
                    + item[1]
                    + ", force-policy="
                    + item[2]
                    + ", update-interval="
                    + str(src["meta"]["int"])
                )
o()
o("[rewrite_local]")
o("[rewrite_remote]")
o()
o("[server_local]")
o("[server_remote]")
