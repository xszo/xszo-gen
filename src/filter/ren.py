class Var:
    EXT = {"vlc": "https://github.com/v2fly/domain-list-community"}
    REX = {
        "comment": "^\\s*($|#|\\/\\/|!)",
        "incl": ["^include:([A-Za-z0-9\\-\\!]+)\\s*(?:#.*)?$", "\\1"],
        "dn": [
            "^full:((?:[A-Za-z0-9\\*](?:[A-Za-z0-9\\-\\*]*[A-Za-z0-9\\*])?\\.)*(?:[A-Za-z]+|xn--[A-Za-z0-9]+))(?:$|\\s)",
            "\\1",
        ],
        "ds": [
            "^(?:domain:)?((?:[A-Za-z0-9\\*](?:[A-Za-z0-9\\-\\*]*[A-Za-z0-9\\*])?\\.)*(?:[A-Za-z]+|xn--[A-Za-z0-9]+))(?:$|\\s)",
            "+.\\1",
        ],
    }
    PATH = {
        "tmp": "tmp/filter/",
        "tmp.vlc": "tmp/filter/vlc/",
        "var": "var/filter/",
        "var.list": "var/filter/list.yml",
        "var.vlc": "tmp/filter/vlc/data/",
        "out.clash": "out/clash/f-",
        "out.surge": "out/surge/f-",
    }
