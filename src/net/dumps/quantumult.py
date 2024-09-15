res = {}
__src = {}
__var = {"map-node": {"direct": "direct", "proxy": "proxy", "reject": "reject"}}


def __node(src: dict, res: dict) -> None:
    res.append("\n[policy]")

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
                    line += ", " + __var["map-node"][val[1:]]
                else:
                    line += ", " + val
        elif "regx" in item:
            line += ", server-tag-regex=" + item["regx"]
        if "icon" in item:
            line += ", img-url=" + item["icon"]["sf"]
        return line

    res.extend([conv(item) for item in src["node"]])


def __filter(src: dict, res: dict) -> None:
    res.append("\n[filter_local]")
    res.append("final, " + __var["map-node"][src["filter"]["main"]])

    res.append("\n[filter_remote]")
    res.extend(
        [
            (
                item[2]
                + ", tag=DN"
                + item[1]
                + ", force-policy="
                + __var["map-node"][item[3]]
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
                + __var["map-node"][item[3]]
                + ", update-interval="
                + str(src["misc"]["interval"])
                + ", opt-parser=true, enabled=true"
            )
            for item in src["filter"]["ip"]["surge"]
            if item[0] == 1
        ]
    )


def let(lsrc: dict) -> None:
    global __src
    __src = lsrc
    for item in __src["node"]:
        if "id" in item:
            __var["map-node"][item["id"]] = item["name"]


def profile(out, loc: dict) -> None:
    global res
    res = [
        "[general]",
        "profile_img_url = " + __src["misc"]["icon"],
        "resource_parser_url = " + loc["parse"],
        "network_check_url = " + __src["misc"]["test"],
        "server_check_url = " + __src["misc"]["test"],
    ]

    res.append("\n[dns]")
    if "dns" in __src["misc"]:
        for item in __src["misc"]["dns"]:
            res.append("server = " + item)
    if "doh" in __src["misc"]:
        res.append("doh-server = " + __src["misc"]["doh"])

    res.append("\n[mitm]")

    __node(__src, res)
    __filter(__src, res)

    res.append("\n[rewrite_local]")
    res.append("\n[rewrite_remote]")

    res.append("\n[server_local]")
    res.append("\n[server_remote]")
    res.extend(
        [
            item + ", tag=Proxy, update-interval=86400, opt-parser=true, enabled=true"
            for item in __src["proxy"]["link"]
        ]
    )

    out.writelines([x + "\n" for x in res])
