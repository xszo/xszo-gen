from filter.run import run as _filter
from net.run import run as _net
from run.run import run as _run


def _gen() -> None:
    _filter()
    _net()


_run(_gen)
