from pathlib import Path

import yaml

from var import var

# load var
html_head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>etc</title></head><body>'
html_404 = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>404</title></head><body><h1>404 Not Found</h1>'
html_tail = "</body></html>"
# load data
with open(var.PATH["var.base"], "tr", encoding="utf-8") as file:
    uri = yaml.safe_load(file)["uri"]


# file tree to html tree
def show(dire: Path, dirl: str):
    html = "<ul>"
    for item in sorted(dire.iterdir(), key=lambda v: v.name):
        loc = item.name
        if loc[0] == "." or (len(loc) > 5 and loc[-5:] == ".html"):
            continue
        if item.is_file():
            html += '<li><a href="' + uri + dirl + loc + '">' + loc + "</a></li>"
            continue
        if item.is_dir():
            html += '<li><a href="' + uri + dirl + loc + '/">' + loc + "/</a></li>"
            html += show(item, dirl + loc + "/")
    html += "</ul>"
    # create index
    with open(dire / "index.html", "tw", encoding="utf-8") as file:
        file.write(html_head + html + html_tail)
    return html


def do():
    # create 404 and index
    with open(var.PATH["out.404"], "tw", encoding="utf-8") as file:
        file.write(html_404 + show(Path(var.PATH["out"]), "") + html_tail)
