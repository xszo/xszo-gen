from ren import Var


# create file null
def do():
    with open(Var.PATH["out.null"], "tw", encoding="utf-8") as file:
        file.write("\n")
