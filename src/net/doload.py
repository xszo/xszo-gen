from copy import deepcopy

import yaml
from ren import Var

with open(Var.PATH["var.pattern"], "tr", encoding="utf-8") as file:
    REX = yaml.safe_load(file)["region"]


class do:
    res = {}

    __base = {}
    __var = {"var": {}}

    # d merge dc2 into dc1
    def __merge(self, dc1: dict, dc2: dict):
        for key in dc2:
            if key in dc1 and isinstance(dc1[key], dict) and isinstance(dc2[key], dict):
                self.__merge(dc1[key], dc2[key])
            else:
                dc1[key] = dc2[key]
        return dc1

    # t insert ls2 into ls1 with template
    def __insert(self, ls1: list, ls2: list):
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

    def __init__(self):
        # load base profile
        with open(Var.PATH["var.base"], "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        self.__base = {
            "dump": {
                "uri": raw["uri"],
            },
            "misc": {
                "interval": raw["int"],
                "icon": raw["ico"],
            },
        }
        self.__var["uri"] = raw["uri"]
        with open(Var.PATH["var.list"], "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        self.__base["proxy"] = raw["proxy"]
        with open(Var.PATH["var"] + raw["base"], "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        self.__merge(self.__base, raw)
        if "var" in self.__base:
            self.__var["var"].update(self.__base.pop("var"))
        if "id" in self.__base:
            self.__base["dump"]["id"] = self.__base.pop("id")
        if "tar" in self.__base:
            self.__base["dump"]["tar"] = self.__base.pop("tar")

    # load data from file
    def load(self, i_src: dict):
        # load sections
        if "tar" in i_src:
            self.res = deepcopy(self.__base)
            self.res["dump"]["tar"] = i_src["tar"]
        else:
            self.res = {}
            return
        if "id" in i_src:
            self.res["dump"]["id"] = i_src["id"]
        if "var" in i_src:
            self.__var["var"].update(i_src["var"])
        if "misc" in i_src:
            self.res["misc"].update(i_src["misc"])
        if "route" in i_src:
            self.res["route"] = self.__insert(self.res["route"], i_src["route"])
        if "node" in i_src:
            self.res["node"] = self.__insert(self.res["node"], i_src["node"])
        # load modules
        self.__load_route()
        self.__load_node()
        self.__load_filter()
        self.__load_proxy()
        return self.res

    # convert route list to node and filter
    def __load_route(self):
        tmp_node = []
        tmp_filter = []
        for item in self.res["route"]:
            # node
            if "id" in item["node"]:
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
                    "type": line["type"],
                    "node": lo_id,
                }
                # filter link or gen filter
                if line["type"] == "pre":
                    lo_filter["link"] = line["list"]
                elif "list" in line:
                    lo_filter["list"] = line["list"]
                tmp_filter.append(lo_filter)
        # append
        self.res["node"] = tmp_node + self.res["node"]
        self.res["filter"] = tmp_filter
        del self.res["route"]

    # ins inline var, format list val
    def __load_node(self):
        for item in self.res["node"]:
            if isinstance(item["list"], list):
                # plain list
                tmp = []
                for sth in item["list"]:
                    # replace variable
                    if sth[0] == "=":
                        tmp.extend(self.__var["var"][sth[1:]])
                    else:
                        tmp.append(sth)
                item["list"] = tmp
            else:
                # regex match
                if item["list"][0] == "=":
                    item["regx"] = REX[item.pop("list")[1:]]
                else:
                    item["regx"] = item.pop("list")

    # get filter content from file and optimize
    def __load_filter(self):
        tmp_domain = [[], [], [], [], [], [], [], []]
        tmp_ipcidr = [[], []]
        tmp_ipgeo = []
        tmp_port = []
        tmp_pre = {}
        for item in self.res["filter"]:
            # type gen
            if item["type"] == "gen":
                # read filter file
                with open(
                    Var.PATH["var.filter"] + item["list"] + ".yml",
                    "tr",
                    encoding="utf-8",
                ) as file:
                    raw = yaml.safe_load(file)
                if "domain" in raw:
                    # divide domain by level
                    for line in raw["domain"]:
                        if line[0] == "-":
                            tmp_domain[line.count(".")].append(
                                (2, line[1:], item["node"])
                            )
                        else:
                            tmp_domain[line.count(".")].append((1, line, item["node"]))
                if "ipcidr" in raw:
                    # sepatate 4 and 6
                    for line in raw["ipcidr"]:
                        if line[0] == "[":
                            tmp_ipcidr[1].append((2, line[1:-1], item["node"]))
                        else:
                            tmp_ipcidr[0].append((1, line, item["node"]))
                if "port" in raw:
                    for line in raw["port"]:
                        # convert to (type, match, dest)
                        tmp_port.append((1, line, item["node"]))
            # type pre
            elif item["type"] == "pre":
                for unit in self.res["dump"]["tar"]:
                    if not unit in tmp_pre:
                        tmp_pre[unit] = []
                    # from name.tar to tar.[name]
                    if item["link"][unit][0] == "-":
                        tmp_pre[unit].append(
                            (
                                1,
                                self.__var["uri"] + item["link"][unit][1:],
                                item["node"],
                                item["id"],
                            )
                        )
                    else:
                        tmp_pre[unit].append(
                            (1, item["link"][unit], item["node"], item["id"])
                        )
            # type other
            elif item["type"] == "ipgeo":
                tmp_ipgeo.append((1, item["list"].upper(), item["node"]))
            elif item["type"] == "main":
                tmp_main = item["node"]
        # merge domain in order
        res = {"domain": [], "ipcidr": [], "main": tmp_main}
        for item in reversed(tmp_domain):
            res["domain"] += sorted(
                item, key=lambda v: ".".join(reversed(v[1].split(".")))
            )
        # copy into res
        for item in tmp_ipcidr:
            res["ipcidr"] += sorted(
                item, reverse=True, key=lambda v: int((v[1].split("/"))[1])
            )
        res["ipgeo"] = sorted(tmp_ipgeo, key=lambda v: v[1])
        res["port"] = sorted(tmp_port, key=lambda v: v[1])
        if len(tmp_pre) > 0:
            res["pre"] = tmp_pre
        self.res["filter"] = res

    def __load_proxy(self):
        tmp_proxy = {"local": [], "link": []}
        for item in self.res["proxy"]:
            item = item.split(" ")
            if "l" in item[0]:
                tmp_proxy["link"].append(item[1])
        self.res["proxy"] = tmp_proxy
