from pathlib import Path
from subprocess import run

from ren import Var


def do() -> None:
    for item in Var.RAW:
        run(["cp", "-f", item, Var.PATH["out"] + item], check=True)
    if Path(Var.PATH["var"]).is_dir():
        run(["cp", "-rf", Var.PATH["var"] + "*", Var.PATH["out"]], check=True)
    with open(Var.PATH["out.null"], "tw", encoding="utf-8") as file:
        file.write("\n")
