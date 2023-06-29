def o(line=""):
    out.write(line + "\n")


for item in src["filter"]["domain"]:
    match item[0]:
        case 1:
            o("host-suffix," + item[1] + "," + item[2])
        case 2:
            o("host," + item[1] + "," + item[2])
for item in src["filter"]["ipcidr"]:
    match item[0]:
        case 1:
            o("ip-cidr," + item[1] + "," + item[2])
        case 2:
            o("ip6-cidr," + item[1] + "," + item[2])
for item in src["filter"]["ipgeo"]:
    match item[0]:
        case 1:
            o("geoip," + item[1] + "," + item[2])
