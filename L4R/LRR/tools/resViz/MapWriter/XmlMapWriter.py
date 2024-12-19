#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
#  @copyright (c) 2019 - 2020 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
#=============================================================================
#  P R O J E C T   I N F O R M A T I O N
#-----------------------------------------------------------------------------
#  Projectname            : resViz (Mapfile based memory resource analysis)
#=============================================================================
#  F I L E   I N F O R M A T I O N
#-----------------------------------------------------------------------------
#  @brief         : Create xml representation of map file symbollist
#=============================================================================


import xml.etree.ElementTree as ET
import os
import time
import re

class XmlMapWriterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class MapWriter(object):
    xml_writer_version = '0.0.1'
    
    def __init__(self,filename):
        self.__filename = filename
        xml_document = ET.ElementTree()
        root = ET.Element('ecusymbols',{'xmlversion':"3.0.0", 'xml_writer_version':MapWriter.xml_writer_version, 'creation_date':time.ctime()})
        xml_document._setroot(root)
        self.__xml_document = xml_document

    # def dump(self):
        # if bool(self.__xml_document):
            # self.__xml_document.dump()
            
    def write(self):
        if not bool(self.__xml_document):
            raise XmlMapWriterError('no xml tree to be written')
        if not bool(self.__filename):
            raise XmlMapWriterError('missing filename')
        try:
            self.__xml_document.write(self.__filename,encoding="UTF-8")
        except :
            raise XmlMapWriterError('failed to write xml data to file "{0}"'.format(self.__filename))

    def addSectionList(self,x_mapfiledata,p_have_mem=False,osectionList=None):
        if bool(osectionList):
            x_osectionlist = ET.SubElement(x_mapfiledata,'osectionlist', {'nos':str(len(osectionList))} )
            for section in osectionList:
                s_attr = {
                        'name':section.getName(),
                        'address':hex(section.getAddress()),
                        'size':hex(section.getSize()),
                        'allocated_size':hex(section.getAllocatedSize()),
                        'allocations':str(section.getRefCount()),
                        'sectionType':section.getSectionType()
                    }
                if p_have_mem:
                    s_attr['memaddr'] = hex(section.getMemStartAddress())
                    x_osection = ET.SubElement(x_osectionlist,'osection',s_attr)
                else:
                    x_osection = ET.SubElement(x_osectionlist,'osection',s_attr)
                    x_memory = ET.SubElement(x_osection,'memory_data',{
                        'memName':section.getMemName(),
                        'memType':section.getMemType(),
                        'memaddr':hex(section.getMemStartAddress())
                    }
                )
            
    def addMemory(self,x_mapfiledata,memRangeList):
        if bool(memRangeList):
            x_memrangelist = ET.SubElement(x_mapfiledata,'memrangelist', {'nos':str(len(memRangeList))} )
            for mr in memRangeList:
                x_section = ET.SubElement(x_memrangelist,'memrange',{
                        'name':mr.getName(),
                        'type':mr.getType(),
                        'address':hex(mr.getStartAddress()),
                        'size':hex(mr.getSize())
                    }
                )

    def addMapfile(self,name,mapfileType,metadata,symbolList,sectionList=None,memRangeList=None): 
        for key in metadata.keys():
            if type(metadata[key]) != type(''):
                metadata[key] = str(metadata[key])
        if not name in metadata:
            metadata['name'] = name
        metadata['__mapfiletype']=str(mapfileType)
        metadata['__sections']=str(bool(sectionList))
        metadata['__memory']=str(bool(memRangeList))
        root = self.__xml_document.getroot()
        x_mapdata = ET.SubElement(root,'mapfile_data',metadata)
        self.addMemory(x_mapdata,memRangeList)
        # if bool(memRangeList):
            # x_memrangelist = ET.SubElement(x_mapdata,'memrangelist', {'nos':str(len(memRangeList))} )
            # for mr in memRangeList:
                # x_section = ET.SubElement(x_memrangelist,'memrange',{
                        # 'name':mr.getName(),
                        # 'type':mr.getType(),
                        # 'address':hex(mr.getStartAddress()),
                        # 'size':hex(mr.getSize())
                    # }
                # )
        self.addSectionList(x_mapdata,bool(memRangeList),sectionList)
        # if bool(sectionList):
            # x_sectionlist = ET.SubElement(x_mapdata,'sectionlist', {'nos':str(len(sectionList))} )
            # for section in sectionList:
                # x_section = ET.SubElement(x_sectionlist,'section',{
                        # 'name':section.getName(),
                        # 'address':hex(section.getAddress()),
                        # 'size':hex(section.getSize()),
                        # 'allocated_size':hex(section.getAllocatedSize()),
                        # 'allocations':str(section.getRefCount()),
                        # 'sectionType':section.getSectionType()
                    # }
                # )
                # x_memory = ET.SubElement(x_section,'memory_data',{
                        # 'memName':section.getMemName(),
                        # 'memType':section.getMemType()
                    # }
                # )
        self.addSymbolList(x_mapdata,bool(memRangeList),bool(sectionList),symbolList)
        indent(root)

    def addSymbolList(self,x_mapfiledata,p_have_mem=False,p_have_osection=False,symbolList=None):
        if bool(symbolList):
            x_symbollist = ET.SubElement(x_mapfiledata,'symbollist', {'nos':str(len(symbolList))} )
            for symbol in symbolList:
                globalSym = 'yes' 
                if symbol.p_local():
                    globalSym = 'no'
                x_symbol = ET.SubElement(x_symbollist,'symbol',{
                        'name':symbol.getName(),
                        'global':globalSym
                    }
                )
                decodedName = symbol.getDecodedName()
                if bool(decodedName):
                    x_ns = ET.SubElement(x_symbol,'decodedname',{
                            'name':decodedName
                        }
                    )
                namespace = symbol.getNamespace()
                if bool(namespace):
                    x_ns = ET.SubElement(x_symbol,'namespace',{
                            'name':namespace
                        }
                    )
                x_alloc = ET.SubElement(x_symbol,'allocation',{
                        'address':hex(symbol.getAddress()),
                        'size':hex(symbol.getSize()),
                        'gap_size':hex(symbol.getGapSize())
                    }
                )
                
                module = '__linker__'
                library = ''
                if not symbol.p_linkerSymbol():
                    module = symbol.getModule()
                    library = symbol.getLibrary()
                if not p_have_osection:
                    x_section = ET.SubElement(x_symbol,'section_data',  {
                            'input_section':symbol.getInputSectionName(),
                            'output_section':symbol.getOutputSectionName(),
                            'sectionType':symbol.getSectionType(),
                            'module':module,
                            'library':library
                        }
                    )
                    x_mem = ET.SubElement(x_section,'memrange',{
                            'name':symbol.getMemName(),
                            'type':symbol.getMemType(),
                            'maddr':hex(symbol.getMemStartAddress())
                        }
                    )
                else:
                    x_section = ET.SubElement(x_symbol,'section_data',  {
                            'input_section':symbol.getInputSectionName(),
                            'output_section':symbol.getOutputSectionName(),
                            'module':module,
                            'library':library
                        }
                    )
                
                # if not bool(memRangeList):
                    # x_mem = ET.SubElement(x_symbol,'memrange',{
                                # 'name':symbol.getMemName(),
                                # 'type':symbol.getMemType(),
                                # 'maddr':hex(-1)
                            # }
                    # )
                # else:


def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

if __name__ == "__main__":
    from testsymbol import CTestsymbol 
    testsymbolList = [
        CTestsymbol(name='sym1',address=1000,size=10,gapsize=3,local=False,lsym=False,isec='i1',osec='o1',module='m1',lib='l1',mName='nn',mType='ram',sType='data'),
        CTestsymbol(name='sym2',address=1500,size=20,gapsize=0,local=True,lsym=False,isec='i2',osec='o2',module='m2',lib='l2',mName='jj',mType='flash',sType='text'),
        CTestsymbol(name='sym3',address=2000,size=15,gapsize=0,local=False,lsym=True,isec='',osec='abb',module='',lib='',mName='m1',mType='flash',sType='text'),
        CTestsymbol(name='sym4',address=2000,size=0,gapsize=0,local=False,lsym=True,isec='',osec='',module='',lib='',mName='',mType='',sType='')
    ]
    xmf = XmlMapWriter('c:/temp/xmftest.xml',malsehn='test',version=3)
    xmf.createDocument(testsymbolList)
    xmf.write()
    