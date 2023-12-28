class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}

    def __init__(self, i_src):
        self.__src = i_src
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def profile(self, out, loc):
        out.writelines(
            [
                "[General]\n",
                "#!include " + loc["base"] + "\n",
                "\n",
                "[Proxy]\n",
                "#!include proxy.conf\n",
                "\n",
                "[Proxy Group]\n",
                "#!include " + loc["base"] + "\n",
                "\n",
                "[Rule]\n",
                "#!include " + loc["base"] + "\n",
            ]
        )

    def base(self, out, loc):
        def o(line=""):
            out.write(line + "\n")

        o(
            "#!MANAGED-CONFIG "
            + loc["up"]
            + " interval="
            + str(self.__src["misc"]["interval"])
            + " strict=false"
        )
        o()
        o("[General]")
        o("loglevel = warning")
        # o("ipv6 = true")
        # o("ipv6-vif = auto")
        # o("udp-priority = true")
        # o("udp-policy-not-supported-behaviour = REJECT")
        # o("exclude-simple-hostnames = true")
        if "dns" in self.__src["misc"]:
            o("hijack-dns = *:53")
            line = "dns-server = "
            for item in self.__src["misc"]["dns"]:
                line += item + ", "
            o(line[:-2])
        if "doh" in self.__src["misc"]:
            # o("encrypted-dns-follow-outbound-mode = true")
            o("encrypted-dns-server = " + self.__src["misc"]["doh"])
        o("internet-test-url = " + self.__src["misc"]["test"])
        o("proxy-test-url = " + self.__src["misc"]["test"])
        o("proxy-test-udp = " + self.__src["misc"]["t-dns"])
        o()
        o("[Proxy Group]")
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
            o(line)
        o()
        o("[Rule]")
        for item in self.__src["filter"]["port"]:
            if item[0] == 1:
                o("DEST-PORT," + str(item[1]) + "," + self.__map_node[item[2]])
        for item in self.__src["filter"]["domain"]:
            if item[0] == 1:
                o("DOMAIN-SUFFIX," + item[1] + "," + self.__map_node[item[2]])
            elif item[0] == 2:
                o("DOMAIN," + item[1] + "," + self.__map_node[item[2]])
        if "pre" in self.__src["filter"]:
            for item in self.__src["filter"]["pre"]["surge"]:
                if item[0] == 1:
                    o("DOMAIN-SET," + item[1] + "," + self.__map_node[item[2]])
        for item in self.__src["filter"]["ipcidr"]:
            if item[0] == 1:
                o("IP-CIDR," + item[1] + "," + self.__map_node[item[2]])
            elif item[0] == 2:
                o("IP-CIDR6," + item[1] + "," + self.__map_node[item[2]])
        for item in self.__src["filter"]["ipgeo"]:
            if item[0] == 1:
                o("GEOIP," + item[1] + "," + self.__map_node[item[2]])
        o("FINAL, " + self.__map_node[self.__src["filter"]["main"]] + ", dns-failed")
