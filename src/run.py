import os

from filter.run import run as run_filter
from net.run import run as run_net
from out.run import run as run_out
from run.run import run

os.chdir(os.path.join(os.path.dirname(__file__), ".."))


def do():
    run_net()
    run_filter()
    run_out()


run(do)
