"""
Note:   1. The wu_xml is based on a dict structure.
        2. The dict can be nested, which means a dict can be a part of another big dict.
        3. If you want a list of dict to be a part of another big dict, 
           you have to use util.add_to_list() to create the list
"""
import numpy as np
import struct
from .wu_dict import *

ENCODING = 'utf-8'
"""
class: xml_base
"""
class xml_base(object):
    """
    Description:
        The class prints out dict in xml format.
        It's a standard format.
    """
    # global variable for indent
    nindent = 0
    def __init__(self, info=workunit_grp):
        """
        Description:
            Create a xml_base object based on tag and info.
        Inputs:
            - tag(str): tag of the xml structure.
                Default='workunit_group'
            - info(dict): xml content in dict structure.
                Default=workunit_grp
        """
        self.f = 0
        self.tag = info['tag']
        self.info = info
        
    def print_xml_begin(self,tag):
        """
        Description:
            Print the beginning tag(<tag>).
        Input:
            - tag(str): tag.
                Default=None
        """
        self.print_xml_indent()
        s = bytes("<%s>\n"%(tag),ENCODING)
        self.f.write(s)

    def print_xml_end(self,tag):
        """
        Description:
            Print the end tag(</tag>).
        Input:
            - tag(str): tag.
                Default=None
        """
        self.print_xml_indent()
        s = bytes("</%s>\n"%(tag), ENCODING)
        self.f.write(s)
    
    def print_xml_content(self, c):
        """
        Description:
            Print the content of xml, which is in dict format.
        Input:
            c(dict): xml content in dict format.
                Default=None
        """
        for k in c:
            if(k == 'class' or k == 'tag'):
                continue
            v = c[k]
            if(isinstance(v,np.ndarray)):
                self.print_xml_begin(k)
                for i in v:
                    ins = eval(i['class'])(i)
                    ins.print_xml(self.f)
                self.print_xml_end(k)
            elif(isinstance(v,dict)):
                ins = eval(v['class'])(v)
                ins.print_xml(self.f)
            else:
                if(v!=''):
                    self.print_xml_indent()
                    s = bytes("<%s>%s</%s>\n"%(k, v, k), ENCODING)
                    self.f.write(s)
                    #print(s, file=self.f)

    def print_xml_indent(self):
        """
        Description:
            Print indent.
        """
        s = bytes("%s"%(' '*xml_base.nindent),ENCODING)
        self.f.write(s)

    def print_xml(self,f):
        """
        Description:
            Print xml to a file.
        Input:
            f(file pointer): It points to the file we want to write xml to.
                Default=None
        """
        self.f = f
        self.print_xml_begin(self.tag)
        xml_base.nindent += 2
        self.print_xml_content(self.info)
        xml_base.nindent -= 2
        self.print_xml_end(self.tag)


class xml_coeff(xml_base):
    """
    Description:
        xml_coeff is inherited from xml_base, which is used fro print coeff.
        The reason is that  coeff's format is a bit different.
    """
    def __init__(self, info):
        """
        Description:
            Create a xml_coeff object.
        Inputs:
            - info(dict): xml content in dict structure.
                Default=workunit_grp
        """
        super(xml_coeff, self).__init__(info)

    def print_xml_begin(self, tag):
        """
        Description:
            It's an overloaded method for xml_coeff format.
            The tag format is like:
                <coeff length=2097152 encoding="setiathome">
                    xxxx
                <\coeff>
        Input:
            - tag(str): tag.
                Default=None
        """
        self.print_xml_indent()
        s = bytes("<%s"%(tag), ENCODING)
        self.f.write(s)
        for k in self.info:
            if(k == 'class' or k == 'tag' or k == 'values'):
                continue
            v = self.info[k]
            s = bytes(" %s=%s"%(k,v), ENCODING)
            self.f.write(s)
        s = bytes(">\n", ENCODING)
        self.f.write(s)

    def print_xml_content(self, c):
        """
        Description:
            It's an overloaded method for xml_coeff format.
            The content format is like this:
                <coeff ...>
                    1,2,3,4
                </coeff>
        Input:
            - c(dict): xml content in dict format.
                Default=None 
        """
        self.print_xml_indent()
        for v in c['values'][:-1]:
            s = bytes("%s,"%(v), ENCODING)
            self.f.write(s)
        s = bytes(c['values'][-1], ENCODING)
        self.f.write(s)
        self.f.write('\n')

class xml_data(xml_coeff):
    """
    Description:
        xml_data is inherited from xml_coeff, which is used for print data.
        data is in binary format.
    """
    def __init__(self, info):
        """
        Description:
            Create a xml_data format.
        Input:
            - tag(str): tag.
                Default=None
            - info(dict): xml content in dict format.
                Default=None
        """
        super(xml_data, self).__init__(info)
    
    def print_xml_content(self, c):
        """
        Description:
             It's an overloaded method for xml_data format.
             data is in binary format.
        """
        #self.print_xml_indent()
        if(not isinstance(c['values'], np.ndarray)):
            c['values'] = np.array(c['values'], dtype=np.int16)
        l = len(c['values'])
        # TODO: double check if it's little endian or big endian here
        for v in c['values']:
            self.f.write(v)
        s = bytes('  \n', ENCODING)
        self.f.write(s)
