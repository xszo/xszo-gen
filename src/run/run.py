import argparse
import os
from subprocess import run

VAR = {
    "run-point": ["net", "filter", "out"],
    "env-python": "python3",
    "env-path": "src/run/",
}

os.chdir(os.path.join(os.path.dirname(__file__), "../.."))


class cmd:
    def shell(command):
        run(
            "cd " + VAR["env-path"] + "; " + command + "; cd ../..;",
            shell=True,
            check=True,
        )

    def run():
        for item in VAR["run-point"]:
            run([VAR["env-python"], "src/" + item + "/run.py"], check=True)

    def iniPip():
        run(
            [
                VAR["env-python"],
                "-m",
                "pip",
                "install",
                "-r",
                "src/run/requirements.txt",
            ],
            check=True,
        )

    def iniGit():
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

    def pushOut():
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

    def rmOut():
        run("rm -rf out/*", shell=True, check=True)


arg = argparse.ArgumentParser()
arg.add_argument("-a", action="store_true", help="run once")
arg.add_argument("-i", action="store_true", help="init git repo & init python env")
arg.add_argument("-g", action="store_true", help="run scripts & generate out/")
arg.add_argument("-n", action="store_true", help="run scripts & generate out/")
arg.add_argument("-o", action="store_true", help="push out/ to branch etc")
arg.add_argument("-c", action="store", help="run commands")
args = arg.parse_args()

flag = True

if args.c:
    flag = False
    cmd.shell(args.c)
if args.a:
    flag = False
    cmd.iniPip()
    cmd.run()
if args.i:
    flag = False
    cmd.iniPip()
    cmd.iniGit()
if args.g:
    flag = False
    cmd.run()
if args.n:
    flag = False
    cmd.rmOut()
    cmd.run()
if args.o:
    flag = False
    cmd.pushOut()
if flag:
    cmd.run()
