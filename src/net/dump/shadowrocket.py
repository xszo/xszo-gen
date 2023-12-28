class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "proxy": "PROXY"}

    def __init__(self, i_src):
        self.__src = i_src
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def config(self, out, loc):
        def o(line=""):
            out.write(line + "\n")

        o("[General]")
        o("update-url = " + loc["up"])
        o()
        o("[Proxy Group]")
        for item in self.__src["node"]:
            line = item["name"]
            if item["type"] == "static":
                line += " = select"
            elif item["type"] == "test":
                line += " = url-test, url=" + self.__src["misc"]["test"]
            else:
                continue
            if "list" in item:
                for val in item["list"]:
                    if val[0] == "-":
                        line += ", " + self.__map_node[val[1:]]
                    else:
                        line += ", " + val
            if "regx" in item:
                line += ", policy-regex-filter=" + item["regx"]
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
        for item in self.__src["filter"]["ipcidr"]:
            if item[0] == 1:
                o("IP-CIDR," + item[1] + "," + self.__map_node[item[2]])
            elif item[0] == 2:
                o("IP-CIDR6," + item[1] + "," + self.__map_node[item[2]])
        for item in self.__src["filter"]["ipgeo"]:
            if item[0] == 1:
                o("GEOIP," + item[1] + "," + self.__map_node[item[2]])
        o("FINAL, " + self.__map_node[self.__src["filter"]["main"]])
