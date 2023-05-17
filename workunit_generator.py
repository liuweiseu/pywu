#! /usr/bin/env python

import sys, os

sys.path.insert(0, './pywu')

from wu_io import dfile,redis_info
from wu_xml import xml, xml_data
from wu_xml import tape_info
from wu_xml import data_desc
from wu_xml import coordinate_t
from wu_xml import az_corr_coeff
from wu_xml import zen_corr_coeff
from wu_xml import receiver_cfg
from wu_xml import recorder_cfg
from wu_xml import splitter_cfg
from wu_xml import chirp_parameter
from wu_xml import analysis_cfg
from wu_xml import subband_desc
from wu_xml import group_info
from wu_xml import workunit_header
from wu_xml import data
from wu_xml import workunit_grp

def main():
    # open data file
    f = dfile('data_example/serendip6_m13_1.05G-1.45G_MB_01_00_20230511_165609_868843681_raw_2s.dat')
    # get metadata from redis_info.json
    r = redis_info('data_example/redis_info_20230511.json')
    coord = r.seekcood(0,f.info['timestamp'], 6)

    # create a wu_xml file
    f = open('workunit.sah','w')
    # create coordinate_ins
    data_desc['coords'] = []
    for md in coord:
        coordinate_ins = xml('coordinate_t', md)
        data_desc['coords'].append(coordinate_ins)
    # create wu_xml header
    workunit_header_ins = xml('workunit_header', workunit_header)
    workunit_grp['workunit_header'] = workunit_header_ins
    # create workunit
    workunit_grp_ins = xml('workunit_group', workunit_grp)
    workunit_grp_ins.print_xml(f)
    f.close()

if __name__ == '__main__':
    main()