"""
Note:   1. The wu_xml is based on a dict structure.
        2. The dict can be nested, which means a dict can be a part of another big dict.
        3. If you want a list of dict to be a part of another big dict, 
           you have to use util/add_to_list() to create the list
"""
import numpy as np
import struct
from .wu_dict import *

"""
class: xml_base
"""
class xml_base(object):
    nindent = 0
    def __init__(self, name='workunit_group', info=workunit_grp):
        self.f = 0
        self.name = name
        self.info = info
        
    def print_xml_begin(self,name):
        self.print_xml_indent()
        print("<%s>"%(name),file=self.f)

    def print_xml_end(self,name):
        self.print_xml_indent()
        print("</%s>"%(name), file=self.f)
    
    def print_xml_content(self, c):
        for k in c:
            if(k == 'class'):
                continue
            v = c[k]
            if(isinstance(v,np.ndarray)):
                for i in v:
                    ins = eval(i['class'])(k,i)
                    ins.print_xml(self.f)
            elif(isinstance(v,dict)):
                ins = eval(v['class'])(k,v)
                ins.print_xml(self.f)
            else:
                self.print_xml_indent()
                print("<%s>%s</%s>"%(k, v, k), file=self.f)

    def print_xml_indent(self):
        print(' '*xml_base.nindent, file=self.f, end='')

    def print_xml(self,f):
        self.f = f
        self.print_xml_begin(self.name)
        xml_base.nindent += 2
        self.print_xml_content(self.info)
        xml_base.nindent -= 2
        self.print_xml_end(self.name)


class xml_coeff(xml_base):
    def __init__(self, name, info):
        super(xml_coeff, self).__init__(name, info)

    def print_xml_begin(self, name):
        self.print_xml_indent()
        print("<%s "%(name),file=self.f, end='')
        for k in self.info:
            if k == 'values':
                break
            v = self.info[k]
            print("%s=%s "%(k,v),file=self.f, end='')
        print(">", file=self.f)
    def print_xml_content(self, c):
        self.print_xml_indent()
        for v in c['values'][:-1]:
            print("%s,"%(v), file=self.f, end='')
        print(c['values'][-1], file=self.f)

class xml_data(xml_coeff):
    def __init__(self, name, info):
        super(xml_data, self).__init__(name, info)
    
    def print_xml_content(self, c):
        self.print_xml_indent()
        if(not isinstance(c['values'], np.ndarray)):
            c['values'] = np.array(c['values'], dtype=np.int16)
        l = len(c['values'])
        d = struct.pack('<%dH'%(l),*c['values'])
        for v in d:
            print("%c"%(v), file=self.f, end='')
        print('',file=self.f)
