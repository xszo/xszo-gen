from ..lib import var
from . import ren

# Var
__src = {}


# Init
def init():
    ren.PATH_OUT_SURGE.mkdir(parents=True, exist_ok=True)
    ren.PATH_OUT_CLASH.mkdir(parents=True, exist_ok=True)


def __ref(als: dict) -> None:
    ref = {
        # avaliability
        "list": {
            "dn": set(als["domain"]),
            "ip": set(als["ip"]),
        },
        # data
        "dn": {},
        "ip": {},
        "misc": {},
    }
    # domain list uri
    for k in ref["list"]["dn"]:
        ref["dn"]["surge-" + k] = "surge/filter-dn+" + k + ".txt"
        ref["dn"]["clash-" + k] = "clash/filter-dn+" + k + ".txt"
    # ip list uri
    for k in ref["list"]["ip"]:
        ref["ip"]["surge-" + k] = "surge/filter-ip+" + k + ".txt"
        ref["ip"]["clash-" + k] = "surge/filter-ip+" + k + ".txt"
    # pass via file
    var.let("filter-ref", ref)


def __dn() -> None:
    for key, val in __src["domain"].items():
        # dump clash
        with open(
            ren.PATH_OUT_CLASH / ("filter-dn+" + key + ".txt"),
            "tw",
            encoding="utf-8",
        ) as file:
            file.writelines(["+" + x + "\n" if x[0] == "." else x + "\n" for x in val])
        # dump surge
        raw = []
        for item in val:
            if item[0] == ".":
                raw.append("DOMAIN-SUFFIX," + item[1:] + "\n")
            elif "*" in item or "?" in item:
                raw.append("DOMAIN-WILDCARD," + item + "\n")
            else:
                raw.append("DOMAIN," + item + "\n")
        with open(
            ren.PATH_OUT_SURGE / ("filter-dn+" + key + ".txt"),
            "tw",
            encoding="utf-8",
        ) as file:
            file.writelines(raw)
    # return avaliable lists
    return __src["domain"].keys()


def __ip() -> None:
    # convert input format
    raw = {}
    for key in ["ip4", "ip6", "ipasn", "ipgeo"]:
        for k, v in __src[key].items():
            if not k in raw:
                raw[k] = {}
            raw[k][key] = v
    for key, val in raw.items():
        # format data
        line = []
        if "ip4" in val:
            line.extend(["IP-CIDR," + x for x in val["ip4"]])
        if "ip6" in val:
            line.extend(["IP-CIDR6," + x for x in val["ip6"]])
        if "ipasn" in val:
            line.extend(["IP-ASN," + x for x in val["ipasn"]])
        if "ipgeo" in val:
            line.extend(["GEOIP," + x for x in val["ipgeo"]])
        # write output
        with open(
            ren.PATH_OUT_SURGE / ("filter-ip+" + key + ".txt"),
            "tw",
            encoding="utf-8",
        ) as file:
            file.writelines([x + "\n" for x in line])
    # return avaliable lists
    return raw.keys()


def dump(lsrc: dict) -> None:
    global __src
    __src = lsrc
    __ref({"domain": tuple(__dn()), "ip": tuple(__ip())})
