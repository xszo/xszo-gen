from argparse import ArgumentParser

from . import cmd

# get cli args
_arg = ArgumentParser()

_arg.add_argument("-a", action="store_true", help="run actions")
_arg.add_argument("-i", action="store_true", help="init git repo & init python env")
_arg.add_argument("-g", action="store_true", help="run scripts & generate out")
_arg.add_argument("-n", action="store_true", help="clear out & run scripts")
_arg.add_argument("-o", action="store_true", help="push out to branch etc")

args = _arg.parse_args()


# call modules
def run(do: callable) -> None:
    if args.a:
        cmd.ini_pip()
        do()

    else:
        if args.i:
            cmd.ini_pip()
            cmd.ini_git()
        if args.g and not args.n:
            do()
        if not args.g and args.n:
            cmd.out_rm()
            do()
        if args.o:
            cmd.out_push()
