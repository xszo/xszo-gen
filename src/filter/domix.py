class Do:
    res = {}

    __src = None

    def __init__(self, i_src: dict) -> None:
        self.__src = i_src
        for key, val in self.__src.items():
            self.__src[key] = set(val)

    def mix(self, dat: list) -> dict:
        for unit in dat:
            if len(unit := unit.split(" ")) < 2:
                continue
            res = set()
            tmp = []
            for item in unit[1:]:
                if item[0] == "-":
                    tmp.append(item[1:])
                else:
                    res.update(self.__src[item])
            for item in tmp:
                res.difference(self.__src[item])
            self.res[unit[0]] = list(res)
        return self.res
