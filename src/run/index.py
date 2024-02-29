from pathlib import Path

import yaml

from . import ren

# data
_html_head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>etc</title></head><body>'
_html_tail = "</ul></body></html>"

with open(ren.PATH_VAR_BASE, "tr", encoding="utf-8") as file:
    _uri = yaml.safe_load(file)["uri"]


# file tree to html tree
def _show(adir: Path, arel: str) -> str:
    html = ""
    # iter dir out/
    for item in sorted(adir.iterdir(), key=lambda v: v.name):
        loc = item.name
        # skip if hidden or html
        if loc[0] == "." or (len(loc) > 5 and loc[-5:] == ".html"):
            continue
        # ret if file
        if item.is_file():
            html += '<li><a href="' + _uri + arel + loc + '">' + loc + "</a></li>"
            continue
        # itr if directory
        if item.is_dir():
            inner = _show(item, arel + loc + "/")
            # add html
            html += (
                '<li><a href="'
                + _uri
                + arel
                + loc
                + '/">'
                + loc
                + "/</a></li><ul>"
                + inner
                + "</ul>"
            )
            # add index
            with open(item / "index.html", "tw", encoding="utf-8") as file:
                file.write(
                    _html_head
                    + "<h2>"
                    + arel
                    + loc
                    + '/</h2><ul><li><a href="'
                    + _uri
                    + arel
                    + '">../</a></li>'
                    + inner
                    + _html_tail
                )
    return html


def do() -> None:
    html = _show(ren.PATH_OUT, "")
    # create index
    with open(ren.PATH_OUT / "index.html", "tw", encoding="utf-8") as file:
        file.write(_html_head + "<h2>Index</h2><ul>" + html + _html_tail)
    # create 404
    with open(ren.PATH_OUT / "404.html", "tw", encoding="utf-8") as file:
        file.write(_html_head + "<h2>404 Not Found</h2><ul>" + html + _html_tail)
