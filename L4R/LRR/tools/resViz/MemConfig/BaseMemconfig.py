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
#  @brief : description of physical controller memory is an set of
#           named 'typed' addressranges (start address,size), the '__shared'
#               attribute describes an additional address range giving access 
#               to the same physical memory
#           This description also provides the function that evaluates the use 
#           of memory blocks by linker sections of an application.
#           In main memory types and linker section names are evaluated to 
#           determine linker section types. __namedDataSections / __namedTextSections allows to define
#           allow to define resp sections explicitly
#=============================================================================


class CMemConfigError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message

class CMemRange:
    validTtypes = ['RAM','FLASH']
    def __init__(self,name,type,startAddr,size=-1,sharedBy=None):
        self.__name = name
        self.__startAddress = startAddr
        self.__size = size
        type = type.upper()
        if not type in CMemRange.validTtypes:
            raise CMemConfigError('CMemRange(): invalid memtype {0} at address {1} must be in {2}'.format(type,startAddr,CMemRange.validTtypes))
        self.__type = type
        self.__sharedBy = sharedBy
        
    def getType(self):
        return self.__type

    def getName(self):
        return self.__name

    def getStartAddress(self):
        return self.__startAddress

    def getSize(self):
        return self.__size

    def getSharedBy(self):
        return self.__sharedBy


    def __str__(self):
        sInfo = '__NONE__'
        if not self.__sharedBy is None:
            sInfo = hex(self.__sharedBy)
        return '{0} .. {1} - N: {2} T: {3} SH: {4}'.format(hex(self.__startAddress),hex(self.__startAddress + self.__size),self.__name,self.__type,sInfo)



class CBaseMemconfig(object):
    __validSectionTypes = ['text','data','bss']
    def __init__(self):
        self.__memRangeByAddr = dict()
        self.__memRangeIndex = None
        self.__LinkerSectionType = {}

    def parse(self):
        pass

    def createIndex(self):
        self.__memRangeIndex = [ x for x in self.__memRangeByAddr.keys()]
        self.__memRangeIndex.sort()

    def getMemRangeAdresses(self):
        if not bool(self.__memRangeIndex) or len(self.__memRangeIndex) != len(self.__memRangeByAddr.keys()):
            self.createIndex()
        return self.__memRangeIndex

#    def getMemRangeList(self):
#        return self.__memRangeByAddr.values()

    def dump(self):
        for mr in self.getMemRangeList():
            print('{0}'.format(str(mr)))
        if len(self.__LinkerSectionType) > 0:
            for sName in self.__LinkerSectionType.keys():
                print('SECTION: {0} TYPE: {1}'.format(sName,self.__LinkerSectionType[sName]))
    
    def addMemRange(self,memrange,key=-1):
        if key < 0:
            key = memrange.getStartAddress()
        if key in self.__memRangeByAddr:
            raise CMemConfigError('addMemRange: duplicate address {0} in MemConfig'.format(hex(address)))
        else:
            self.__memRangeByAddr[key] = memrange


    def addTypedSection(self,sectionName,type='data'):
        if not type in self.__validSectionTypes:
            raise CMemConfigError('addTypedSection: invalid section type "{0}" for section "{1}" - expected one of {2}'.format(
                        type,
                        sectionName,
                        self.__validSectionTypes
                    )
                )
        if sectionName in self.__LinkerSectionType:
            if type != self.__LinkerSectionType[sectionName]:
                raise CMemConfigError('addTypedSection: section type for section "{0}" already set to "{1}" differing from current type "{2}"'.format(
                            sectionName,self.__LinkerSectionType[sectionName],type
                        )
                    )
        else:
            self.__LinkerSectionType[sectionName] = type

    def nn_getMemStartAddr(self,address):
        result = -1
        factor = 1
        taddr = address
        while taddr >= 0:
            if taddr in self.__memRangeByAddr:
                result = taddr
                break
            elif taddr > 0:
                taddr = int(taddr/16)
                factor *= 16
            else:
                taddr = -1
        if result >= 0:
            result *= factor
        return result
        
    def getMemStartAddr(self,address):
        return self.__getMemRangeAddress(address)

    def __getMemRangeAddress(self,address):
        import sys
        indexList = self.getMemRangeAdresses()
        #print(indexList)
        lastIndex = -1;
        for index in indexList:
            #print('__getMemRangeAddress  trying {0} ---> {1}'.format(hex(address),hex(lastIndex)))
            if index > address:
                break
            lastIndex = index
        if lastIndex > 0: 
            mrSize = self.__memRangeByAddr[lastIndex].getSize()
            if (lastIndex <= address) and ((lastIndex + mrSize) > address):
                pass
            else:
                lastIndex = -1
        #print('__getMemRangeAddress {0} ---> {1}'.format(hex(address),hex(lastIndex)))
        return lastIndex

    def nn__getMemRangeAddress(self,address):
        result = -1
        taddr = address
        while taddr >= 0:
            if taddr in self.__memRangeByAddr:
                result = taddr
                break
            elif taddr > 0:
                taddr = int(taddr/16)
            else:
                taddr = -1
        return result

    def getMemRangeId(self,address):
        return self.__getMemRangeAddress(address)

    def p_allocatedAddress(self,address):
        return self.__getMemRangeAddress(address) >= 0

    def getMemRangeById(self,id):
        return self.__memRangeByAddr[id]

    def getMemRange(self,address):
        mr_address = self.__getMemRangeAddress(address)
        if mr_address < 0:
            self.dump()
            raise CMemConfigError('getMemRange: no memrange defined for addr {0}'.format(hex(address)))
        return self.__memRangeByAddr[mr_address]

    def getMemName(self,address):
        mr = self.getMemRange(address)
        return mr.getName()
        
    def getMemType(self,address):
        mr = self.getMemRange(address)
        return mr.getType()

    def p_SectionInNamedDataSections(self,sectionName):
        return sectionName in self.__namedDataSections

    def getSectionType(self,address,sectionName):
        if sectionName in self.__LinkerSectionType:
            result = self.__LinkerSectionType[sectionName]
        elif self.getMemType(address) == 'RAM':
            result = 'bss'
            if sectionName.lower().endswith('.data') or sectionName.lower().endswith('.default_data'):
                result = 'data'
            elif sectionName.lower().endswith('.text'):
                result = 'text'
        else:
            result = 'text'
        return result
    
    def getMemRangeList(self):
        return [ self.__memRangeByAddr[x] for x in self.getMemRangeAdresses() ]

if __name__ == "__main__":
    print('JUPP')
    mcfg =  CBaseMemconfig()
    try:
        mcfg.addMemRange(CMemRange('JUPP','ROM',int('0x10000',16),int('0x10000',16),None))
        mcfg.addMemRange(CMemRange('JUPP1','FLASH',int('0x40000',16),int('0x10000',16),None))
    except Exception as e:
        print('EXCEPTION while adding MemRange ... {0}'.format(e))
        pass
    try:
        mcfg.addTypedSection('.juhu','data')
        mcfg.addTypedSection('.crammens','bss')
        mcfg.addTypedSection('.code','text')
        mcfg.addTypedSection('.rodata','rodata')
    except Exception as e:
        print('EXCEPTION while adding TypedSection ... {0}'.format(e))
        pass
    mcfg.dump()

