from os import system
from subprocess import run

from ren import Var


class Command:
    def shell(self, command):
        system(
            "cd " + Var.PATH["run"] + "; " + command + "; cd " + Var.PATH["pan"] + ";"
        )

    def run(self):
        for item in Var.RUN:
            print("Run " + item)
            run([Var.ENV["python"], "src/" + item + "/run.py"], check=True)

    def ini_pip(self):
        run(
            [
                Var.ENV["python"],
                "-m",
                Var.ENV["pip"],
                "install",
                "-r",
                Var.PATH["pip"],
            ],
            check=True,
        )

    def ini_git(self):
        system(
            """
        git submodule update --init --recursive --remote;
        if ! git worktree list | grep -q out; then
            if [ -e out ]; then rm -rf out; fi
            git worktree add out;
        fi
        wait;
        git switch -f main;
        cd doc;
        git switch -f master;
        cd ../out;
        git switch -f etc;
        git pull -r;
        cd ..;
        """
        )

    def out_push(self):
        system(
            """
        cd out;
        git switch etc;
        git add -A;
        git commit --amend --reset-author -qm run;
        git push -qf;
        cd ..;
        """
        )

    def out_rm(self):
        system(
            """
        cd out;
        git switch -f etc;
        rm -rf *;
        cd ..;
        """
        )
