import os
from argparse import ArgumentParser

from docmd import CommandLine
from ren import Var

os.chdir(os.path.join(os.path.dirname(__file__), Var.PATH["pan"]))

arg = ArgumentParser()
arg.add_argument("-a", action="store_true", help="run once")
arg.add_argument("-i", action="store_true", help="init git repo & init python env")
arg.add_argument("-g", action="store_true", help="run scripts & generate out")
arg.add_argument("-n", action="store_true", help="clear out & run scripts")
arg.add_argument("-o", action="store_true", help="push out to branch etc")
args = arg.parse_args()

if args.a:
    CommandLine.ini_pip()
    CommandLine.run()
else:
    if args.i:
        CommandLine.ini_pip()
        CommandLine.ini_git()
    if args.g and not args.n:
        CommandLine.run()
    if not args.g and args.n:
        CommandLine.out_rm()
        CommandLine.run()
    if args.o:
        CommandLine.out_push()
