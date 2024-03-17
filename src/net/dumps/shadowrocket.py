class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "proxy": "PROXY"}

    def __init__(self, araw: dict) -> None:
        self.__src = araw
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def config(self, out, loc: dict) -> None:
        raw = [
            "[General]",
            "update-url = " + loc["up"],
        ]

        raw.append("\n[Proxy Group]")
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
            raw.append(line)

        raw.append("\n[Rule]")
        raw.extend(
            [
                (
                    "DOMAIN-SUFFIX," + item[1] + "," + self.__map_node[item[2]]
                    if item[0] == 1
                    else (
                        "DOMAIN," + item[1] + "," + self.__map_node[item[2]]
                        if item[0] == 2
                        else None
                    )
                )
                for item in self.__src["filter"]["domain"]
            ]
            + [
                (
                    "IP-CIDR," + item[1] + "," + self.__map_node[item[2]]
                    if item[0] == 1
                    else (
                        "IP-CIDR6," + item[1] + "," + self.__map_node[item[2]]
                        if item[0] == 2
                        else None
                    )
                )
                for item in self.__src["filter"]["ipcidr"]
            ]
            + [
                (
                    "GEOIP," + item[1] + "," + self.__map_node[item[2]]
                    if item[0] == 1
                    else None
                )
                for item in self.__src["filter"]["ipgeo"]
            ]
        )
        raw.append("FINAL, " + self.__map_node[self.__src["filter"]["main"]])

        out.writelines([x + "\n" for x in raw])
