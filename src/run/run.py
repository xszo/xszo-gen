from argparse import ArgumentParser
from os import system

# get cli args
_arg = ArgumentParser()

_arg.add_argument("-a", action="store_true", help="run actions")
_arg.add_argument("-i", action="store_true", help="initialize")
_arg.add_argument("-g", action="store_true", help="generate")

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
git switch -f etc;
git pull -r;
cd ..;
"""
        )
    # generate
    if arg.a or arg.g:
        gen()

    if arg.c:
        system(
            """
npx prettier . --write;
python -m black .;
python -m isort . --profile black;
"""
        )
