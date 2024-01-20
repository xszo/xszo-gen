from pathlib import Path

import yaml

from .ren import Var


class Do:
    __uri = None
    # html code
    __html_head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>etc</title></head><body>'
    __html_tail = "</ul></body></html>"
    __msg_index = "<h2>Index</h2><ul>"
    __msg_404 = "<h2>404 Not Found</h2><ul>"

    def __init__(self):
        with open(Var.PATH["var.base"], "tr", encoding="utf-8") as file:
            self.__uri = yaml.safe_load(file)["uri"]

    # file tree to html tree
    def __show(self, dire: Path, dirl: str):
        html = ""
        for item in sorted(dire.iterdir(), key=lambda v: v.name):
            loc = item.name
            if loc[0] == "." or (len(loc) > 5 and loc[-5:] == ".html"):
                continue
            if item.is_file():
                # ret if file
                html += (
                    '<li><a href="' + self.__uri + dirl + loc + '">' + loc + "</a></li>"
                )
                continue
            if item.is_dir():
                # itr if directory
                inner = self.__show(item, dirl + loc + "/")
                # add html
                html += (
                    '<li><a href="'
                    + self.__uri
                    + dirl
                    + loc
                    + '/">'
                    + loc
                    + "/</a></li><ul>"
                    + inner
                    + "</ul>"
                )
                # add index
                inner = (
                    self.__html_head
                    + "<h2>"
                    + dirl
                    + loc
                    + '/</h2><ul><li><a href="'
                    + self.__uri
                    + dirl
                    + '">../</a></li>'
                    + inner
                    + self.__html_tail
                )
                with open(item / "index.html", "tw", encoding="utf-8") as file:
                    file.write(inner)
        return html

    # create 404 and index
    def do(self):
        html = self.__show(Path(Var.PATH["out"]), "")
        with open(Var.PATH["out"] + "index.html", "tw", encoding="utf-8") as file:
            file.write(self.__html_head + self.__msg_index + html + self.__html_tail)
        with open(Var.PATH["out.404"], "tw", encoding="utf-8") as file:
            file.write(self.__html_head + self.__msg_404 + html + self.__html_tail)
