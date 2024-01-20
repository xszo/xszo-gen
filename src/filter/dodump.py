import yaml

from .ren import Var


class Do:
    __src = None

    def __init__(self, i_src: dict) -> None:
        self.__src = i_src

    def dump(self, loc: list) -> None:
        for key, val in self.__src.items():
            if "clash" in loc:
                with open(
                    Var.PATH["out.clash"] + key + ".yml",
                    "tw",
                    encoding="utf-8",
                ) as file:
                    yaml.safe_dump({"payload": val}, file)
            if "surge" in loc:
                with open(
                    Var.PATH["out.surge"] + key + ".txt",
                    "tw",
                    encoding="utf-8",
                ) as file:
                    file.writelines(
                        [x[1:] + "\n" if x[0] == "+" else x + "\n" for x in val]
                    )
