res = {}
__src = {}
__var = {"map-node": {"direct": "DIRECT", "reject": "REJECT"}}


def let(lsrc: dict) -> None:
    global __src
    __src = lsrc
    for item in __src["node"]:
        if "id" in item:
            __var["map-node"][item["id"]] = item["name"]


def profile(out, loc: dict) -> None:
    out.writelines(
        [
            "[General]\n",
            "#!include " + loc["base"] + "\n",
            "\n[Proxy]\n",
            "#!include proxy.conf\n",
            "\n[Proxy Group]\n",
            "#!include " + loc["base"] + "\n",
            "\n[Rule]\n",
            "#!include " + loc["base"] + "\n",
        ]
    )


def base(out, loc: dict) -> None:
    global res
    res = [
        "#!MANAGED-CONFIG "
        + loc["up"]
        + " interval="
        + str(__src["misc"]["interval"])
        + " strict=false",
        "\n",
        #
        "[General]",
        "loglevel = warning",
        "internet-test-url = " + __src["misc"]["test"],
        "proxy-test-url = " + __src["misc"]["test"],
        "proxy-test-udp = " + __src["misc"]["t-dns"],
    ]

    if "dns" in __src["misc"]:
        line = "dns-server = system"
        for item in __src["misc"]["dns"]:
            line += ", " + item
        res.append(line)
    if "doh" in __src["misc"]:
        res.append(
            "encrypted-dns-server = " + __src["misc"]["doh"],
        )

    res.append("\n[Proxy Group]")

    def conv_n(item: dict) -> str:
        line = item["name"]
        if item["type"] == "static":
            line += " = select"
        elif item["type"] == "test":
            line += ' = smart, policy-priority="\\[B\\]:8;"'
        else:
            return None
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += ", " + __var["map-node"][val[1:]]
                else:
                    line += ", " + val
        if "regx" in item:
            line += (
                ', include-all-proxies=true, policy-regex-filter="' + item["regx"] + '"'
            )
        return line

    res.extend([conv_n(item) for item in __src["node"]])

    res.append("\n[Rule]")

    res.extend(
        [
            "RULE-SET, "
            + item[2]
            + ", "
            + __var["map-node"][item[3]]
            + ", no-resolve, extended-matching"
            for item in __src["filter"]["dn"]["surge"]
            if item[0] in set([1, 2])
        ]
        + [
            "RULE-SET, " + item[2] + ", " + __var["map-node"][item[3]]
            for item in __src["filter"]["ip"]["surge"]
            if item[0] == 1
        ]
    )
    res.append("FINAL, " + __var["map-node"][__src["filter"]["main"]] + ", dns-failed")

    out.writelines([x + "\n" for x in res])
