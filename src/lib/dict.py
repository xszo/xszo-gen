def merge(var1: dict, var2: dict) -> dict:
    for key, val in var2.items():
        if key in var1:
            if isinstance(var1[key], dict):
                merge(var1[key], val)
            else:
                var1[key] = val
        else:
            var1[key] = val
