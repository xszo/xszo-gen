import argparse
from subprocess import run
from var import data

parsearg = argparse.ArgumentParser()
parsearg.add_argument("-a", dest="oA", action="store_true", help="run once")
parsearg.add_argument("-i", dest="oI", action="store_true", help="install")
parsearg.add_argument("-g", dest="oG", action="store_true", help="generate")
parsearg.add_argument("-o", dest="oO", action="store_true", help="output")
args = parsearg.parse_args()

if args.oA:
    run([data["env-python"], "src/run/ini-python.py"], check=True)
    run([data["env-python"], "src/run/gen.py"], check=True)
if args.oI:
    run([data["env-python"], "src/run/ini-unix.py"], check=True)
    run([data["env-python"], "src/run/ini-python.py"], check=True)
    run([data["env-python"], "src/run/ini-git.py"], check=True)
if args.oG:
    run([data["env-python"], "src/run/gen.py"], check=True)
if args.oO:
    run([data["env-python"], "src/run/out.py"], check=True)
