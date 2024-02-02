from pathlib import Path

import yaml

PATH_SRC = Path("src/net/")
PATH_VAR = Path("var/net/")
PATH_VAR_BASE = Path("var/base.yml")
PATH_VAR_REX = Path("var/re.yml")
PATH_VAR_LIST = Path("var/net/list.yml")
PATH_VAR_FILTER = Path("var/filter/")
PATH_OUT = Path("out/network/")
PATH_OUT_CLASH = Path("out/clash/")
PATH_OUT_SURGE = Path("out/surge/")

EXT_QUANTUMULT_PARSER = "https://raw.githubusercontent.com/KOP-XIAO/QuantumultX/master/Scripts/resource-parser.js"

with open(PATH_VAR_BASE, "tr", encoding="utf-8") as _in:
    URI = yaml.safe_load(_in)["uri"]
URI_NET = URI + "network/"
URI_CLASH = URI + "clash/"
URI_SURGE = URI + "surge/"
