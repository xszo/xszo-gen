import yaml

from . import dump, getrex, getvar, getvlc, remix, ren


def run() -> None:
    getvlc.init()
    getrex.init()
    dump.init()

    with open(ren.PATH_VAR_LIST, "tr", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    val = getvar.get()
    getrex.letvar(data["var"])
    val["domain"].update(getrex.get(data["get"]))
    val["domain"].update(getvlc.get(data["vlc"]))

    remix.let(val)
    remix.mix(data["list"])
    val = remix.get()

    dump.dump(val)
