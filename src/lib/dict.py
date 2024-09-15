def merge(res: dict, ins: dict) -> None:
    for key, val in ins.items():
        if key in res:
            if isinstance(res[key], dict):
                merge(res[key], val)
            else:
                res[key] = val
        else:
            res[key] = val
