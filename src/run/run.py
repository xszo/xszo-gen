from argparse import ArgumentParser
from os import system

# get cli args
_arg = ArgumentParser()

_arg.add_argument("-a", action="store_true", help="run actions")
_arg.add_argument("-i", action="store_true", help="init repo & env")
_arg.add_argument("-g", action="store_true", help="generate out")
_arg.add_argument("-n", action="store_true", help="clear & generate out")
_arg.add_argument("-o", action="store_true", help="generate & push out")
_arg.add_argument("-c", action="store_true", help="code clean")

arg = _arg.parse_args()


# call modules
def run(gen: callable) -> None:
    # init repo
    if arg.i:
        system(
            """
        git submodule update --init --recursive --remote;
        git clone https://github.com/xszo/etc out;
        wait;
        git switch main;
        cd doc;
        git switch master;
        cd ../out;
        git switch etc;
        cd ..;
        """
        )
    # clear out dir
    if arg.n or arg.o:
        system(
            """
        cd out;
        git switch -f etc;
        rm -rf network surge clash;
        cd ..;
        """
        )
    # generate
    if arg.a or arg.g or arg.n or arg.o:
        gen()
    # push out to branch
    if arg.o:
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

    if arg.c:
        system(
            """
        npx prettier . --write;
        python3 -m black .;
        python3 -m isort . --profile black;
        """
        )
