class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}

    def __init__(self, araw: dict) -> None:
        self.__src = araw
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def profile(self, out, loc: dict) -> None:
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

    def base(self, out, loc: dict) -> None:
        raw = [
            "#!MANAGED-CONFIG "
            + loc["up"]
            + " interval="
            + str(self.__src["misc"]["interval"])
            + " strict=false"
        ]

        raw.extend(
            [
                "\n[General]",
                "loglevel = warning",
                # "ipv6 = true",
                # "ipv6-vif = auto",
                "udp-priority = true",
                "udp-policy-not-supported-behaviour = REJECT",
                "exclude-simple-hostnames = true",
                "allow-wifi-access = false"
            ]
        )
        if "dns" in self.__src["misc"]:
            line = "dns-server = "
            for item in self.__src["misc"]["dns"]:
                line += item + ", "
            raw.extend(["hijack-dns = *:53", line[:-2]])
        if "doh" in self.__src["misc"]:
            # raw.append("encrypted-dns-follow-outbound-mode = true")
            raw.append("encrypted-dns-server = " + self.__src["misc"]["doh"])
        raw.extend(
            [
                "internet-test-url = " + self.__src["misc"]["test"],
                "proxy-test-url = " + self.__src["misc"]["test"],
                "proxy-test-udp = " + self.__src["misc"]["t-dns"],
            ]
        )

        raw.append("\n[Proxy Group]")
        for item in self.__src["node"]:
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
                        line += ", " + self.__map_node[val[1:]]
                    else:
                        line += ", " + val
            if "regx" in item:
                line += (
                    ', include-all-proxies=true, policy-regex-filter="'
                    + item["regx"]
                    + '"'
                )
            raw.append(line)

        raw.append("\n[Rule]")
        raw.extend(
            [
                "DEST-PORT," + str(item[1]) + "," + self.__map_node[item[2]]
                if item[0] == 1
                else None
                for item in self.__src["filter"]["port"]
            ]
        )
        if "pre" in self.__src["filter"]:
            raw.extend(
                [
                    "DOMAIN-SET, " + item[1] + ", " + self.__map_node[item[2]]
                    if item[0] == 1
                    else None
                    for item in self.__src["filter"]["pre"]["surge"]
                ]
            )
        raw.extend(
            [
                "DOMAIN-SUFFIX," + item[1] + "," + self.__map_node[item[2]]
                if item[0] == 1
                else "DOMAIN," + item[1] + "," + self.__map_node[item[2]]
                if item[0] == 2
                else None
                for item in self.__src["filter"]["domain"]
            ]
        )
        raw.extend(
            [
                "IP-CIDR," + item[1] + "," + self.__map_node[item[2]]
                if item[0] == 1
                else "IP-CIDR6," + item[1] + "," + self.__map_node[item[2]]
                if item[0] == 2
                else None
                for item in self.__src["filter"]["ipcidr"]
            ]
        )
        raw.extend(
            [
                "GEOIP," + item[1] + "," + self.__map_node[item[2]]
                if item[0] == 1
                else None
                for item in self.__src["filter"]["ipgeo"]
            ]
        )
        raw.append(
            "FINAL, " + self.__map_node[self.__src["filter"]["main"]] + ", dns-failed"
        )

        out.writelines([x + "\n" for x in raw])
