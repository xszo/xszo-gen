from copy import deepcopy

import yaml

from var import VAR

with open(VAR["path"]["var.pattern"], "tr", encoding="utf-8") as file:
    Pat = yaml.safe_load(file)["region"]


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
        Res = []
        for item in ls2:
            if isinstance(item, str):
                if item == "=":
                    Res.extend(ls1)
                if item[0] == "-":
                    Res.append(ls1[int(item[1:])])
            else:
                Res.append(item)
        return Res

    def __init__(self):
        # load base profile
        with open(VAR["path"]["var.base"], "tr", encoding="utf-8") as file:
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
        with open(VAR["path"]["var.list"], "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        self.__base["proxy"] = raw["proxy"]
        with open(VAR["path"]["var"] + raw["base"], "tr", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        self.__merge(self.__base, raw)
        if "var" in self.__base:
            self.__var["var"].update(self.__base.pop("var"))
        if "id" in self.__base:
            self.__base["dump"]["id"] = self.__base.pop("id")
        if "tar" in self.__base:
            self.__base["dump"]["tar"] = self.__base.pop("tar")

    # load data from file
    def load(self, ipro: dict):
        # load sections
        if "tar" in ipro:
            self.res = deepcopy(self.__base)
            self.res["dump"]["tar"] = ipro["tar"]
        else:
            self.res = {}
            return
        if "id" in ipro:
            self.res["dump"]["id"] = ipro["id"]
        if "var" in ipro:
            self.__var["var"].update(ipro["var"])
        if "misc" in ipro:
            self.res["misc"].update(ipro["misc"])
        if "route" in ipro:
            self.res["route"] = self.__insert(self.res["route"], ipro["route"])
        if "node" in ipro:
            self.res["node"] = self.__insert(self.res["node"], ipro["node"])
        # load modules
        self.__loadRoute()
        self.__loadNode()
        self.__loadFilter()
        self.__loadProxy()
        return self.res

    # convert route list to node and filter
    def __loadRoute(self):
        tmpNode = []
        tmpFilter = []
        for item in self.res["route"]:
            # node
            if "id" in item["node"]:
                loId = item["node"]["id"]
            else:
                loId = item["id"]
                # format node
                loNode = {
                    "id": loId,
                    "type": item["node"]["type"],
                    "name": item["node"]["name"],
                    "list": item["node"]["list"],
                }
                if "icon" in item:
                    loNode["icon"] = item["icon"]
                tmpNode.append(loNode)
            # filter
            for idx, line in enumerate(item["filter"]):
                loFilter = {
                    "id": item["id"] + str(idx),
                    "type": line["type"],
                    "node": loId,
                }
                # filter link or gen filter
                if line["type"] == "pre":
                    loFilter["link"] = line["list"]
                elif "list" in line:
                    loFilter["list"] = line["list"]
                tmpFilter.append(loFilter)
        # append
        self.res["node"] = tmpNode + self.res["node"]
        self.res["filter"] = tmpFilter
        del self.res["route"]

    # ins inline var, format list val
    def __loadNode(self):
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
                    item["regx"] = Pat[item.pop("list")[1:]]
                else:
                    item["regx"] = item.pop("list")

    # get filter content from file and optimize
    def __loadFilter(self):
        tmpDomain = [[], [], [], [], [], [], [], []]
        tmpIpcidr = [[], []]
        tmpIpgeo = []
        tmpPort = []
        tmpPre = {}
        for item in self.res["filter"]:
            # type gen
            if item["type"] == "gen":
                # read filter file
                with open(
                    VAR["path"]["var.filter"] + item["list"] + ".yml",
                    "tr",
                    encoding="utf-8",
                ) as file:
                    raw = yaml.safe_load(file)
                if "domain" in raw:
                    # divide domain by level
                    for line in raw["domain"]:
                        if line[0] == "-":
                            tmpDomain[line.count(".")].append(
                                (2, line[1:], item["node"])
                            )
                        else:
                            tmpDomain[line.count(".")].append((1, line, item["node"]))
                if "ipcidr" in raw:
                    # sepatate 4 and 6
                    for line in raw["ipcidr"]:
                        if line[0] == "[":
                            tmpIpcidr[1].append((2, line[1:-1], item["node"]))
                        else:
                            tmpIpcidr[0].append((1, line, item["node"]))
                if "port" in raw:
                    for line in raw["port"]:
                        # convert to (type, match, dest)
                        tmpPort.append((1, line, item["node"]))
            # type pre
            elif item["type"] == "pre":
                for unit in self.res["dump"]["tar"]:
                    if not unit in tmpPre:
                        tmpPre[unit] = []
                    # from name.tar to tar.[name]
                    if item["link"][unit][0] == "-":
                        tmpPre[unit].append(
                            (
                                1,
                                self.__var["uri"] + item["link"][unit][1:],
                                item["node"],
                                item["id"],
                            )
                        )
                    else:
                        tmpPre[unit].append(
                            (1, item["link"][unit], item["node"], item["id"])
                        )
            # type other
            elif item["type"] == "ipgeo":
                tmpIpgeo.append((1, item["list"].upper(), item["node"]))
            elif item["type"] == "main":
                tmpMain = item["node"]
        # merge domain in order
        Res = {"domain": [], "ipcidr": [], "main": tmpMain}
        for item in reversed(tmpDomain):
            Res["domain"] += sorted(
                item, key=lambda v: ".".join(reversed(v[1].split(".")))
            )
        # copy into Res
        for item in tmpIpcidr:
            Res["ipcidr"] += sorted(
                item, reverse=True, key=lambda v: int((v[1].split("/"))[1])
            )
        Res["ipgeo"] = sorted(tmpIpgeo, key=lambda v: v[1])
        Res["port"] = sorted(tmpPort, key=lambda v: v[1])
        if len(tmpPre) > 0:
            Res["pre"] = tmpPre
        self.res["filter"] = Res

    def __loadProxy(self):
        tmpProxy = {"local": [], "link": []}
        for item in self.res["proxy"]:
            item = item.split(" ")
            if "l" in item[0]:
                tmpProxy["link"].append(item[1])
        self.res["proxy"] = tmpProxy
