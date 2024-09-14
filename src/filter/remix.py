# Var
res = {}
__raw = {}
__dn_lv = range(1, 5)


def load(araw: dict) -> None:
    global __raw
    for k1, v1 in araw.items():
        __raw[k1] = {}
        for k2, v2 in v1.items():
            __raw[k1][k2] = set(v2)


def __dn_mini(raw: set | list) -> set:
    dat = set()
    for i in __dn_lv:
        suffix = set(x for x in raw if x[0] == "." and x.count(".") == i)
        dat.update(suffix)
        raw = set(x for x in raw if not ("." + ".".join(x.split(".")[-i:])) in suffix)
    dat.update(raw)
    return dat


def __dn_rm(raw: set, rm: set):
    for i in __dn_lv:
        # remove parent
        raw.difference_update(
            set("." + ".".join(x.split(".")[-i:]) for x in rm if x.count(".") >= i)
        )
        # remove children
        suffix = set(x for x in rm if x[0] == "." and x.count(".") == i)
        raw = set(x for x in raw if not ("." + ".".join(x.split(".")[-i:])) in suffix)
    return raw


def mix(dat: list) -> None:
    global res
    keys = __raw.keys()
    for k in keys:
        res[k] = {}

    for unit in dat:
        # format list desc
        if len(unit := unit.split(" ")) < 2:
            continue
        name = unit[0]

        tmp_excl = []
        for item in unit[1:]:
            if item[0] == "-":
                tmp_excl.append(item[1:])
            else:
                for k in keys:
                    if item in __raw[k]:
                        if name in res[k]:
                            res[k][name].update(__raw[k][item])
                        else:
                            res[k][name] = __raw[k][item]
        res["domain"][name] = __dn_mini(res["domain"][name])

        tmp_exdn = set()
        for item in tmp_excl:
            for k in keys:
                if name in res[k]:
                    if item in res[k]:
                        if k == "domain":
                            tmp_exdn.update(res["domain"][item])
                        else:
                            res[k][name].difference_update(res[k][item])
                    elif item in __raw[k]:
                        if k == "domain":
                            tmp_exdn.update(__raw["domain"][item])
                        else:
                            res[k][name].difference_update(__raw[k][item])
        if len(tmp_exdn) > 0:
            res["domain"][name] = __dn_rm(res["domain"][name], tmp_exdn)


def get() -> dict:
    ret = {}
    for k1, v1 in res.items():
        ret[k1] = {}
        for k2, v2 in v1.items():
            ret[k1][k2] = tuple(sorted(v2))
    return ret
