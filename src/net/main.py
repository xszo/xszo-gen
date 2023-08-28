import os
import requests
import yaml
from copy import deepcopy


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
with open("src/net/main.yml", "tr", encoding="utf-8") as file:
    Data = yaml.safe_load(file)
with open("var/net/main.yml", "tr", encoding="utf-8") as file:
    Base = yaml.safe_load(file)
Data["list"] = Base.pop("list")
with open("var/main.yml", "tr", encoding="utf-8") as file:
    raw = yaml.safe_load(file)
    Data["path"] = raw["uri"] + "net/"
    Merge(
        Base,
        {
            "meta": {
                "path": Data["path"],
                "interval": raw["int"],
                "icon": raw["ico"],
            }
        },
    )

# shared variables
Gen = {}


# modules
def RunFile(Base, Ovrd):
    """load data from file and call output"""
    Res = {}
    # store options in var Gen
    global Gen
    Gen = deepcopy(Base["gen"])
    if "gen" in Ovrd:
        Merge(Gen, Ovrd["gen"])
    # normalize id
    if "id" in Gen:
        Gen["id"] += "-"
    else:
        Gen["id"] = ""
    # load sections
    if "meta" in Ovrd:
        Res["meta"] = Merge(deepcopy(Base["meta"]), Ovrd["meta"])
    else:
        Res["meta"] = deepcopy(Base["meta"])
    if "node" in Ovrd:
        Res["node"] = LoadNode(Insert(deepcopy(Base["node"]), Ovrd["node"]))
    else:
        Res["node"] = LoadNode(deepcopy(Base["node"]))
    if "filter" in Ovrd:
        Res["filter"] = LoadFilter(Insert(Base["filter"], Ovrd["filter"]))
    else:
        Res["filter"] = LoadFilter(Base["filter"])
    # call script to output
    CallScript(Res)
    return Res


def LoadNode(ListNode):
    """ins inline var, format list val"""
    # get data
    with open("var/pattern.yml", "tr", encoding="utf-8") as file:
        Pat = yaml.safe_load(file)["region"]
    for item in ListNode:
        # load list val
        if isinstance(item["list"], list):
            # plain list
            tmp = []
            for line in item["list"]:
                # replace variable
                if line[0] == "=":
                    tmp.extend(Gen["var"][line[1:]])
                else:
                    tmp.append(line)
            item["list"] = tmp
        else:
            # regex match
            if item["list"][0] == "=":
                item["regx"] = Pat[item["list"][1:]]
            else:
                item["regx"] = item["list"]
            del item["list"]
    return ListNode


def LoadFilter(ListFilter):
    """get filter content from file and optimize"""
    Res = {"domain": [], "ipcidr": [], "ipgeo": [], "port": []}
    tmpDomain = [[], [], [], [], [], [], [], []]
    tmpIpcidr = [[], []]
    tmpPre = {}
    for item in ListFilter:
        # type gen
        if item["type"] == "gen":
            # read filter file
            with open(
                "var/net/filter/" + item["name"] + ".yml", "tr", encoding="utf-8"
            ) as file:
                raw = yaml.safe_load(file)
            if "domain" in raw:
                # divide domain by level
                for line in raw["domain"]:
                    if line[0] == "-":
                        tmpDomain[line.count(".")].append((2, line[1:], item["dest"]))
                    else:
                        tmpDomain[line.count(".")].append((1, line, item["dest"]))
            if "ipcidr" in raw:
                # sepatate 4 and 6
                for line in raw["ipcidr"]:
                    if line[0] == "[":
                        tmpIpcidr[1].append((2, line[1:-1], item["dest"]))
                    else:
                        tmpIpcidr[0].append((1, line, item["dest"]))
            if "port" in raw:
                for line in raw["port"]:
                    # convert to (type, match, dest)
                    Res["port"].append((1, str(line), item["dest"]))
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
                            item["dest"],
                            item["name"],
                        )
                    )
                else:
                    tmpPre[unit].append(
                        (1, item["link"][unit], item["dest"], item["name"])
                    )
        # type other
        elif item["type"] == "ipgeo":
            Res["ipgeo"].append((1, item["name"].upper(), item["dest"]))
        elif item["type"] == "main":
            Res["main"] = item["dest"]
    # merge domain in order
    for item in reversed(tmpDomain):
        Res["domain"] += item
    # copy into Res
    for item in tmpIpcidr:
        Res["ipcidr"] += item
    if len(tmpPre) > 0:
        Res["pre"] = tmpPre
    return Res


# pre callscript
for item in Data["script"]:
    tmp = []
    for unit in Data["script"][item]:
        unit = unit.split(" ")
        tmp.append(tuple(unit))
        outPath = "out/net/" + os.path.dirname(unit[1])
        if not os.path.exists(outPath):
            os.makedirs(outPath)
    Data["script"][item] = tmp


def CallScript(Info):
    """call script to generate output from object"""
    Info["id"] = Gen["id"]
    # loop targets
    for item in Gen["tar"]:
        for unit in Data["script"][item]:
            outPath = "out/net/" + unit[1]
            # see flag
            if "g" in unit[0]:
                # call script
                outPath = os.path.join(
                    os.path.dirname(outPath), Gen["id"] + os.path.basename(outPath)
                )
                out = open(outPath, "tw", encoding="utf-8")
                with open("src/net/" + unit[1] + ".py", "tr", encoding="utf-8") as file:
                    exec(file.read(), {"out": out, "src": Info})
                out.close()
                continue
            if "r" in unit[0]:
                # fetch remote
                with open(outPath, "tw", encoding="utf-8") as file:
                    file.write(requests.get(unit[2], timeout=1000).text)
                continue
            # copy file
            os.system("cp -f src/net/" + unit[1] + " " + outPath)


# run scripts
RunFile(Base, {})
for item in Data["list"]:
    with open("var/net/" + item, "tr", encoding="utf-8") as file:
        RunFile(Base, yaml.safe_load(file))
