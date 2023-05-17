#! /usr/bin/env python

import sys, os

sys.path.insert(0, '../pywu/')

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

if __name__ == '__main__':
    # create a workunit file
    f = open('workunit_template.sah','w')
    # create coordinate_ins
    coordinate_ins = xml('coordinate_t', coordinate_t)
    data_desc['coords'] = [coordinate_ins , coordinate_ins]
    # create corr coeff
    az_corr_coeff_ins = xml_data('az_corr_coeff', az_corr_coeff)
    zen_corr_coeff_ins = xml_data('zen_corr_coeff', zen_corr_coeff)
    receiver_cfg['az_corr_coeff'] = az_corr_coeff_ins
    receiver_cfg['zen_corr_coeff_ins'] = zen_corr_coeff_ins
    # create chirp_parameter
    chirp_parameter_ins = xml('chirp_parameter_t', chirp_parameter)
    analysis_cfg['chirps'] = [chirp_parameter_ins, chirp_parameter_ins]
    # create workunit header
    workunit_header_ins = xml('workunit_header', workunit_header)
    workunit_grp['workunit_header'] = workunit_header_ins
    # create data
    data_ins = xml_data('data', data)
    workunit_grp['data'] = data_ins
    workunit_grp_ins = xml('workunit_grp', workunit_grp)
    workunit_grp_ins.print_xml(f)
    f.close()