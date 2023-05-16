#! /usr/bin/env python

import sys, os

sys.path.insert(0, './')

from workunit import xml
from workunit import tape_info
from workunit import data_desc
from workunit import coordinate_t
from workunit import group_info
from workunit import workunit_header

if __name__ == '__main__':
    f = open('test.sah','w')
    workunit_header_ins = xml('workunit_header', workunit_header)
    workunit_header_ins.print_xml(f)
    f.close()