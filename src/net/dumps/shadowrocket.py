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

        def conv_n(item: dict) -> str:
            line = item["name"]
            if item["type"] == "static":
                line += " = select"
            elif item["type"] == "test":
                line += " = url-test, url=" + self.__src["misc"]["test"]
            else:
                return None
            if "list" in item:
                for val in item["list"]:
                    if val[0] == "-":
                        line += ", " + self.__map_node[val[1:]]
                    else:
                        line += ", " + val
            if "regx" in item:
                line += ", policy-regex-filter=" + item["regx"]
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
        raw.append("FINAL, " + self.__map_node[self.__src["filter"]["main"]])

        out.writelines([x + "\n" for x in raw])
