from pathlib import Path

import yaml

from var import VAR

# load var
htmlHead = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>etc</title></head><body>'
html404 = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>404</title></head><body><h1>404 Not Found</h1>'
htmlTail = "</body></html>"
# load data
with open(VAR["path"]["var.base"], "tr", encoding="utf-8") as file:
    uri = yaml.safe_load(file)["uri"]


# file tree to html tree
def show(dire: Path, dirl: str):
    htmlBody = "<ul>"
    for item in sorted(dire.iterdir(), key=lambda v: v.name):
        loc = item.name
        if loc[0] == "." or (len(loc) > 5 and loc[-5:] == ".html"):
            continue
        if item.is_file():
            htmlBody += '<li><a href="' + uri + dirl + loc + '">' + loc + "</a></li>"
            continue
        if item.is_dir():
            htmlBody += '<li><a href="' + uri + dirl + loc + '/">' + loc + "/</a></li>"
            htmlBody += show(item, dirl + loc + "/")
    htmlBody += "</ul>"
    # create index
    with open(dire / "index.html", "tw", encoding="utf-8") as file:
        file.write(htmlHead + htmlBody + htmlTail)
    return htmlBody


def do():
    # create 404 and index
    with open(VAR["path"]["out.404"], "tw", encoding="utf-8") as file:
        file.write(html404 + show(Path(VAR["path"]["out"]), "") + htmlTail)
