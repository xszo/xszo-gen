__src = {}

map_node = {"direct": "direct", "proxy": "proxy", "reject": "reject"}


def node(src: dict, raw: dict) -> None:
    raw.append("\n[policy]")

    def conv(item: dict) -> str:
        if item["type"] == "static":
            line = "static = "
        elif item["type"] == "test":
            line = "url-latency-benchmark = "
        else:
            return None
        line += item["name"]
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += ", " + map_node[val[1:]]
                else:
                    line += ", " + val
        elif "regx" in item:
            line += ", server-tag-regex=" + item["regx"]
        if "icon" in item:
            line += ", img-url=" + item["icon"]["sf"]
        return line

    raw.extend([conv(item) for item in src["node"]])


def filter(src: dict, raw: dict) -> None:
    raw.append("\n[filter_local]")
    raw.append("final, " + map_node[src["filter"]["main"]])

    raw.append("\n[filter_remote]")
    raw.extend(
        [
            (
                item[2]
                + ", tag=DN"
                + item[1]
                + ", force-policy="
                + map_node[item[3]]
                + ", update-interval="
                + str(src["misc"]["interval"])
                + ", opt-parser=true, enabled=true"
            )
            for item in src["filter"]["dn"]["surge"]
            if item[0] in set([1, 2])
        ]
        + [
            (
                item[2]
                + ", tag=IP"
                + item[1]
                + ", force-policy="
                + map_node[item[3]]
                + ", update-interval="
                + str(src["misc"]["interval"])
                + ", opt-parser=true, enabled=true"
            )
            for item in src["filter"]["ip"]["surge"]
            if item[0] == 1
        ]
    )


def load(araw: dict) -> None:
    global __src, map_node
    __src = araw
    for item in __src["node"]:
        if "id" in item:
            map_node[item["id"]] = item["name"]


def profile(out, loc: dict) -> None:
    raw = [
        "[general]",
        "profile_img_url = " + __src["misc"]["icon"],
        "resource_parser_url = " + loc["parse"],
        "network_check_url = " + __src["misc"]["test"],
        "server_check_url = " + __src["misc"]["test"],
    ]

    raw.append("\n[dns]")
    if "dns" in __src["misc"]:
        for item in __src["misc"]["dns"]:
            raw.append("server = " + item)
    if "doh" in __src["misc"]:
        raw.append("doh-server = " + __src["misc"]["doh"])

    raw.append("\n[mitm]")

    node(__src, raw)
    filter(__src, raw)

    raw.append("\n[rewrite_local]")
    raw.append("\n[rewrite_remote]")

    raw.append("\n[server_local]")
    raw.append("\n[server_remote]")
    raw.extend(
        [
            item + ", tag=Proxy, update-interval=86400, opt-parser=true, enabled=true"
            for item in __src["proxy"]["link"]
        ]
    )

    out.writelines([x + "\n" for x in raw])
