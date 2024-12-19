#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
#  @copyright (c) 2019 - 2021 by Robert Bosch GmbH. All rights reserved.
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
#  @brief : parse GHS linker script - here restricted to get output section
#           'loaded' into some other address using 
#           GHS linker ROM|CROM|ROM_NOCOPY directive
#=============================================================================


import re
import sys, os

class GHS_LDReaderError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return 'GHS_LDReader - ' + self.message

class CSectionCopy(object):
    def __init__(self,orig,copy,compressed=False):
        self.__section = orig
        self.__sectionCopy = copy
        self.__compressed = compressed
    def getSection(self):
        return self.__section

    def getSectionCopy(self):
        return self.__sectionCopy

    def p_compressed(self):
        return self.__compressed

    def __str__(self):
        return 'SECTION: {0} COPIED: {1} (compressed: {2})'.format(self.__section,self.__sectionCopy,self.__compressed)
    

class GHS_LDReader(object):
    def __init__(self,filename):
        self.__ldfile = filename
        self.__sectionCopyMap = {}
        self.__verbose = 0
        self.__verbose_functions = {}

    def getVerbosityLevel(self):
        level = self.__verbose
        caller = sys._getframe().f_back.f_code.co_name
        if caller in self.__verbose_functions:
            level = self.__verbose_functions[caller]
        return level

    def p_verbose(self,mode=0):
        level = self.__verbose
        caller = sys._getframe().f_back.f_code.co_name
        if caller in self.__verbose_functions:
            level = self.__verbose_functions[caller]
        return level > mode

    def p_extraVerbose(self):
        return self.__verbose > 1
        
    def readFile(self):
        result = None
        if os.path.isfile(self.__ldfile):
            result = []
            try:
                infile = open(self.__ldfile,'r')
                for line in infile:
                    line = line.rstrip(' \r\n').strip()
                    if bool(line) and not line.startswith('#'):
                        result.append(line)
                infile.close()
            except Exception as e:
                raise GHS_LDReaderError('ERROR reading file {0} - {1}'.format(self.__ldfile,e))
        else:
            raise GHS_LDReaderError('ERROR no such file "{0}"'.format(self.__ldfile)) 
        return result

    def parse(self,lines=None):
        fc = lines
        if fc is None:
            fc = self.readFile()
        # pattern to find rom copy sections
        rcPattern = re.compile(r'\b(\S+)\s+(ROM|CROM|ROM_NOCOPY)\s*\(\s*([^\(\)\s]+)\s*\)')
        for line in fc:
            rcDef = rcPattern.findall(line)
            if rcDef:
                for match in rcDef:
                    orig = match[2]
                    self.__sectionCopyMap[match[2]] = CSectionCopy(match[2],match[0],match[1] == 'CROM')

    def add(self,orig,copy,compressed=False):
        self.__sectionCopyMap[orig] = CSectionCopy(orig,copy,compressed)

    def getSectionMap(self):
        return self.__sectionCopyMap

    def dump(self):
        print('############# LDFile: {0}'.format(self.__ldfile))
        print('ROM LOADED sections') 
        n=0
        for section in self.__sectionCopyMap.keys():
            n+=1
            print('[{0}]\t{1}'.format(n, self.__sectionCopyMap[section]))
            
if __name__ == "__main__":
    ldreader = GHS_LDReader(sys.argv[1])
    ldreader.parse()
    sm = ldreader.getSectionMap()
    print('SectionMap {0} entries'.format(len(sm.keys())))
    ldreader.dump()