import os

os.chdir(os.path.join(os.path.dirname(__file__), "../.."))

import argparse

arg = argparse.ArgumentParser()
arg.add_argument("-a", action="store_true", help="run once")
arg.add_argument("-i", action="store_true", help="init git repo & init python env")
arg.add_argument("-g", action="store_true", help="run scripts & generate out")
arg.add_argument("-n", action="store_true", help="clear out & run scripts")
arg.add_argument("-o", action="store_true", help="push out to branch etc")
args = arg.parse_args()

from cmd import cmd

if args.a:
    cmd.iniPip()
    cmd.run()
else:
    if args.i:
        cmd.iniPip()
        cmd.iniGit()
    if args.g and not args.n:
        cmd.run()
    if not args.g and args.n:
        cmd.outRm()
        cmd.run()
    if args.o:
        cmd.outPush()
