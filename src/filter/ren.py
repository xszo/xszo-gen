from pathlib import Path

PATH_TMP = Path("tmp/filter/")
PATH_VAR = Path("var/filter/")
PATH_VAR_LIST = Path("var/filter/list.yml")
PATH_OUT_CLASH = Path("out/clash/")
PATH_OUT_SURGE = Path("out/surge/")

REX_COM = "^\\s*($|#|\\/\\/|!)"

# getvlc.py
VLC_EXT = "https://github.com/v2fly/domain-list-community"
VLC_TMP = Path("tmp/filter/vlc/")
VLC_VAR = Path("tmp/filter/vlc/data/")
VLC_REX_INCL = ["^include:([A-Za-z0-9\\-\\!]+)\\s*(?:#.*)?$", "\\1"]
VLC_REX = [
    [
        "^full:((?:[A-Za-z0-9\\*](?:[A-Za-z0-9\\-\\*]*[A-Za-z0-9\\*])?\\.)*(?:[A-Za-z]+|xn--[A-Za-z0-9]+))(?:$|\\s)",
        "\\1",
    ],
    [
        "^(?:domain:)?((?:[A-Za-z0-9\\*](?:[A-Za-z0-9\\-\\*]*[A-Za-z0-9\\*])?\\.)*(?:[A-Za-z]+|xn--[A-Za-z0-9]+))(?:$|\\s)",
        ".\\1",
    ],
]
