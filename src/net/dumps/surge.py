__src = {}
__map_node = {"direct": "DIRECT", "reject": "REJECT"}


def load(araw: dict) -> None:
    global __src, __map_node
    __src = araw
    for item in __src["node"]:
        if "id" in item:
            __map_node[item["id"]] = item["name"]


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
    raw = [
        "#!MANAGED-CONFIG "
        + loc["up"]
        + " interval="
        + str(__src["misc"]["interval"])
        + " strict=false",
        "\n",
        "[General]",
        "loglevel = warning",
        "auto-suspend = true",
        "ipv6 = true",
        "udp-priority = true",
        "udp-policy-not-supported-behaviour = REJECT",
        "allow-wifi-access = false",
        "exclude-simple-hostnames = true",
        "internet-test-url = " + __src["misc"]["test"],
        "proxy-test-url = " + __src["misc"]["test"],
        "proxy-test-udp = " + __src["misc"]["t-dns"],
    ]

    if "dns" in __src["misc"]:
        line = "dns-server = "
        for item in __src["misc"]["dns"]:
            line += item + ", "
        raw.extend(["hijack-dns = *:53", line[:-2]])
    if "doh" in __src["misc"]:
        raw.append(
            "encrypted-dns-server = " + __src["misc"]["doh"],
        )

    raw.append("\n[Proxy Group]")

    def conv_n(item: dict) -> str:
        line = item["name"]
        if item["type"] == "static":
            line += " = select"
        elif item["type"] == "test":
            line += ' = smart, hidden=true, policy-priority="\\[B\\]:8;"'
        else:
            return None
        if "list" in item:
            for val in item["list"]:
                if val[0] == "-":
                    line += ", " + __map_node[val[1:]]
                else:
                    line += ", " + val
        if "regx" in item:
            line += (
                ', include-all-proxies=true, policy-regex-filter="' + item["regx"] + '"'
            )
        return line

    raw.extend([conv_n(item) for item in __src["node"]])

    raw.append("\n[Rule]")

    raw.extend(
        [
            "RULE-SET, " + item[2] + ", " + __map_node[item[3]] + ", no-resolve"
            for item in __src["filter"]["dn"]["surge"]
            if item[0] in set([1, 2])
        ]
        + [
            "RULE-SET, " + item[2] + ", " + __map_node[item[3]]
            for item in __src["filter"]["ip"]["surge"]
            if item[0] == 1
        ]
    )
    raw.append("FINAL, " + __map_node[__src["filter"]["main"]] + ", dns-failed")

    out.writelines([x + "\n" for x in raw])
