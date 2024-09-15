from pathlib import Path

from ..ren import PATH_OUT, PATH_TMP_FILTER, PATH_VAR_FILTER, URI

NAME_SURGE = "surge"
NAME_CLASH = "clash"

PATH_TMP = PATH_TMP_FILTER
PATH_TMP_REF = PATH_TMP / "ref.yml"
PATH_VAR = PATH_VAR_FILTER
PATH_VAR_LIST = PATH_VAR / "list.yml"
PATH_OUT_SURGE = PATH_OUT / NAME_SURGE
PATH_OUT_CLASH = PATH_OUT / NAME_CLASH

LEVEL_DN = range(1, 5)
REX_COM = "^\\s*($|#|//|!)"

# getvlc.py
VLC_EXT = "https://github.com/v2fly/domain-list-community"
VLC_TMP = Path("tmp/filter/vlc/")
VLC_VAR = Path("tmp/filter/vlc/data/")
VLC_REX_INCL = ["^include:([A-Za-z0-9\\-\\!]+)\\s*(?:#.*)?$", "\\1"]
VLC_REX = [
    [
        "^full:((?:[a-z0-9\\*](?:[a-z0-9\\-\\*]*[a-z0-9\\*])?\\.)*(?:[a-z]+|xn--[a-z0-9]+))(?:$|\\s)",
        "\\1",
    ],
    [
        "^(?:domain:)?((?:[a-z0-9\\*](?:[a-z0-9\\-\\*]*[a-z0-9\\*])?\\.)*(?:[a-z]+|xn--[a-z0-9]+))(?:$|\\s)",
        ".\\1",
    ],
]
