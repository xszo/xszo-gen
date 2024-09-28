from pathlib import Path

import yaml

PATH_TMP = Path("tmp/")
PATH_TMP_NET = PATH_TMP / "net"
PATH_TMP_FILTER = PATH_TMP / "filter"

PATH_SRC_NET = Path("src/net/")
PATH_SRC_FILTER = Path("src/filter/")

PATH_VAR = Path("var/")
PATH_VAR_NET = PATH_VAR / "net"
PATH_VAR_FILTER = PATH_VAR / "filter"

PATH_OUT = Path("out/")

with open("var/ren.yml", "tr", encoding="utf-8") as __file:
    __var = yaml.safe_load(__file)

URI = __var["uri"]
ICO = __var["ico"]
INT = __var["int"]
