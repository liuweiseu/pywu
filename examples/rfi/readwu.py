def xml2dict(x):
    d = {}
    for i in range(len(x)):
        if len(x[i]) == 0:
            try:
                d[x[i].tag] = float(x[i].text)
            except:
                d[x[i].tag] = x[i].text
        else:
            d[x[i].tag] = xml2dict(x[i])
    return d