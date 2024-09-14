from copy import deepcopy

import yaml

from . import ren

res = {}

__var = {}
__base = {}
__tmp_var = {}

# load var
with open(ren.PATH_VAR_REX, "tr", encoding="utf-8") as file:
    __var["rex"] = yaml.safe_load(file)


# load base profile
def base(araw: dict) -> None:
    global __base, __tmp_var
    __base = araw
    __base["ref"] = {}
    # load common
    with open(ren.PATH_VAR_BASE, "tr", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
    __base["misc"].update(
        {
            "interval": raw["int"],
            "icon": raw["ico"],
        }
    )
    # load sections
    if "id" in __base:
        __base["ref"]["id"] = __base.pop("id")
    if "var" in __base:
        __tmp_var.update(__base.pop("var"))


# load data from file
def load(araw: dict) -> None:
    global res, __tmp_var
    # load sections
    if "tar" in araw:
        res = deepcopy(__base)
        res["ref"]["tar"] = araw.pop("tar")
    else:
        res = {}
        return

    if "id" in araw:
        res["ref"]["id"] = araw["id"]
    if "var" in araw:
        __tmp_var.update(araw["var"])
    if "misc" in araw:
        res["misc"].update(araw["misc"])
    if "route" in araw:
        res["route"] = __insert(res["route"], araw["route"])
    if "node" in araw:
        res["node"] = __insert(res["node"], araw["node"])
    __tmp_var["node"] = [x["name"] for x in res["node"]]
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
    global res
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
    global res
    for item in res["node"]:
        if isinstance(item["list"], list):
            # plain list
            tmp = []
            for sth in item["list"]:
                # replace variable
                if sth[0] == "=":
                    tmp.extend(__tmp_var[sth[1:]])
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
    global res
    with open(ren.PATH_TMP_FILTER_LIST, "tr", encoding="utf-8") as file:
        ref = yaml.safe_load(file)

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
    global res
    tmp_proxy = {"local": [], "link": []}
    for item in res["proxy"]:
        item = item.split(" ")
        if "l" in item[0]:
            tmp_proxy["link"].append(item[1])
    res["proxy"] = tmp_proxy
