from shutil import copyfile, copytree

from . import ren


def copy() -> None:
    # copy raw dir
    copytree(ren.RAW_PATH, ren.PATH_OUT, dirs_exist_ok=True)
    # copy raw list
    for item in ren.RAW_FILE:
        copyfile(item, ren.PATH_OUT / item)

    # copy custom file
    if ren.PATH_OUT_VAR.is_dir():
        copytree(ren.PATH_OUT_VAR, ren.PATH_OUT, dirs_exist_ok=True)
