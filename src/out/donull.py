from var import VAR


# create file null
def do():
    with open(VAR["path"]["out.null"], "tw", encoding="utf-8") as file:
        file.write("\n")
