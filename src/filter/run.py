import re
from base64 import b64decode
from pathlib import Path

import requests
import yaml
from ren import Var

# load data
with open(Var.PATH["var.list"], "tr", encoding="utf-8") as file:
    data = yaml.safe_load(file)
# compile variable pattern
re_tmp = []
for name, line in data["var"].items():
    re_tmp.append((re.compile("\\\\=" + name + "\\\\"), line))
data["var"] = re_tmp + [(re.compile("\\\\=\\w*\\\\"), "")]
data["com"] = re.compile(Var.REX["comment"])  # comment line

# path of tmp file
cc = Path(Var.PATH["tmp"])
cc.mkdir(parents=True, exist_ok=True)

# variables
no_match = {}  # not matched

# start
for unit in data["list"]:
    lo_nomc = []
    # load patterns and out
    re_pat = []
    out = {}
    for key in unit["reg"]:
        # each sublist
        for item in unit["reg"][key]:
            # insert variables
            for val in data["var"]:
                item = re.sub(val[0], val[1], item)
            # compile pattern
            item = item.split("  ")
            re_pat.append((re.compile(item[0]), item[1], key))
        # ini output obj
        out[key] = []
    # get remote filter
    raw = requests.get(unit["uri"], timeout=1000).text
    # pre process
    if "b64" in unit["pre"]:
        raw = b64decode(raw).decode("utf-8")
    # loop lines
    for item in raw.splitlines():
        if re.match(data["com"], item):
            continue
        # match pattern
        for pat in re_pat:
            # find 1 and rewrite 2
            if line := re.match(pat[0], item):
                out[pat[2]].append(line.expand(pat[1]))
                break
        else:
            # no match
            lo_nomc.append(item)
    # drop dupl
    for key in out:
        out[key] = list(dict.fromkeys(out[key]))
    # output
    for key, con in out.items():
        # + means prefix, * means any
        if "gen" in data["tar"]:
            with open(cc / (unit["id"] + key + ".yml"), "tw", encoding="utf-8") as file:
                yaml.safe_dump(
                    {"domain": [x[2:] if x[0] == "+" else "-" + x for x in con]},
                    file,
                )
        if "clash" in data["tar"]:
            with open(
                Var.PATH["out.clash"] + unit["id"] + key + ".yml",
                "tw",
                encoding="utf-8",
            ) as file:
                yaml.safe_dump({"payload": con}, file)
        if "surge" in data["tar"]:
            with open(
                Var.PATH["out.surge"] + unit["id"] + key + ".txt",
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines(
                    [x[1:] + "\n" if x[0] == "+" else x + "\n" for x in con]
                )
    # log not matched ones
    no_match[unit["id"]] = lo_nomc
with open(cc / "no.yml", "tw", encoding="utf-8") as file:
    yaml.safe_dump(no_match, file)
