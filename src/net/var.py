VAR = {
    "path": {
        "src": "src/net/",
        "var": "var/net/",
        "var.base": "var/base.yml",
        "var.list": "var/net/list.yml",
        "var.pattern": "var/pattern.yml",
        "var.filter": "var/filter/",
        "out": "out/net/",
    },
    # path to output scripts by target
    "script": {
        # flag path [args]
        # g means run code, r means download remote, a means copy raw
        "quantumult": [
            "g quantumult/Profile.conf",
            "g quantumult/filter.txt",
            "r quantumult/parser.js https://raw.githubusercontent.com/KOP-XIAO/QuantumultX/master/Scripts/resource-parser.js",
        ],
        "clash": [
            "g clash/scv.ini",
            "g clash/scv.yml",
            "g clash/Stash.yml",
        ],
        "surge": [
            "g surge/Profile.conf",
            "g surge/Server.conf",
            "g surge/base.conf",
            "a other/scv.ini",
        ],
        "shadowrocket": [
            "g other/shadowrocket.conf",
        ],
        "loon": [
            "r other/loon-parser.js https://github.com/sub-store-org/Sub-Store/releases/latest/download/sub-store-parser.loon.min.js"
        ],
    },
}
