class dump:
    __src = None
    __map_node = {"direct": "DIRECT", "reject": "REJECT"}
    __var_rex = []

    def __init__(self, araw: dict) -> None:
        self.__src = araw
        for item in self.__src["node"]:
            if "id" in item:
                self.__map_node[item["id"]] = item["name"]

    def profile(self, out, loc: dict) -> None:
        raw = [
            "[General]",
            "resource-parser = " + loc["parse"],
            "internet-test-url = " + self.__src["misc"]["test"],
            "proxy-test-url = " + self.__src["misc"]["test"],
        ]
        if "dns" in self.__src["misc"]:
            line = "dns-server = "
            for item in self.__src["misc"]["dns"]:
                line += item + ", "
            raw.append(line[:-2])
        if "doh" in self.__src["misc"]:
            raw.append("doh-server = " + self.__src["misc"]["doh"])

        raw.append("\n[Mitm]")

        raw.append("\n[Proxy]")

        raw.append("\n[Proxy Chain]")

        raw.append("\n[Proxy Group]")
        tmp_idx_reg = 0
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
                        line += ", " + self.__map_node[val[1:]]
                    else:
                        line += ", " + val
            if "regx" in item:
                line += ", Rex" + str(tmp_idx_reg)
                tmp_idx_reg += 1
            if item["type"] == "test":
                line += ", url=" + self.__src["misc"]["test"] + ", interval=600"
            if "icon" in item:
                line += ", img-url=" + item["icon"]["sf"][:-7]
            raw.append(line)

        raw.append("\n[Rule]")
        raw.append("FINAL, " + self.__map_node[self.__src["filter"]["main"]])

        raw.append("\n[Remote Proxy]")
        raw.extend(
            [
                "Proxy"
                + str(idx)
                + " = "
                + item
                + ", parser-enabled=true, enabled=true"
                for idx, item in enumerate(self.__src["proxy"]["link"])
            ]
        )

        raw.append("\n[Remote Filter]")
        self.__var_rex = [item["regx"] for item in self.__src["node"] if "regx" in item]
        raw.extend(
            [
                "Rex" + str(idx) + ' = NameRegex, FilterKey="' + item + '"'
                for idx, item in enumerate(self.__var_rex)
            ]
        )

        raw.append("\n[Remote Rule]")
        raw.extend(
            [
                (
                    item[2]
                    + ", tag=DN"
                    + item[1]
                    + ", policy="
                    + self.__map_node[item[3]]
                    + ", parser-enabled=true, enabled=true"
                )
                for item in self.__src["filter"]["dn"]["surge"]
                if item[0] in set([1, 2])
            ]
            + [
                (
                    item[2]
                    + ", tag=IP"
                    + item[1]
                    + ", policy="
                    + self.__map_node[item[3]]
                    + ", parser-enabled=true, enabled=true"
                )
                for item in self.__src["filter"]["ip"]["surge"]
                if item[0] == 1
            ]
        )

        out.writelines([x + "\n" for x in raw])
