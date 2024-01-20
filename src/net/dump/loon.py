class dump:
    __src = None

    __var = {"map": {"direct": "DIRECT", "reject": "REJECT"}}

    def __init__(self, i_src):
        self.__src = i_src

    def profile(self, out, loc):
        def o(line=""):
            out.write(line + "\n")

        o("[General]")
        o("resource-parser = " + loc["parse"])
        if "dns" in self.__src["misc"]:
            line = "dns-server = "
            for item in self.__src["misc"]["dns"]:
                line += item + ", "
            o(line[:-2])
        if "doh" in self.__src["misc"]:
            if self.__src["misc"]["doh"][:5] == "https":
                o("doh3-server = " + "h3" + self.__src["misc"]["doh"][5:])
            else:
                o("doh-server = " + self.__src["misc"]["doh"])
        o("proxy-test-url = " + self.__src["misc"]["test"])
        o()
        o("[Mitm]")
        o()
        o("[Proxy]")
        o()
        o("[Proxy Chain]")
        o()
        o("[Remote Proxy]")
        for idx, item in enumerate(self.__src["proxy"]["link"]):
            o("Proxy" + str(idx) + " = " + item)
        o()
        o("[Remote Filter]")
        self.__var["rex"] = []
        for item in self.__src["node"]:
            if "regx" in item:
                self.__var["rex"].append(item["regx"])
        for idx, item in enumerate(self.__var["rex"]):
            o("Rex" + str(idx) + " = NameRegex, " + 'FilterKey="' + item + '"')
        o()
        o("[Proxy Group]")
        for item in self.__src["node"]:
            if "id" in item:
                self.__var["map"][item["id"]] = item["name"]
        idx_reg = 0
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
                        line += ", " + self.__var["map"][val[1:]]
                    else:
                        line += ", " + val
            if "regx" in item:
                line += ", Rex" + str(idx_reg)
                idx_reg += 1
            if item["type"] == "test":
                line += ", url=" + self.__src["misc"]["test"] + ", interval=600"
            if "icon" in item:
                line += ", img-url=" + item["icon"]["sf"][:-7]
            o(line)
        o()
        o("[Rule]")
        for item in self.__src["filter"]["domain"]:
            if item[0] == 1:
                o("DOMAIN-SUFFIX," + item[1] + "," + self.__var["map"][item[2]])
            elif item[0] == 2:
                o("DOMAIN," + item[1] + "," + self.__var["map"][item[2]])
        for item in self.__src["filter"]["ipcidr"]:
            if item[0] == 1:
                o("IP-CIDR," + item[1] + "," + self.__var["map"][item[2]])
            elif item[0] == 2:
                o("IP-CIDR6," + item[1] + "," + self.__var["map"][item[2]])
        for item in self.__src["filter"]["ipgeo"]:
            if item[0] == 1:
                o("GEOIP," + item[1] + "," + self.__var["map"][item[2]])
        o("FINAL, " + self.__var["map"][self.__src["filter"]["main"]])
        o()
        o("[Remote Rule]")
        if "pre" in self.__src["filter"]:
            for item in self.__src["filter"]["pre"]["surge"]:
                if item[0] == 1:
                    o(
                        item[1]
                        + ", tag="
                        + item[3]
                        + ", policy="
                        + self.__var["map"][item[2]]
                        + ", parser-enable=true, enabled=true"
                    )
