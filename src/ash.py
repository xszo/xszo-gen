from .filter.run import run as _filter
from .net.run import run as _net
from .run.run import run as _run


def _gen() -> None:
    _net()
    _filter()


def run() -> None:
    _run(_gen)
