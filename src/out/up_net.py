from subprocess import run


def do():
    run(["rm", "-rf", "out/net"], check=True)
    run(["mkdir", "out/net"], check=False)
    run(["cp", "-r", "out/clash", "out/net/clash"], check=True)
    run(["cp", "-r", "out/surge", "out/net/surge"], check=True)
    run(["cp", "-r", "out/network", "out/net/other"], check=True)
    run(["mkdir", "out/net/quantumult"], check=False)
    run(
        ["mv", "out/net/other/quantumult.conf", "out/net/quantumult/Profile.conf"],
        check=True,
    )
    run(
        [
            "mv",
            "out/net/other/quantumult-filter.txt",
            "out/net/quantumult/filter.txt",
        ],
        check=True,
    )
    run(
        [
            "mv",
            "out/net/other/quantumult-parser.js",
            "out/net/quantumult/parser.js",
        ],
        check=True,
    )
