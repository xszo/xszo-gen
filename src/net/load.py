from copy import deepcopy

import yaml

from . import ren


class Load:
    res = {}

    __base = {}
    __rex = None
    __tmp_var = {}

    def __init__(self) -> None:
        # load var
        with open(ren.PATH_VAR_REX, "tr", encoding="utf-8") as file:
            self.__rex = yaml.safe_load(file)

    # load base profile
    def base(self, araw: dict) -> None:
        self.__base = araw
        self.__base["ref"] = {}
        # load common
        with open(ren.PATH_VAR_BASE, "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        self.__base["misc"].update(
            {
                "interval": raw["int"],
                "icon": raw["ico"],
            }
        )
        # load sections
        if "id" in self.__base:
            self.__base["ref"]["id"] = self.__base.pop("id")
        if "var" in self.__base:
            self.__tmp_var.update(self.__base.pop("var"))

    # load data from file
    def load(self, araw: dict) -> None:
        # load sections
        if "tar" in araw:
            self.res = deepcopy(self.__base)
            self.res["ref"]["tar"] = araw.pop("tar")
        else:
            self.res = {}
            return

        if "id" in araw:
            self.res["ref"]["id"] = araw["id"]
        if "var" in araw:
            self.__tmp_var.update(araw["var"])
        if "misc" in araw:
            self.res["misc"].update(araw["misc"])
        if "route" in araw:
            self.res["route"] = self.__insert(self.res["route"], araw["route"])
        if "node" in araw:
            self.res["node"] = self.__insert(self.res["node"], araw["node"])
        self.__tmp_var["node"] = [x["name"] for x in self.res["node"]]
        # load modules
        self.__load_route()
        self.__load_node()
        self.__load_filter()
        self.__load_proxy()
        return self.res

    # t insert ls2 into ls1 with template
    def __insert(self, ls1: list, ls2: list) -> list:
        res = []
        for item in ls2:
            if isinstance(item, str):
                if item == "=":
                    res.extend(ls1)
                if item[0] == "-":
                    res.append(ls1[int(item[1:])])
            else:
                res.append(item)
        return res

    # convert route list to node and filter
    def __load_route(self) -> None:
        tmp_node = []
        tmp_filter = []
        for item in self.res["route"]:
            # node
            if "id" in item["node"]:
                # refer existing node
                lo_id = item["node"]["id"]
            else:
                lo_id = item["id"]
                # format node
                lo_node = {
                    "id": lo_id,
                    "type": item["node"]["type"],
                    "name": item["node"]["name"],
                    "list": item["node"]["list"],
                }
                if "icon" in item:
                    lo_node["icon"] = item["icon"]
                tmp_node.append(lo_node)
            # filter
            for idx, line in enumerate(item["filter"]):
                lo_filter = {
                    "id": item["id"] + str(idx),
                    "node": lo_id,
                }
                # type
                if "type" in line:
                    lo_filter.update(line)
                elif "use" in line:
                    lo_filter["type"] = "use"
                    lo_filter["use"] = line["use"]
                elif "link" in line:
                    lo_filter["type"] = "link"
                    lo_filter["link"] = line["link"]
                tmp_filter.append(lo_filter)
        # append
        tmp_node.extend(self.res["node"])
        self.res["node"] = tmp_node
        self.res["filter"] = tmp_filter
        del self.res["route"]

    # ins inline var, format list val
    def __load_node(self) -> None:
        for item in self.res["node"]:
            if isinstance(item["list"], list):
                # plain list
                tmp = []
                for sth in item["list"]:
                    # replace variable
                    if sth[0] == "=":
                        tmp.extend(self.__tmp_var[sth[1:]])
                    else:
                        tmp.append(sth)
                item["list"] = tmp
            else:
                # regex match
                if item["list"][0] == "=":
                    item["regx"] = self.__rex[item.pop("list")[1:]]
                else:
                    item["regx"] = item.pop("list")

    # get filter content from file and optimize
    def __load_filter(self) -> None:
        with open(ren.PATH_TMP_FILTER_LIST, "tr", encoding="utf-8") as file:
            ref = yaml.safe_load(file)

        tmp_dn = {"surge": [], "clash": []}
        tmp_ip = {"surge": [], "clash": []}

        for item in self.res["filter"]:
            if item["type"] == "main":
                tmp_main = item["node"]

            elif item["type"] == "use":
                loc = item["use"]
                if loc in ref["list"]["dn"]:
                    tmp_dn["surge"].append(
                        (
                            1,
                            loc,
                            ren.URI + ref["dn"]["surge-" + loc],
                            item["node"],
                        )
                    )
                    tmp_dn["clash"].append(
                        (
                            1,
                            loc,
                            ren.URI + ref["dn"]["clash-" + loc],
                            item["node"],
                        )
                    )
                if loc in ref["list"]["ip"]:
                    tmp_ip["surge"].append(
                        (
                            1,
                            loc,
                            ren.URI + ref["ip"]["surge-" + loc],
                            item["node"],
                        )
                    )
                    tmp_ip["clash"].append(
                        (
                            1,
                            loc,
                            ren.URI + ref["ip"]["clash-" + loc],
                            item["node"],
                        )
                    )

            elif item["type"] == "link":
                tmp_dn["surge"].append((2, item["id"], item["link"], item["node"]))
                tmp_dn["clash"].append((2, item["id"], item["link"], item["node"]))

        res = {"dn": tmp_dn, "ip": tmp_ip, "main": tmp_main}
        self.res["filter"] = res

    def __load_proxy(self) -> None:
        tmp_proxy = {"local": [], "link": []}
        for item in self.res["proxy"]:
            item = item.split(" ")
            if "l" in item[0]:
                tmp_proxy["link"].append(item[1])
        self.res["proxy"] = tmp_proxy
