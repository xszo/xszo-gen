import yaml
from pathlib import Path

with open("out/null", "tw", encoding="utf-8") as file:
    file.write("\n")

with open("var/base.yml", "tr", encoding="utf-8") as file:
    uri = yaml.safe_load(file)["uri"]

htmlHead = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>etc</title></head><body>'
htmlTail = "</body></html>"


def show(dire: Path, dirl: str):
    htmlBody = "<ul>"
    for item in sorted(dire.iterdir(), key=lambda v: v.name):
        if item.name[0] == "." or item.name.split(".")[-1] == "html":
            continue
        if item.is_file():
            loc = dirl + item.name
            htmlBody += '<li><a href="' + uri + loc + '">' + loc + "</a></li>"
            continue
        if item.is_dir():
            loc = dirl + item.name + "/"
            htmlBody += '<li><a href="' + uri + loc + '">' + loc + "</a></li>"
            htmlBody += show(item, loc)
    htmlBody += "</ul>"
    with open(dire / "index.html", "tw", encoding="utf-8") as file:
        file.write(htmlHead + htmlBody + htmlTail)
    return htmlBody


with open("out/404.html", "tw", encoding="utf-8") as file:
    file.write(htmlHead + show(Path("out"), "") + htmlTail)
