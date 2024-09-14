import yaml

from . import ren

# Var
res = {"domain": {}, "ip4": {}, "ip6": {}, "ipasn": {}, "ipgeo": {}}


def get() -> dict:
    global res
    for ls in ren.PATH_VAR.iterdir():
        if ls == ren.PATH_VAR_LIST:
            continue
        loc = ls.name.split(".")[0]

        with open(
            ls,
            "tr",
            encoding="utf-8",
        ) as file:
            raw = yaml.safe_load(file)

        if "domain" in raw:

            def conv_domain(item: str) -> str:
                if item[0] == "-":
                    return item[1:]
                else:
                    return "." + item

            res["domain"][loc] = [conv_domain(item) for item in raw["domain"]]

        if "ipcidr" in raw:
            tmp = [line for line in raw["ipcidr"] if not line[0] == "["]
            if len(tmp) > 0:
                res["ip4"][loc] = tmp

            tmp = [line[1:-1] for line in raw["ipcidr"] if line[0] == "["]
            if len(tmp) > 0:
                res["ip6"][loc] = tmp

        if "ipgeo" in raw:
            res["ipgeo"][loc] = [item.upper() for item in raw["ipgeo"]]

        if "ipasn" in raw:
            res["ipasn"][loc] = [str(item) for item in raw["ipasn"]]

    return res
