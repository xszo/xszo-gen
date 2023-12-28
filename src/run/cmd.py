from subprocess import run

from var import var


class cmd:
    def shell(command):
        run(
            "cd " + var.PATH["run"] + "; " + command + "; cd " + var.PATH["pan"] + ";",
            shell=True,
            check=True,
        )

    def run():
        for item in var.RUN:
            run([var.ENV["python"], "src/" + item + "/run.py"], check=True)

    def iniPip():
        run(
            [
                var.ENV["python"],
                "-m",
                var.ENV["pip"],
                "install",
                "-r",
                var.PATH["pip"],
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

    def outPush():
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

    def outRm():
        run("rm -rf out/*", shell=True, check=True)
