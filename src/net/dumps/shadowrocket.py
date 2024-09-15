res = {}
__src = {}
__var = {"map-node": {"direct": "DIRECT", "proxy": "PROXY"}}


def let(lsrc: dict) -> None:
    global __src
    __src = lsrc
    for item in __src["node"]:
        if "id" in item:
            __var["map-node"][item["id"]] = item["name"]


def config(out, loc: dict) -> None:
    global res
    res = [
        "[General]",
        "update-url = " + loc["up"],
    ]

    res.append("\n[Proxy Group]")

    def conv_n(item: dict) -> str:
        line = item["name"]
        if item["type"] == "static":
            line += " = select"
        elif item["type"] == "test":
            line += " = url-test"
        else:
            return None
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += ", " + __var["map-node"][val[1:]]
                else:
                    line += ", " + val
        if "regx" in item:
            line += ", policy-regex-filter=" + item["regx"]
        return line

    res.extend([conv_n(item) for item in __src["node"]])

    res.append("\n[Rule]")

    res.extend(
        [
            "RULE-SET, " + item[2] + ", " + __var["map-node"][item[3]]
            for item in __src["filter"]["dn"]["surge"]
            if item[0] in set([1, 2])
        ]
        + [
            "RULE-SET, " + item[2] + ", " + __var["map-node"][item[3]]
            for item in __src["filter"]["ip"]["surge"]
            if item[0] == 1
        ]
    )
    res.append("FINAL, " + __var["map-node"][__src["filter"]["main"]])

    out.writelines([x + "\n" for x in res])
