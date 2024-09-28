from .filter.run import run as _filter
from .net.run import run as _network
from .sh.run import run as _run


def _gen() -> None:
    _filter()
    _network()


_run(_gen)
