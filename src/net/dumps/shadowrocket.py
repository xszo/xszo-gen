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
                line += ", policy-regex-filter=" + item["regx"]
            return line

        raw.extend([conv_n(item) for item in self.__src["node"]])

        raw.append("\n[Rule]")

        raw.extend(
            [
                "RULE-SET, " + item[2] + ", " + self.__map_node[item[3]]
                for item in self.__src["filter"]["dn"]["surge"]
                if item[0] in set([1, 2])
            ]
            + [
                "RULE-SET, " + item[2] + ", " + self.__map_node[item[3]]
                for item in self.__src["filter"]["ip"]["surge"]
                if item[0] == 1
            ]
        )
        raw.append("FINAL, " + self.__map_node[self.__src["filter"]["main"]])

        out.writelines([x + "\n" for x in raw])
