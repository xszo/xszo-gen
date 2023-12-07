import argparse
from subprocess import run

from var import VAR


def DoRun():
    for item in VAR["run-point"] + ["out"]:
        run([VAR["env-python"], "src/" + item + "/run.py"], check=True)


def DoIni():
    run(
        [VAR["env-python"], "-m", "pip", "install", "-r", "src/run/requirements.txt"],
        check=True,
    )


def DoGit():
    run(
        ["git", "submodule", "update", "--init", "--recursive", "--remote"],
        check=True,
    )
    run(
        """
    git switch -qf main
    cd doc
    git switch -qf master
    cd ../out
    git switch -qf etc
    git pull -q --rebase
    cd ..
    """,
        shell=True,
        check=True,
    )


def DoOut():
    run(
        """
    cd out
    git switch -q etc
    git add --all
    git commit -qm run --amend --reset-author
    git push -qf
    cd ..
    """,
        shell=True,
        check=True,
    )


arg = argparse.ArgumentParser()
arg.add_argument("-a", action="store_true", help="run once")
arg.add_argument("-i", action="store_true", help="init git repo & init python env")
arg.add_argument("-g", action="store_true", help="run scripts & generate out/")
arg.add_argument("-o", action="store_true", help="push out/ to branch etc")
arg.add_argument("-c", action="store", help="run commands")
args = arg.parse_args()

flag = True

if args.c:
    flag = False
    run("cd src/run; " + args.c + "; cd ../..;", shell=True, check=True)
if args.a:
    flag = False
    DoIni()
    DoRun()
if args.i:
    flag = False
    DoIni()
    DoGit()
if args.g:
    flag = False
    DoRun()
if args.o:
    flag = False
    DoOut()
if flag:
    DoRun()
