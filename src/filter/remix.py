from . import ren

# Var
res = {}
__src = {}


def let(lsrc: dict) -> None:
    for ty, v1 in lsrc.items():
        __src[ty] = {}
        for key, v2 in v1.items():
            __src[ty][key] = set(v2)


def __dn_mini(raw: set | list) -> set:
    ret = set()
    for i in ren.LEVEL_DN:
        # add level
        suffix = set(x for x in raw if x[0] == "." and x.count(".") == i)
        ret.update(suffix)
        # remove children
        raw = set(x for x in raw if not ("." + ".".join(x.split(".")[-i:])) in suffix)
    ret.update(raw)
    return ret


def __dn_rm(raw: set | list, rm: set | list):
    for i in ren.LEVEL_DN:
        # remove parent
        raw.difference_update(
            set("." + ".".join(x.split(".")[-i:]) for x in rm if x.count(".") >= i)
        )
        # remove children
        suffix = set(x for x in rm if x[0] == "." and x.count(".") == i)
        raw = set(x for x in raw if not ("." + ".".join(x.split(".")[-i:])) in suffix)
    return raw


def mix(dat: list) -> None:
    types = __src.keys()
    for k in types:
        res[k] = {}

    for unit in dat:
        # format list desc
        if len(unit := unit.split(" ")) < 2:
            continue
        name = unit[0]
        # incl
        tmp_excl = []
        for item in unit[1:]:
            if item[0] == "-":
                tmp_excl.append(item[1:])
            else:
                for k in types:
                    if item in __src[k]:
                        if name in res[k]:
                            res[k][name].update(__src[k][item])
                        else:
                            res[k][name] = __src[k][item]
        res["domain"][name] = __dn_mini(res["domain"][name])
        # excl
        tmp_exdn = set()
        for item in tmp_excl:
            for k in types:
                if name in res[k]:
                    if item in res[k]:
                        if k == "domain":
                            tmp_exdn.update(res["domain"][item])
                        else:
                            res[k][name].difference_update(res[k][item])
                    elif item in __src[k]:
                        if k == "domain":
                            tmp_exdn.update(__src["domain"][item])
                        else:
                            res[k][name].difference_update(__src[k][item])
        if len(tmp_exdn) > 0:
            res["domain"][name] = __dn_rm(res["domain"][name], tmp_exdn)


def get() -> dict:
    ret = {}
    for ty, v1 in res.items():
        ret[ty] = {}
        for key, v2 in v1.items():
            ret[ty][key] = tuple(sorted(v2))
    return ret
