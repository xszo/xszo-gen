def insert_t(ls: list, tpl: list) -> list:
    res = []
    for item in tpl:
        if isinstance(item, str):
            if item == "=":
                res.extend(ls)
            if item[0] == "-":
                res.append(ls[int(item[1:])])
        else:
            res.append(item)
    return res
