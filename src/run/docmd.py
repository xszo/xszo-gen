from subprocess import run

from ren import Var


class CommandLine:
    def shell(command):
        run(
            "cd " + Var.PATH["run"] + "; " + command + "; cd " + Var.PATH["pan"] + ";",
            shell=True,
            check=True,
        )

    def run():
        for item in Var.RUN:
            run([Var.ENV["python"], "src/" + item + "/run.py"], check=True)

    def ini_pip():
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

    def ini_git():
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

    def out_push():
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

    def out_rm():
        run("rm -rf out/*", shell=True, check=True)
