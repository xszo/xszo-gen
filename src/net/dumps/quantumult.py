class dump:
    __src = None
    __map_node = {"direct": "direct", "proxy": "proxy", "reject": "reject"}

    def __init__(self, araw: dict) -> None:
        self.__src = araw
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def profile(self, out, loc: dict) -> None:
        raw = [
            "[general]",
            "profile_img_url = " + self.__src["misc"]["icon"],
            "resource_parser_url = " + loc["parse"],
            "network_check_url = " + self.__src["misc"]["test"],
            "server_check_url = " + self.__src["misc"]["test"],
        ]

        raw.append("\n[dns]")
        if "dns" in self.__src["misc"]:
            for item in self.__src["misc"]["dns"]:
                raw.append("server = " + item)
        if "doh" in self.__src["misc"]:
            raw.append("doh-server = " + self.__src["misc"]["doh"])

        raw.append("\n[mitm]")

        raw.append("\n[policy]")
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
            raw.append(line)

        raw.extend(
            [
                "\n[filter_local]",
                "final, " + self.__map_node[self.__src["filter"]["main"]],
                "\n[filter_remote]",
                loc["filter"]
                + ", tag=Filter, update-interval="
                + str(self.__src["misc"]["interval"])
                + ", opt-parser=false, enabled=true",
            ]
        )
        if "pre" in self.__src["filter"]:
            raw.extend(
                [
                    (
                        item[1]
                        + ", tag="
                        + item[3]
                        + ", force-policy="
                        + self.__map_node[item[2]]
                        + ", update-interval="
                        + str(self.__src["misc"]["interval"])
                        + ", opt-parser=true, enabled=true"
                    )
                    for item in self.__src["filter"]["pre"]["surge"]
                    if item[0] == 1
                ]
            )

        raw.append("\n[rewrite_local]")
        raw.append("\n[rewrite_remote]")

        raw.append("\n[server_local]")
        raw.append("\n[server_remote]")
        raw.extend(
            [
                item
                + ", tag=Proxy, update-interval=86400, opt-parser=true, enabled=true"
                for item in self.__src["proxy"]["link"]
            ]
        )

        out.writelines([x + "\n" for x in raw])

    def filter(self, out) -> None:
        out.writelines(
            [
                (
                    "host-suffix," + item[1] + "," + self.__map_node[item[2]] + "\n"
                    if item[0] == 1
                    else (
                        "host," + item[1] + "," + self.__map_node[item[2]] + "\n"
                        if item[0] == 2
                        else None
                    )
                )
                for item in self.__src["filter"]["domain"]
            ]
            + [
                (
                    "ip-cidr," + item[1] + "," + self.__map_node[item[2]] + "\n"
                    if item[0] == 1
                    else (
                        "ip6-cidr," + item[1] + "," + self.__map_node[item[2]] + "\n"
                        if item[0] == 2
                        else None
                    )
                )
                for item in self.__src["filter"]["ipcidr"]
            ]
            + [
                (
                    "geoip," + item[1] + "," + self.__map_node[item[2]] + "\n"
                    if item[0] == 1
                    else None
                )
                for item in self.__src["filter"]["ipgeo"]
            ]
        )
