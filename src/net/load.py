from copy import deepcopy

import yaml

from ..lib import var
from . import ren

# Var
res = {}
__src = {}
__var = {"var": {}}
with open(ren.PATH_VAR_REX, "tr", encoding="utf-8") as file:
    __var["rex"] = yaml.safe_load(file)


# load base profile
def base(araw: dict) -> None:
    global __src
    __src = araw
    __src["ref"] = {}
    # load common
    __src["misc"].update(
        {
            "interval": ren.INT,
            "icon": ren.ICO,
        }
    )
    # load sections
    if "id" in __src:
        __src["ref"]["id"] = __src.pop("id")
    if "var" in __src:
        __var["var"].update(__src.pop("var"))


# load data from file
def load(araw: dict) -> None:
    global res
    # load sections
    if "tar" in araw:
        res = deepcopy(__src)
        res["ref"]["tar"] = araw.pop("tar")
    else:
        res = {}
        return

    if "id" in araw:
        res["ref"]["id"] = araw["id"]
    if "var" in araw:
        __var["var"].update(araw["var"])
    if "misc" in araw:
        res["misc"].update(araw["misc"])
    if "route" in araw:
        res["route"] = __insert(res["route"], araw["route"])
    if "node" in araw:
        res["node"] = __insert(res["node"], araw["node"])
    __var["var"]["node"] = [x["name"] for x in res["node"]]
    # load modules
    __load_route()
    __load_node()
    __load_filter()
    __load_proxy()
    return res


# t insert ls2 into ls1 with template
def __insert(ls1: list, ls2: list) -> list:
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
def __load_route() -> None:
    tmp_node = [[], [], [], []]
    tmp_filter = []
    for item in res["route"]:
        sortn = 0
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
                if "sort" in item["icon"]:
                    sortn = item["icon"]["sort"]
            while sortn > len(tmp_node):
                tmp_node.extend([[], [], [], []])
            tmp_node[sortn].append(lo_node)
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
    tmp_nodels = []
    for item in tmp_node:
        tmp_nodels.extend(item)
    tmp_nodels.extend(res["node"])
    res["node"] = tmp_nodels
    res["filter"] = tmp_filter
    del res["route"]


# ins inline var, format list val
def __load_node() -> None:
    for item in res["node"]:
        if isinstance(item["list"], list):
            # plain list
            tmp = []
            for sth in item["list"]:
                # replace variable
                if sth[0] == "=":
                    tmp.extend(__var["var"][sth[1:]])
                else:
                    tmp.append(sth)
            item["list"] = tmp
        else:
            # regex match
            if item["list"][0] == "=":
                item["regx"] = __var["rex"][item.pop("list")[1:]]
            else:
                item["regx"] = item.pop("list")


# get filter content from file and optimize
def __load_filter() -> None:
    ref = var.get("filter-ref")
    tmp_dn = {"surge": [], "clash": []}
    tmp_ip = {"surge": [], "clash": []}

    for item in res["filter"]:
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

    res["filter"] = {"dn": tmp_dn, "ip": tmp_ip, "main": tmp_main}


def __load_proxy() -> None:
    tmp_proxy = {"local": [], "link": []}
    for item in res["proxy"]:
        item = item.split(" ")
        if "l" in item[0]:
            tmp_proxy["link"].append(item[1])
    res["proxy"] = tmp_proxy
