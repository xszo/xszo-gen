import yaml
from pathlib import Path

with open("out/null", "tw", encoding="utf-8") as file:
    file.write("\n")

with open("var/base.yml", "tr", encoding="utf-8") as file:
    uri = yaml.safe_load(file)["uri"]

htmlHead = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>404</title></head><body><ul>'
htmlBody = ""
htmlTail = "</ul></body></html>"


def show(dire: Path, dirl: str):
    global htmlBody
    for item in dire.iterdir():
        if item.is_file():
            loc = dirl + item.name
            htmlBody += '<li><a href="' + uri + loc + '">' + loc + "</a></li>"
        else:
            loc = dirl + item.name + "/"
            htmlBody += "<li>" + loc + "</li><ul>"
            show(item, loc)
            htmlBody += "</ul>"


show(Path("out"), "")
with open("out/404.html", "tw", encoding="utf-8") as file:
    file.write(htmlHead + htmlBody + htmlTail)
