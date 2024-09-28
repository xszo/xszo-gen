from .. import ren as __ren

NAME_SURGE = "surge"
NAME_CLASH = "clash"

PATH_TMP = __ren.PATH_TMP_FILTER
PATH_VAR = __ren.PATH_VAR_FILTER
PATH_VAR_LIST = PATH_VAR / "list.yml"
PATH_OUT_SURGE = __ren.PATH_OUT / NAME_SURGE
PATH_OUT_CLASH = __ren.PATH_OUT / NAME_CLASH

# getvlc.py
VLC_URI = "https://github.com/v2fly/domain-list-community"
VLC_REPO = PATH_TMP / "vlc"
VLC_DATA = PATH_TMP / "vlc" / "data"

# remix.py
LEVEL_DN = range(1, 5)
