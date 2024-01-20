from argparse import ArgumentParser

from .cmd import Command

cmd = Command()

arg = ArgumentParser()

arg.add_argument("-a", action="store_true", help="run actions")
arg.add_argument("-i", action="store_true", help="init git repo & init python env")
arg.add_argument("-g", action="store_true", help="run scripts & generate out")
arg.add_argument("-n", action="store_true", help="clear out & run scripts")
arg.add_argument("-o", action="store_true", help="push out to branch etc")

args = arg.parse_args()


def run(do) -> None:
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
