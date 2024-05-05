import yaml

from . import ren


class Dump:
    __raw = None

    def __init__(self) -> None:
        (ren.PATH_OUT / "surge").mkdir(parents=True, exist_ok=True)
        (ren.PATH_OUT / "clash").mkdir(parents=True, exist_ok=True)

    def __ref(self, als: dict) -> None:
        ref = {
            "list": {
                "dn": als["domain"],
                "ip": als["ip"],
            },
            "dn": {},
            "ip": {},
            "misc": {},
        }

        for k in ref["list"]["dn"]:
            ref["dn"]["surge-" + k] = "surge/filter-dn+" + k + ".txt"
            ref["dn"]["clash-" + k] = "clash/filter-dn+" + k + ".yml"
        for k in ref["list"]["ip"]:
            ref["ip"]["surge-" + k] = "surge/filter-ip+" + k + ".txt"
            ref["ip"]["clash-" + k] = "clash/filter-ip+" + k + ".yml"

        with open(ren.PATH_TMP / "list.yml", "tw", encoding="utf-8") as file:
            yaml.safe_dump(ref, file)

    def __domain(self) -> None:
        for key, val in self.__raw["domain"].items():
            # dump clash
            with open(
                ren.PATH_OUT / "clash" / ("filter-dn+" + key + ".yml"),
                "tw",
                encoding="utf-8",
            ) as file:
                yaml.safe_dump(
                    {"payload": ["+" + x if x[0] == "." else x for x in val]}, file
                )
            # dump surge
            with open(
                ren.PATH_OUT / "surge" / ("filter-dn+" + key + ".txt"),
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines([x + "\n" for x in val])

        return self.__raw["domain"].keys()

    def __ip(self) -> None:
        types = ["ip4", "ip6", "ipasn", "ipgeo"]

        raw = {}
        for key in types:
            for k, v in self.__raw[key].items():
                if not k in raw:
                    raw[k] = {}
                raw[k][key] = v

        for key, val in raw.items():
            line = []
            if "ip4" in val:
                line.extend(["IP-CIDR," + x for x in val["ip4"]])
            if "ip6" in val:
                line.extend(["IP-CIDR6," + x for x in val["ip6"]])
            if "ipasn" in val:
                line.extend(["IP-ASN," + x for x in val["ipasn"]])
            if "ipgeo" in val:
                line.extend(["GEOIP," + x for x in val["ipgeo"]])

            with open(
                ren.PATH_OUT / "surge" / ("filter-ip+" + key + ".txt"),
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines([x + "\n" for x in line])
            with open(
                ren.PATH_OUT / "clash" / ("filter-ip+" + key + ".yml"),
                "tw",
                encoding="utf-8",
            ) as file:
                yaml.safe_dump(
                    {"payload": line},
                    file,
                )

        return raw.keys()

    def dump(self, araw: dict) -> None:
        self.__raw = araw
        self.__ref({"domain": tuple(self.__domain()), "ip": tuple(self.__ip())})
