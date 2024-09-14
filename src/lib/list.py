def insert_tp(ls1: list, ls2: list) -> list:
    res = []
    for item in ls2:
        if isinstance(item, str):
            if item == "=":
                res.extend(ls1)
            if item[0] == "-":
                res.append(ls1[int(item[1:])])
        else:
            res.append(item)
    return res
