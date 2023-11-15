import re
import yaml
from base64 import b64decode
from pathlib import Path
from requests import get as download

# load data
with open("var/net/filter/list.yml", "tr", encoding="utf-8") as file:
    Data = yaml.safe_load(file)
# compile variable pattern
ReVar = []
for name, line in Data["var"].items():
    ReVar.append((re.compile("\\\\=" + name + "\\\\"), line))
Data["var"] = ReVar + [(re.compile("\\\\=\\w+\\\\"), "")]
# path of tmp file
ccPath = Path("tmp/net/filter")
ccPath.mkdir(parents=True, exist_ok=True)

# variables
ReCom = re.compile("^ *($|#|!)")  # comment line
NoMc = {}  # not matched

# start
for unit in Data["list"]:
    LoNoMc = []
    # load patterns and out
    Pattern = []
    Out = {}
    for key in unit["reg"]:
        # each sublist
        for item in unit["reg"][key]:
            # insert variables
            for val in Data["var"]:
                item = re.sub(val[0], val[1], item)
            # compile pattern
            item = item.split(" ")
            Pattern.append((re.compile(item[0]), item[1], key))
        # ini output obj
        Out[key] = []
    # get remote filter
    Raw = download(unit["uri"], timeout=1000).text
    if "b64" in unit["pre"]:
        Raw = b64decode(Raw).decode("utf-8")
    # loop lines
    for item in Raw.splitlines():
        if re.match(ReCom, item):
            continue
        # match pattern
        for pat in Pattern:
            # find 1 and rewrite 2
            if line := re.match(pat[0], item):
                Out[pat[2]].append(line.expand(pat[1]))
                break
        else:
            # no match
            LoNoMc.append(item)
    # drop dupl
    for key in Out:
        Out[key] = list(dict.fromkeys(Out[key]))
    # output
    for key, con in Out.items():
        if "gen" in Data["tar"]:
            with open(
                ccPath / (unit["id"] + key + ".yml"), "tw", encoding="utf-8"
            ) as file:
                yaml.safe_dump(
                    {"domain": [x[2:] if x[0] == "+" else "-" + x for x in con]},
                    file,
                )
        if "clash" in Data["tar"]:
            with open(
                "out/net/clash/f-" + unit["id"] + key + ".yml", "tw", encoding="utf-8"
            ) as file:
                yaml.safe_dump({"payload": con}, file)
        if "surge" in Data["tar"]:
            with open(
                "out/net/surge/f-" + unit["id"] + key + ".txt", "tw", encoding="utf-8"
            ) as file:
                file.writelines(
                    [x[1:] + "\n" if x[0] == "+" else x + "\n" for x in con]
                )
        if "quantumult" in Data["tar"]:
            with open(
                "out/net/quantumult/f-" + unit["id"] + key + ".txt",
                "tw",
                encoding="utf-8",
            ) as file:
                file.writelines(
                    [
                        "host-suffix," + x[2:] + ",o\n"
                        if x[0] == "+"
                        else "host," + x + ",o\n"
                        for x in con
                    ]
                )
    # log not matched ones
    NoMc[unit["id"]] = LoNoMc
with open(ccPath / "no.yml", "tw", encoding="utf-8") as file:
    yaml.safe_dump(NoMc, file)