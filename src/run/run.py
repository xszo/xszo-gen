from argparse import ArgumentParser

from . import cmd
from .out import copy

# get cli args
_arg = ArgumentParser()

_arg.add_argument("-i", action="store_true", help="init repo & env")
_arg.add_argument("-d", action="store_true", help="init also dev")
_arg.add_argument("-g", action="store_true", help="generate out")
_arg.add_argument("-n", action="store_true", help="clear & generate out")
_arg.add_argument("-o", action="store_true", help="generate & push out")
_arg.add_argument("-c", action="store_true", help="code clean")
_arg.add_argument("-a", action="store_true", help="run actions")

args = _arg.parse_args()


# call modules
def run(gen: callable) -> None:
    def g() -> None:
        gen()
        copy()

    if args.i:
        cmd.ini_git()
        if args.d:
            cmd.ini_dev()
    if args.g:
        g()
    if args.n:
        cmd.out_rm()
        g()
    if args.o:
        cmd.out_rm()
        g()
        cmd.out_push()

    if args.c:
        cmd.fmt()

    if args.a:
        g()
        cmd.out_push()
