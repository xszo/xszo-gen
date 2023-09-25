def o(line=""):
    out.write(line + "\n")


o("[General]")
o("loglevel = warning")
o("external-controller-access = 0000000000000000@0.0.0.0:8420")
o("ipv6 = true")
o("ipv6-vif = auto")
o("udp-priority = true")
o("udp-policy-not-supported-behaviour = REJECT")
o("exclude-simple-hostnames = true")
if "dns" in src["meta"]:
    o("hijack-dns = *:53")
    line = "dns-server = "
    for item in src["meta"]["dns"]:
        line += item + ", "
    o(line[:-2])
if "doh" in src["meta"]:
    o("encrypted-dns-server = " + src["meta"]["doh"])
o("internet-test-url = " + src["meta"]["test"])
o("proxy-test-url = " + src["meta"]["test"])
o()
o("[Proxy]")
o("#!include proxy.conf")
o()
o("[Proxy Group]")
o("#!include " + src["id"] + "base.conf")
o()
o("[Rule]")
o("#!include " + src["id"] + "base.conf")
