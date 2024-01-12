import re
from base64 import b64decode
from pathlib import Path

import requests
import yaml
from ren import VAR


class Do:
    def do(self):
        # load data
        with open(VAR["path"]["var.list"], "tr", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # compile variable pattern
        re_tmp = []
        for name, line in data["var"].items():
            re_tmp.append((re.compile("\\\\=" + name + "\\\\"), line))
        data["var"] = re_tmp + [(re.compile("\\\\=\\w*\\\\"), "")]
        data["com"] = re.compile(VAR["rex"]["comment"])  # comment line

        # flag mode
        if "gen" in data["tar"]:
            FLAG = True
            # path of tmp file
            cc = Path(VAR["path"]["tmp"])
            cc.mkdir(parents=True, exist_ok=True)
            # not matched
            cc_no = {}
        else:
            FLAG = False

        # start
        for unit in data["list"]:
            # load patterns and out
            re_pat = []
            out = {}
            cc_out = {}
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
                cc_out[key] = []

            # get remote filter
            raw = requests.get(unit["uri"], timeout=1000).text

            # pre process
            if "b64" in unit["pre"]:
                raw = b64decode(raw).decode("utf-8")

            # loop lines
            for item in raw.splitlines():
                if not re.match(data["com"], item):
                    for pat in re_pat:
                        # find 1 and rewrite 2
                        if line := re.match(pat[0], item):
                            out[pat[2]].append(line.expand(pat[1]))
                            break

            # drop dupl
            for key in out:
                out[key] = list(dict.fromkeys(out[key]))

            # output
            for key, con in out.items():
                # + means prefix, * means any
                if "clash" in data["tar"]:
                    with open(
                        VAR["path"]["out.clash"] + unit["id"] + key + ".yml",
                        "tw",
                        encoding="utf-8",
                    ) as file:
                        yaml.safe_dump({"payload": con}, file)
                if "surge" in data["tar"]:
                    with open(
                        VAR["path"]["out.surge"] + unit["id"] + key + ".txt",
                        "tw",
                        encoding="utf-8",
                    ) as file:
                        file.writelines(
                            [x[1:] + "\n" if x[0] == "+" else x + "\n" for x in con]
                        )

            # flag mode
            if FLAG:
                for idx, item in enumerate(re_pat):
                    if item[1][0] == "+":
                        re_pat[idx] = (item[0], item[1][2:], item[2])
                    else:
                        re_pat[idx] = (item[0], "-" + item[1], item[2])
                lo_no = []
                for item in raw.splitlines():
                    if not re.match(data["com"], item):
                        for pat in re_pat:
                            if line := re.match(pat[0], item):
                                cc_out[pat[2]].append(
                                    "- " + line.expand(pat[1]) + " # " + item + "\n"
                                )
                                break
                        else:
                            lo_no.append(item)
                cc_no[unit["id"]] = lo_no
                for key, val in cc_out.items():
                    with open(
                        cc / (unit["id"] + key + ".yml"), "tw", encoding="utf-8"
                    ) as file:
                        file.write("domain:\n")
                        file.writelines(val)

        if FLAG:
            with open(cc / "no.yml", "tw", encoding="utf-8") as file:
                yaml.safe_dump(cc_no, file)
