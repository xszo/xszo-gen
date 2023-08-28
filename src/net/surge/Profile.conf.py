def o(line=""):
    out.write(line + "\n")


o("[General]")
o("#!include " + src["id"] + "base.conf")
o()
o("[Proxy]")
o("#!include node.conf")
o()
o("[Proxy Group]")
o("#!include " + src["id"] + "base.conf")
o()
o("[Rule]")
o("#!include " + src["id"] + "base.conf")
