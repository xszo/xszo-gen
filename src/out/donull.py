from pathlib import Path
from shutil import copyfile, copytree

from .ren import Var


def do() -> None:
    copytree(Var.PATH["src"] + "raw/", Var.PATH["out"], dirs_exist_ok=True)
    for item in Var.RAW:
        copyfile(item, Var.PATH["out"] + item)
    if Path(Var.PATH["var"]).is_dir():
        copytree(Var.PATH["var"], Var.PATH["out"], dirs_exist_ok=True)
    with open(Var.PATH["out.null"], "tw", encoding="utf-8") as file:
        file.write("\n")
