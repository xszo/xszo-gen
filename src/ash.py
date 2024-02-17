from .filter.run import run as _filter
from .net.run import run as _net
from .out.run import run as _out
from .run.run import run as _run


def _gen() -> None:
    _net()
    _filter()
    _out()


def run() -> None:
    _run(_gen)
