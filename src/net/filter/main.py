import os
import re
import requests
import yaml

# load data
with open("var/net/filter/main.yml", "tr", encoding="utf-8") as file:
    Data = yaml.safe_load(file)

# variables
NoMc = {}

# start
for Filter in Data:
    LoNo = []
    # load patterns and out
    Pattern = []
    Out = {}
    for keyLs in Filter["sub"]:
        Out[keyLs] = []
        for keyRe in Filter["sub"][keyLs]:
            Pattern.append((re.compile(Filter["sub"][keyLs][keyRe]), keyLs, keyRe))
    # get filter
    for item in requests.get(Filter["uri"], timeout=1000).text.split("\n"):
        for pat in Pattern:
            # match pattern
            if line := re.match(pat[0], item.lower()):
                # match type
                if pat[2] == "ds":
                    Out[pat[1]].append("+." + line.group(1))
                if pat[2] == "dn":
                    Out[pat[1]].append(line.group(1))
                break
        else:
            LoNo.append(item)
    # output
    for key, con in Out.items():
        with open(
            "out/net/clash/" + Filter["id"] + "-" + key + ".yml", "tw", encoding="utf-8"
        ) as file:
            yaml.safe_dump({"payload": con}, file)
    NoMc[Filter["id"]] = LoNo

# no match
if not os.path.exists("tmp/net/filter"):
    os.makedirs("tmp/net/filter")
with open("tmp/net/filter/no.yml", "tw", encoding="utf-8") as file:
    yaml.safe_dump(NoMc, file)
