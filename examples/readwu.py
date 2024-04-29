#! /usr/bin/env python3

import xml.etree.ElementTree as ET

def xml2dict(x):
    """
    Description:
        Convert xml to dict.
    Inputs:
        - x(xml.etree.ElementTree.Element): xml element
    Outputs:
        - d(dict): dict
    """
    d = {}
    for i in range(len(x)):
        if len(x[i]) == 0:
            try:
                d[x[i].tag] = float(x[i].text)
            except:
                d[x[i].tag] = x[i].text
        elif x[i].tag in d.keys():
            # if the key is already in the dict, 
            # convert it to list
            if type(d[x[i].tag]) == dict:
                d[x[i].tag]= [d[x[i].tag]]
            d[x[i].tag].append(xml2dict(x[i]))
        else:
            d[x[i].tag] = xml2dict(x[i])
    return d

def read_wu_header(fn):
    """
    Description:
        Generate workunit header.
    Inputs:
        - fn(str): workunit filename
    Outputs:
        - wuh(dict): workunit header
    """
    with open(fn, 'rb') as f:
        xmls = f.readlines()
    h = []
    for x in xmls:
        # skip the workunit tag
        if x == b'<workunit>\n':
            continue
        # if it's the end of workunit_header, exit
        elif x == b'  </workunit_header>\n' :
            h.append(x.decode('utf-8'))
            break
        else:
            h.append(x.decode('utf-8'))
    # convert list to string
    hstr = ''.join(h)
    # read xml
    r = ET.fromstring(hstr)
    # convert xml to dict
    wuh = {}
    wuh[r.tag] = xml2dict(r)
    return wuh

def _get_data_info(infostr):
    """
    Description:
        Get data info from infostr.
        The format has to be like '  <data length=61034 encoding="sun_binary">\n'
    Inputs:
        - infostr(str): info string
    Outputs:
        - info(dict): data info
    """
    info = {}
    s = infostr.split('=')
    info[s[0][3:]] = int(s[1].split(' ')[0])
    info[s[1].split(' ')[1]] = s[2][:-2]
    return info

def read_wu_data(fn):
    """
    Description:
        Generate workunit data.
    Inputs:
        - fn(str): workunit filename
    Outputs:
        - info(dict): data info
        - d(bytes): data
    """
    with open('workunit_example.sah', 'rb') as f:
        xmls = f.readlines()
    d = b''
    dflag = 0
    for x in xmls:
        # try to decode the byte to string
        try:
            xstr = x.decode('utf-8')
        except:
            pass
        # if it's the end of data, set dflag to 0
        if xstr.startswith('  </data>') and dflag == 1:
            dflag = 0
        # if it's the data, add it to d
        if dflag == 1:
            d = d + x
        # if it's the start of data, set dflag to 1
        if xstr.startswith('  <data length') and dflag == 0:
            dflag = 1
            info = _get_data_info(xstr)
    # Verify the length of data
    if len(d) != info['data length']:
        print('Error: length of data is not correct!')
    # throw away the last '\n' in data
    return info, d[:-1]

# This is for test
if __name__ == '__main__':
    wuh = read_wu_header('workunit_example.sah')
    print(wuh)
    info, wud = read_wu_data('workunit_example.sah')
    print(info)
    print('length of data:', len(wud))  