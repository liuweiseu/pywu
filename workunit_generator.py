#! /usr/bin/env python

import sys, os

sys.path.insert(0, './pywu')

from data_parse import dfile
from workunit import xml, xml_data
from workunit import tape_info
from workunit import data_desc
from workunit import coordinate_t
from workunit import az_corr_coeff
from workunit import zen_corr_coeff
from workunit import receiver_cfg
from workunit import recorder_cfg
from workunit import splitter_cfg
from workunit import chirp_parameter
from workunit import analysis_cfg
from workunit import subband_desc
from workunit import group_info
from workunit import workunit_header
from workunit import data
from workunit import workunit_grp

def main():
    f = open('test.sah','w')
    workunit_grp_ins = xml('workunit_group', workunit_grp)
    workunit_grp_ins.print_xml(f)
    f.close()

if __name__ == '__main__':
    main()