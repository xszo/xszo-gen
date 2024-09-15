from pathlib import Path

import yaml

PATH_TMP = Path("tmp/")
PATH_TMP_NET = Path("tmp/net/")
PATH_TMP_FILTER = Path("tmp/filter/")

PATH_SRC_NET = Path("src/net/")
PATH_SRC_FILTER = Path("src/filter/")

PATH_VAR_NET = Path("var/net/")
PATH_VAR_FILTER = Path("var/filter/")
PATH_VAR_BASE = Path("var/base.yml")
PATH_VAR_REX = Path("var/re.yml")

PATH_OUT = Path("out/")
PATH_OUT_NET = Path("out/network/")

with open(PATH_VAR_BASE, "tr", encoding="utf-8") as __file:
    __var_base = yaml.safe_load(__file)

URI = __var_base["uri"]
ICO = __var_base["ico"]
