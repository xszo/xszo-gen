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
            + " strict=false",
            "\n",
            "[General]",
            "loglevel = warning",
            "auto-suspend = true",
            "ipv6 = true",
            # "ipv6-vif = auto",
            "udp-priority = true",
            "udp-policy-not-supported-behaviour = REJECT",
            "allow-wifi-access = false",
            "exclude-simple-hostnames = true",
            "show-error-page-for-reject = true",
            "internet-test-url = " + self.__src["misc"]["test"],
            "proxy-test-url = " + self.__src["misc"]["test"],
            "proxy-test-udp = " + self.__src["misc"]["t-dns"],
        ]

        if "dns" in self.__src["misc"]:
            line = "dns-server = "
            for item in self.__src["misc"]["dns"]:
                line += item + ", "
            raw.extend(["hijack-dns = *:53", line[:-2]])
        if "doh" in self.__src["misc"]:
            raw.append("encrypted-dns-follow-outbound-mode = true")
            raw.append("encrypted-dns-server = " + self.__src["misc"]["doh"])

        raw.append("\n[Proxy Group]")

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
                        line += ", " + self.__map_node[val[1:]]
                    else:
                        line += ", " + val
            if "regx" in item:
                line += (
                    ', include-all-proxies=true, policy-regex-filter="'
                    + item["regx"]
                    + '"'
                )
            return line

        raw.extend([conv_n(item) for item in self.__src["node"]])

        raw.append("\n[Rule]")

        def conv_f(item: tuple) -> str:
            match item[0]:
                case 1:
                    return "IP-CIDR," + item[1] + "," + self.__map_node[item[2]]
                case 2:
                    return "IP-CIDR6," + item[1] + "," + self.__map_node[item[2]]
                case 9:
                    return "GEOIP," + item[1] + "," + self.__map_node[item[2]]
                case _:
                    return None

        raw.extend(
            [
                "DOMAIN-SET, " + item[1] + ", " + self.__map_node[item[2]]
                for item in self.__src["filter"]["pre"]["surge"]
                if item[0] in set([1, 2])
            ]
            + [conv_f(item) for item in self.__src["filter"]["misc"]]
        )
        raw.append(
            "FINAL, " + self.__map_node[self.__src["filter"]["main"]] + ", dns-failed"
        )

        out.writelines([x + "\n" for x in raw])
