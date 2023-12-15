import os
from copy import deepcopy

import requests
import yaml

from var import VAR


# utils
def Merge(dc1, dc2):
    """lo dy, merge dict right into left"""
    for key in dc2:
        if key in dc1 and isinstance(dc1[key], dict) and isinstance(dc2[key], dict):
            Merge(dc1[key], dc2[key])
        else:
            dc1[key] = dc2[key]
    return dc1


def Insert(ls1, ls2):
    """lo st, insert list right into left"""
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


# load data
with open(VAR["path"]["var.list"], "tr", encoding="utf-8") as file:
    Data = yaml.safe_load(file)
with open(VAR["path"]["var.base"], "tr", encoding="utf-8") as file:
    raw = yaml.safe_load(file)
    Data["path"] = raw["uri"] + "net/"
    Base = {
        "proxy": Data.pop("proxy"),
        "misc": {
            "path": Data["path"],
            "interval": raw["int"],
            "icon": raw["ico"],
        },
    }

# shared variables
Gen = {}


# modules
def RunFile(Base, Ovrd):
    """load data from file and call output"""
    global Gen
    Gen = deepcopy(Base)
    # load sections
    if not "tar" in Ovrd:
        return
    Gen["tar"] = Ovrd["tar"]
    if "id" in Ovrd:
        Gen["id"] = Ovrd["id"]
        if not Gen["id"] == "":
            Gen["id"] += "-"
    if "var" in Ovrd:
        Gen["var"].update(Ovrd["var"])
    if "misc" in Ovrd:
        Merge(Gen["misc"], Ovrd["misc"])
    if "route" in Ovrd:
        Gen["route"] = Insert(Gen["route"], Ovrd["route"])
    if "node" in Ovrd:
        Gen["node"] = Insert(Gen["node"], Ovrd["node"])
    # load
    LoadRoute()
    LoadNode()
    LoadFilter()
    LoadProxy()
    # call script to output
    CallScript()


def LoadRoute():
    """convert route list to node and filter"""
    global Gen
    tmpNode = []
    tmpFilter = []
    for item in Gen["route"]:
        # node
        if "id" in item["node"]:
            loId = item["node"]["id"]
        else:
            loId = item["id"]
            if item["node"]["type"] != "pre":
                loNode = {
                    "id": item["id"],
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
            if line["type"] == "pre":
                loFilter["link"] = line["list"]
            elif "list" in line:
                loFilter["list"] = line["list"]
            tmpFilter.append(loFilter)
    Gen["node"] = tmpNode + Gen["node"]
    Gen["filter"] = tmpFilter
    del Gen["route"]


# pre LoadNode
with open(VAR["path"]["var.pattern"], "tr", encoding="utf-8") as file:
    Pat = yaml.safe_load(file)["region"]


def LoadNode():
    """ins inline var, format list val"""
    global Gen
    for item in Gen["node"]:
        if isinstance(item["list"], list):
            # plain list
            tmp = []
            for sth in item["list"]:
                # replace variable
                if sth[0] == "=":
                    tmp.extend(Gen["var"][sth[1:]])
                else:
                    tmp.append(sth)
            item["list"] = tmp
        else:
            # regex match
            if item["list"][0] == "=":
                item["regx"] = Pat[item.pop("list")[1:]]
            else:
                item["regx"] = item.pop("list")


def LoadFilter():
    """get filter content from file and optimize"""
    global Gen
    tmpDomain = [[], [], [], [], [], [], [], []]
    tmpIpcidr = [[], []]
    tmpIpgeo = []
    tmpPort = []
    tmpPre = {}
    for item in Gen["filter"]:
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
                        tmpDomain[line.count(".")].append((2, line[1:], item["node"]))
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
            for unit in Gen["tar"]:
                if not unit in tmpPre:
                    tmpPre[unit] = []
                # from name.tar to tar.[name]
                if item["link"][unit][0] == "-":
                    tmpPre[unit].append(
                        (
                            1,
                            Data["path"] + item["link"][unit][1:],
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
        Res["domain"] += sorted(item, key=lambda v: ".".join(reversed(v[1].split("."))))
    # copy into Res
    for item in tmpIpcidr:
        Res["ipcidr"] += sorted(
            item, reverse=True, key=lambda v: int((v[1].split("/"))[1])
        )
    Res["ipgeo"] = sorted(tmpIpgeo, key=lambda v: v[1])
    Res["port"] = sorted(tmpPort, key=lambda v: v[1])
    if len(tmpPre) > 0:
        Res["pre"] = tmpPre
    Gen["filter"] = Res


def LoadProxy():
    global Gen
    tmpProxy = {"local": [], "link": []}
    for item in Gen["proxy"]:
        item = item.split(" ")
        if "l" in item[0]:
            tmpProxy["link"].append(item[1])
    Gen["proxy"] = tmpProxy


# pre CallScript
for item in VAR["script"]:
    tmp = []
    for unit in VAR["script"][item]:
        unit = unit.split(" ")
        tmp.append(tuple(unit))
        outPath = VAR["path"]["out"] + os.path.dirname(unit[1])
        if not os.path.exists(outPath):
            os.makedirs(outPath)
    VAR["script"][item] = tmp


def CallScript():
    """call script to generate output from object"""
    # loop targets
    for item in Gen["tar"]:
        for unit in VAR["script"][item]:
            outPath = VAR["path"]["out"] + unit[1]
            # see flag
            if "g" in unit[0]:
                # call script
                outPath = os.path.join(
                    os.path.dirname(outPath), Gen["id"] + os.path.basename(outPath)
                )
                out = open(outPath, "tw", encoding="utf-8")
                with open(
                    VAR["path"]["src"] + unit[1] + ".py", "tr", encoding="utf-8"
                ) as file:
                    exec(
                        file.read(),
                        {
                            "out": out,
                            "src": {
                                "id": Gen["id"],
                                "meta": Gen["misc"],
                                "node": deepcopy(Gen["node"]),
                                "filter": Gen["filter"],
                                "proxy": Gen["proxy"],
                            },
                        },
                    )
                out.close()
                continue
            if "r" in unit[0]:
                # fetch remote
                with open(outPath, "tw", encoding="utf-8") as file:
                    file.write(requests.get(unit[2], timeout=1000).text)
                continue
            # copy file
            os.system(
                "cp -f "
                + VAR["path"]["src"]
                + unit[1]
                + " "
                + VAR["path"]["out"]
                + unit[1]
            )


# run scripts
with open(VAR["path"]["var"] + Data["base"], "tr", encoding="utf-8") as file:
    Merge(Base, yaml.safe_load(file))
for item in Data["list"]:
    with open(VAR["path"]["var"] + item, "tr", encoding="utf-8") as file:
        RunFile(Base, yaml.safe_load(file))
