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
#  @brief : read xml to create a list of symbols 
#           and its relevant attributes for memory consumption anylysis
#  @state : waiting for cleanup 
#=============================================================================


import sys
import xml.etree.ElementTree as ET

from Symbol import CSymbol,CSymbolMap
from LoSection import CLoSection,CLoSectionMap

class CXmlMapReaderError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message

class CMemory(object):
    def __init__(self,*data,**namedData):
        pass
    
    
class CMemConfig(object):
    def __init__(self):
        pass
    def addMemory(self,memory):
        pass

class CMapFile(object):
    def __init__(self,name):
        self.__name = name
        self.__memcfg = None
        self.__losections = None
        self.__symbols = None
        self.__mapfileType = -1

    def init(self,metadata):
        if '__mapfiletype' in metadata:
            self.__mapfileType = int(metadata['__mapfiletype'])
        else:
            self.__mapfileType = 1
        if '__memory' in metadata and metadata['__memory'].lower() in ['true','yes','1']:
            self.__memcfg = CMemConfig()
        if '__sections' in metadata and metadata['__sections'].lower() in ['true','yes','1']:
            self.__losections = CLoSectionMap()
        self.__symbols = CSymbolMap()
    
    def p_haveSection(self):
        return not self.__losections is None
    def p_haveMemconfig(self):
        return not self.__memcfg is None

    def finit(self):
        pass

    def addLoSection(self,section):
        self.__losections.addLoSection(section)

    def addSymbol(self,symbol):
        if self.__symbols == None:
            self.__symbols = CLoSectionMap()
        self.__symbols.addSymbol(symbol)

    def getOutputSectionByName(self,name):
        return self.__losections.getOutputSectionByName(name)

    def getName(self):
        return self.__name

    def parse(self,xmapfile):
        if self.p_haveMemconfig():
            pass
        if self.p_haveSection():
            pass
        xsymbollist = xmapfile.findall('./symbollist/symbol')
        if xsymbollist is None:
            raise CXmlMapReaderError('no symbols found in mapfile "{0}"'.format(self.__name))
        for xsymbol in xsymbollist:
            self.parseSymbol(xsymbol)

    def parseSymbol(self,xsymbol):
        for xattr in xsymbol.attrib.keys():
            print('... {0} {1}'.format(xattr,xsymbol.attrib[xattr]))
        for xchild in xsymbol:
            print(' ------ {0}'.format(xchild.tag))


#CSymbol(name,address,size,local,inputSection,inputSectionName,outputSection,outputSectionName,source,linkerSymbol,notlinked)
#CLoSection(name,address,size,memName,memStartAddress,memType,sectionType)

class CXmlMapReader(object):
    def __init__(self,compiler,filename):
        self.__compiler = compiler
        self.__filename = filename
        self.__mapFile = dict()
        self.__state = ''
        self.__verbose = 0
        self.__verbose_functions = {
            }

    def addMapFile(self,mapfile):
        mname = mapfile.getName()
        if mname in self.__mapFile:
            raise CXmlMapReaderError('when adding mapfile data "{0}" name must be uniq in file "{1}"'.format(name,self.__filename))
        self.__mapFile[mname] = mapfile

    def getVerbosityLevel(self):
        level = self.__verbose
        caller = sys._getframe().f_back.f_code.co_name
        if caller in self.__verbose_functions:
            level = self.__verbose_functions[caller]
        return level

    def p_terminateAtEOF(self):
        return (self.getVerbosityLevel() & 4)>0

    def p_verbose(self,mode=0):
        level = self.__verbose
        caller = sys._getframe().f_back.f_code.co_name
        if caller in self.__verbose_functions:
            level = self.__verbose_functions[caller]
        return level > mode

    def p_extraVerbose(self):
        return self.__verbose > 1
        

    def p_MapFileType1(self):
        return self.__mapfileType == 1

    def getMapFileType(self):
        return self.__mapfileType

    def parse(self):
        if self.__state == 'parsed':
            raise CXmlMapReaderError('file {0} already read - nothing to be done')
        else: 
            xmlData = ET.parse(self.__filename)
            root = xmlData.getroot()
            mapfiles = root.findall('./mapfile_data')
            if mapfiles is None:
                raise CXmlMapReaderError('no mapfile data found in "{0}"'.format(self.__filename))
            for xmapFile in mapfiles:
                for xattr in xmapFile.attrib.keys():
                    print('... {0} {1}'.format(xattr,xmapFile.attrib[xattr]))
                mapfile = CMapFile(xmapFile.attrib['mapfilenname'])
                mapfile.init(xmapFile.attrib)
                mapfile.parse(xmapFile)
                self.addMapFile(mapfile)
#        <decodedname name="Dc::Sit::BsImba::s_intersectionDxToleranceRelationObj2Polyline" />
#        <namespace name="Dc::Sit::BsImba" />
#        <allocation address="0x60033828" gap_size="0x0" size="0x4" />
#        <section_data input_section=".bss" library="libdc_fw_sit_lib.a" module="sit_behaviorStrategyImba.o" output_section="rbLinker_dsram1.bss" sectionType="bss" />
#        <memrange name="CPU1_DataSratchPad" type="RAM" />
                
                
    # targetToolComponents = getToolComponents(root)
    # csettingsList = root.findall('./component_settings')
    # csettings = None
    # if csettingsList is None or len(csettingsList) < 1:
        # csettings = ET.SubElement(root,'component_settings')
    # else:
        # csettings = csettingsList[0]
    # for target in optionListByTarget.keys():
        # findPathAttribute = "[@target='" + target + "']"
        # inputList = csettings.findall('./input_to' +  findPathAttribute)
        # ipt = None
        # if inputList is None or len(inputList) < 1:
            # if targetToolComponents.has_key(target):
                # ipt = ET.SubElement(csettings,'input_to',targetToolComponents[target])
            # else:
                # raise QAFXmlError("updateAnalyzerFile - missing component definitions for target '" + target + "'")
        # else:
            # for ipt in inputList:
                # if ipt.attrib['component'] == 'qac' or ipt.attrib['component'] == 'qacpp':
                    # break
        # for option in optionListByTarget[target]:
            # ET.SubElement(ipt,'option',option)
    # if exludeFilter :
        # inputList = csettings.findall('./input_to')
        # ipt = None
        # if inputList is None or len(inputList) < 1:
            # pass
        # else:
            # for ipt in inputList:
                # if ipt.attrib['component'] in ['qac','qacpp','rcma','mcpp','m3cm']:
                    # for path in exludeFilter:
                        # ET.SubElement(ipt,'option',{'argument':path, 'name':"-quiet"})
    # if silentCHeader: 
        # inputList = csettings.findall('./input_to')
        # ipt = None
        # if inputList is None or len(inputList) < 1:
            # pass
        # else:
            # for ipt in inputList:
                # if ipt.attrib['component'] in ['qacpp']:
                    # for path in silentCHeader:
                        # ET.SubElement(ipt,'option',{'argument':path, 'name':"-quiet"})

if __name__ == "__main__":
    print('HOLLA {0} {1}'.format(len(sys.argv),sys.argv[1]))
    if len(sys.argv) > 1:
        huhu = CXmlMapReader('GHS',sys.argv[1])
        huhu.parse()
