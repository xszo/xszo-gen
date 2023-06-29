import os
import requests
import yaml


# utils
def Merge(dc1, dc2):
    """merge dict right into left"""
    for key in dc2:
        if key in dc1 and isinstance(dc1[key], dict) and isinstance(dc2[key], dict):
            Merge(dc1[key], dc2[key])
        else:
            dc1[key] = dc2[key]


# load data
with open("src/net/main.yml", "tr", encoding="utf-8") as file:
    Data = yaml.safe_load(file)
with open("var/net/main.yml", "tr", encoding="utf-8") as file:
    Merge(Data, yaml.safe_load(file))

# variables
Gen = {}


# modules
def LoadFile(File):
    """load content from file"""
    Res = {}
    if "gen" in File:
        global Gen
        Gen = File["gen"]
    if "meta" in File:
        Res["meta"] = File["meta"]
    if "node" in File:
        Res["node"] = LoadNode(File["node"])
    if "filter" in File:
        Res["filter"] = LoadFilter(File["filter"])
    return Res


def LoadNode(ListNode):
    """load node section in file"""
    Res = []
    for item in ListNode:
        # load list
        if isinstance(item["list"], list):
            lols = []
            for line in item["list"]:
                # insert variable
                if line[0] == "=":
                    lols.extend(Gen["var"][line[1:]])
                else:
                    lols.append(line)
            item["list"] = lols
        else:
            item["regex"] = item["list"]
            del item["list"]
        Res.append(item)
    return Res


def LoadFilter(ListFilter):
    """load filter section in file"""
    Res = {"domain": [], "ipcidr": [], "ipgeo": [], "port": []}
    tmpDomain = [[], [], [], [], [], [], [], []]
    tmpIpcidr = [[], []]
    tmpPre = {}
    for item in ListFilter:
        # type gen
        if item["type"] == "gen":
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
                for line in raw["ipcidr"]:
                    if line[0] == "[":
                        tmpIpcidr[1].append((2, line[1:-1], item["dest"]))
                    else:
                        tmpIpcidr[0].append((1, line, item["dest"]))
            if "port" in raw:
                for line in raw["port"]:
                    Res["port"].append((1, str(line), item["dest"]))
        # type pre
        elif item["type"] == "pre":
            for mod in Gen["tar"]:
                if not mod in tmpPre:
                    tmpPre[mod] = []
                tmpPre[mod].append((1, item["name"][mod], item["dest"]))
        # type other
        elif item["type"] == "ipgeo":
            Res["ipgeo"].append((1, item["name"].upper(), item["dest"]))
        elif item["type"] == "main":
            Res["main"] = item["dest"]
    # merge in order
    for item in reversed(tmpDomain):
        Res["domain"] += item
    for item in tmpIpcidr:
        Res["ipcidr"] += item
    if len(tmpPre) > 0:
        Res["pre"] = tmpPre
    return Res


def CallScript(File):
    """call script to output"""
    File["id"] = Gen["id"]
    for item in Gen["tar"]:
        for unit in Data["script"][item]:
            unit = unit.split(" ")
            # create dir
            outPath = "out/net/" + os.path.dirname(unit[1])
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            # call script
            if "a" in unit[0]:
                outPath = os.path.join(outPath, Gen["id"] + os.path.basename(unit[1]))
                out = open(outPath, "tw", encoding="utf-8")
                with open("src/net/" + unit[1] + ".py", "tr", encoding="utf-8") as file:
                    exec(file.read(), {"out": out, "src": File})
                out.close()
                continue
            # fetch remote
            if "r" in unit[0]:
                outPath = os.path.join(outPath, os.path.basename(unit[1]))
                with open(outPath, "tw", encoding="utf-8") as file:
                    file.write(requests.get(unit[2], timeout=1000).text)
                continue
            # copy file
            outPath = os.path.join(outPath, os.path.basename(unit[1]))
            os.system("cp -f src/net/" + unit[1] + " " + outPath)


# load base
with open("var/main.yml", "tr", encoding="utf-8") as file:
    raw = yaml.safe_load(file)
Base = {"meta": {"path": raw["uri"] + "net/", "int": raw["int"], "ico": raw["ico"]}}
with open("var/net/" + Data["base"], "tr", encoding="utf-8") as file:
    Merge(Base, LoadFile(yaml.safe_load(file)))
# load file
for item in Data["list"]:
    File = Base.copy()
    with open("var/net/" + item, "tr", encoding="utf-8") as file:
        Merge(File, LoadFile(yaml.safe_load(file)))
    # call output
    CallScript(File)
