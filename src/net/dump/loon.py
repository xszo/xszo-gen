class dump:
    __src = None

    def __init__(self, i_src):
        self.__src = i_src

    def profile(self, out, loc):
        def o(line=""):
            out.write(line + "\n")

        o("[General]")
        o("resource-parser = " + loc["parse"])
        if "dns" in self.__src["misc"]:
            o("hijack-dns = *:53")
            line = "dns-server = "
            for item in self.__src["misc"]["dns"]:
                line += item + ", "
            o(line[:-2])
        if "doh" in self.__src["misc"]:
            o("doh-server = " + self.__src["misc"]["doh"])
        o("proxy-test-url = " + self.__src["misc"]["test"])
        o()
        o("[MITM]")
        o()
        o("[Proxy]")
        o()
        o("[Remote Proxy]")
        proxy_list = ""
        for idx, item in enumerate(self.__src["proxy"]["link"]):
            o("Proxy" + str(idx) + " = " + item)
            proxy_list += "Proxy" + str(idx) + ", "
        o()
        o("[Remote Filter]")
        tmp_reg = []
        for item in self.__src["node"]:
            if "regx" in item:
                tmp_reg.append(item["regx"])
        for idx, item in enumerate(tmp_reg):
            o(
                "RegExp"
                + str(idx)
                + " = NameRegex, "
                + proxy_list
                + 'FilterKey="'
                + item
                + '"'
            )
        o()
        o("[Proxy Group]")
        map_node = {"direct": "DIRECT", "reject": "REJECT"}
        for item in self.__src["node"]:
            if "id" in item:
                map_node[item["id"]] = item["name"]
        tmp_reg = 0
        for item in self.__src["node"]:
            line = item["name"]
            if item["type"] == "static":
                line += " = select"
            elif item["type"] == "test":
                line += " = url-test"
            else:
                continue
            if "list" in item:
                for val in item["list"]:
                    if val[0] == "-":
                        line += ", " + map_node[val[1:]]
                    else:
                        line += ", " + val
            if "regx" in item:
                line += ", RegExp" + str(tmp_reg)
                tmp_reg += 1
            o(line)
        o()
        o("[Rule]")
        for item in self.__src["filter"]["domain"]:
            if item[0] == 1:
                o("DOMAIN-SUFFIX," + item[1] + "," + map_node[item[2]])
            elif item[0] == 2:
                o("DOMAIN," + item[1] + "," + map_node[item[2]])
        for item in self.__src["filter"]["ipcidr"]:
            if item[0] == 1:
                o("IP-CIDR," + item[1] + "," + map_node[item[2]])
            elif item[0] == 2:
                o("IP-CIDR6," + item[1] + "," + map_node[item[2]])
        for item in self.__src["filter"]["ipgeo"]:
            if item[0] == 1:
                o("GEOIP," + item[1] + "," + map_node[item[2]])
        o("FINAL, " + map_node[self.__src["filter"]["main"]])
        o()
        o("[Remote Rule]")
        if "pre" in self.__src["filter"]:
            for item in self.__src["filter"]["pre"]["surge"]:
                if item[0] == 1:
                    o(item[1] + ", policy=" + map_node[item[2]] + ", enabled=true")
