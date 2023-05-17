#! /usr/bin/env python

import sys, os

sys.path.insert(0, '../pywu/')

from wu_xml  import xml, xml_data
from wu_xml  import tape_info
from wu_xml  import data_desc
from wu_xml  import coordinate_t
from wu_xml  import az_corr_coeff
from wu_xml  import zen_corr_coeff
from wu_xml  import receiver_cfg
from wu_xml  import recorder_cfg
from wu_xml  import splitter_cfg
from wu_xml  import chirp_parameter
from wu_xml  import analysis_cfg
from wu_xml  import subband_desc
from wu_xml  import group_info
from wu_xml  import workunit_header
from wu_xml  import data
from wu_xml  import workunit_grp

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