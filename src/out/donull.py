from var import var


# create file null
def do():
    with open(var.PATH["out.null"], "tw", encoding="utf-8") as file:
        file.write("\n")
