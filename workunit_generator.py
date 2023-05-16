import sys, os

sys.path.insert(0, './')

from workunit import xml
from workunit import tape_info
from workunit import data_desc
from workunit import coordinate_t

if __name__ == '__main__':
    f = open('test.sah','w')
    
    tape_info_ins = xml('tape_info',tape_info)
    tape_info_ins.print_xml(f)
    data_desc_ins = xml('data_desc', data_desc)
    data_desc_ins.print_xml(f)

    f.close()