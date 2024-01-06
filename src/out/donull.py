from ren import Var


class Do:
    # create file null
    def do(self):
        with open(Var.PATH["out.null"], "tw", encoding="utf-8") as file:
            file.write("\n")
