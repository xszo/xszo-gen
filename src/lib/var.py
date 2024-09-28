__var = {}


def let(key, val) -> None:
    __var[key] = val


def get(key):
    return __var[key]


def pop(key):
    return __var.pop(key)
