class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}

    def __init__(self, i_src):
        self.__src = i_src
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def profile(self, out, loc):
        def o(line=""):
            out.write(line + "\n")

        o("[general]")
        o("profile_img_url = " + self.__src["misc"]["icon"])
        o("resource_parser_url = " + loc["parse"])
        o("network_check_url = " + self.__src["misc"]["test"])
        o("server_check_url = " + self.__src["misc"]["test"])
        o()
        o("[dns]")
        if "dns" in self.__src["misc"]:
            for item in self.__src["misc"]["dns"]:
                o("server = " + item)
        if "doh" in self.__src["misc"]:
            o("doh-server = " + self.__src["misc"]["doh"])
        o()
        o("[mitm]")
        o()
        o("[server_local]")
        o("[server_remote]")
        for idx, item in enumerate(self.__src["proxy"]["link"]):
            o(
                item
                + ", tag=Proxy"
                + str(idx)
                + ", update-interval=86400, opt-parser=true, enabled=true"
            )
        o()
        o("[policy]")
        for item in self.__src["node"]:
            if item["type"] == "static":
                line = "static = "
            elif item["type"] == "test":
                line = "url-latency-benchmark = "
            else:
                continue
            line += item["name"]
            if "list" in item:
                for val in item["list"]:
                    if val[0] == "-":
                        line += ", " + self.__map_node[val[1:]]
                    else:
                        line += ", " + val
            elif "regx" in item:
                line += ", server-tag-regex=" + item["regx"]
            if "icon" in item:
                line += ", img-url=" + item["icon"]["sf"]
            o(line)
        o()
        o("[filter_local]")
        o("final, " + self.__map_node[self.__src["filter"]["main"]])
        o("[filter_remote]")
        o(
            loc["filter"]
            + ", tag=Filter, update-interval="
            + str(self.__src["misc"]["interval"])
            + ", opt-parser=false, enabled=true"
        )
        if "pre" in self.__src["filter"]:
            for item in self.__src["filter"]["pre"]["quantumult"]:
                if item[0] == 1:
                    o(
                        item[1]
                        + ", tag="
                        + item[3]
                        + ", force-policy="
                        + self.__map_node[item[2]]
                        + ", update-interval="
                        + str(self.__src["misc"]["interval"])
                        + ", opt-parser=false, enabled=true"
                    )
        o()
        o("[rewrite_local]")
        o("[rewrite_remote]")

    def filter(self, out):
        out.writelines(
            [
                "host-suffix," + x[1] + "," + self.__map_node[x[2]] + "\n"
                if x[0] == 1
                else "host," + x[1] + "," + self.__map_node[x[2]] + "\n"
                if x[0] == 2
                else None
                for x in self.__src["filter"]["domain"]
            ]
            + [
                "ip-cidr," + x[1] + "," + self.__map_node[x[2]] + "\n"
                if x[0] == 1
                else "ip6-cidr," + x[1] + "," + self.__map_node[x[2]] + "\n"
                if x[0] == 2
                else None
                for x in self.__src["filter"]["ipcidr"]
            ]
            + [
                "geoip," + x[1] + "," + self.__map_node[x[2]] + "\n"
                if x[0] == 1
                else None
                for x in self.__src["filter"]["ipgeo"]
            ]
        )
