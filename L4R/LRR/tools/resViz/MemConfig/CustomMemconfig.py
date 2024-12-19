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
#  @brief : read memconfig from json cfg file:
#    
#{
#  "MemRanges": 
#  [
#     {
#       "StartAddress":"0x80000000",
#       "Name":"PFI0",
#       "Type":"FLASH",
#       "Size":"0x3000000"
#     }
#  ],
#  "DataSections": 
#  [
#     {
#       "Name":"crammens"
#     }
#  ]
#}
#
#           
#           provide section type (text,data,bss) for address and (output) section name
#  @state : waiting for cleanup 
#=============================================================================
from BaseMemconfig import CBaseMemconfig,CMemRange,CMemConfigError 

import json

class CMemConfig(CBaseMemconfig):

    def __init__(self,cfgFile):
        super().__init__()
        self.__cfgFile = cfgFile
        # self.__memRangeByAddr = dict()
        # self.__memRangeIndex = None
        # self.__namedDataSections = []
    
    
    
    def parse(self):
        with open(self.__cfgFile , 'r') as f:
            data = f.read()
        json_data = json.loads(data)
        for mcfg in json_data['MemRanges']:
            name = mcfg['Name']
            type = mcfg['Type'].upper()
            if mcfg['StartAddress'].upper().startswith('0X'):
                startAddress = int(mcfg['StartAddress'],16)
            else:
                startAddress = int(mcfg['StartAddress'])
            if mcfg['Size'].upper().startswith('0X'):
                size = int(mcfg['Size'],16)
            else:
                size = int(mcfg['Size'])
            if not type in CMemRange.validTtypes:
                raise CMemConfigError('CustomMemconfig.parse: invalid memtype "{0}"'.format(type))
            if size <= 0:
                raise CMemConfigError('CustomMemconfig.parse: size "{0}" : size must be > 0 '.format(size))
            self.addMemRange(CMemRange(name,type,startAddress,size))
        for dataSection in json_data['DataSections']:
            dname = dataSection['Name']
            self.addDataSection(dname)

    def addDataSection(self,sectionName):
        super().addDataSection(sectionName)
            
    def addMemRange(self,memrange):
        address = memrange.getStartAddress()
        lastAddress = address + memrange.getSize() - 1
        conflict = False
        for erange in super().getMemRangeList():
            e_start_addr = erange.getStartAddress()
            e_end_addr = e_start_addr + erange.getSize()
            if e_end_addr > address and lastAddress >= e_start_addr:
                raise CMemConfigError('addMemRange: memrange overlap detected while adding memrange \n\t{0}'.format(str(memrange)))
        super().addMemRange(memrange)

    def getMemRangeList(self):
        return super.getMemRangeList()

    def __getMemRangeAddress(self,address):
        index = self.getMemRangeAdresses()
        last = -1
        for curr in index:
            if curr > address:
                break
            last = curr
        if last >= 0:
            if last + super().getMemRangeById(last).getSize() <= address:
                last = -1
        return last
    
    def dump(self):
        super().dump()
        
    def p_allocatedAddress(self,address):
        return self.__getMemRangeAddress(address) >= 0

    def getMemRangeById(self,id):
        return super().getMemRangeById(id)

    def getMemStartAddr(self,address):
        return self.__getMemRangeAddress(address)

    def getMemRange(self,address):
        id = self.__getMemRangeAddress(address)
        if id < 0:
            raise CMemConfigError('getMemRange: no memrange defined for addr {0}'.format(address))
        return super().getMemRangeById(id)

    def getMemName(self,address):
        return self.getMemRange(address).getName()

    def getMemType(self,address):
        return self.getMemRange(address).getType()

    def p_SectionInNamedDataSections(self,sectionName):
        return super().p_SectionInNamedDataSections(sectionName)

    def getSectionType(self,address,sectionName):
        result = 'text'
        if self.p_SectionInNamedDataSections(sectionName):
            result = 'data'
        elif self.getMemType(address) == 'RAM':
            result = 'bss'
            pos = sectionName.lower().find('data')
            if pos >= 0:
                result = 'data'
        return result


    def createIndex(self):
        super().createIndex()
        
    def getMemRangeAdresses(self):
        return super().getMemRangeAdresses()


if __name__ == "__main__":
    print('JUPP')
    import os
    mcfg =  CMemConfig(os.path.join(os.path.dirname(__file__),'tc_default_mcfg.json'))
    mcfg.parse()
    mcfg.dump()
    # i = 0
    # for addr in mcfg.getMemRangeAdresses():
        # i += 1
        # fulladdr = int(((hex(addr)[2:] + '00000000')[:8]),16)
        # mname = mcfg.getMemName(fulladdr)
        # mtype = mcfg.getMemType(fulladdr)
        # sname = ['holla.bss','crammes', 'seppel' ]
        # stype = mcfg.getSectionType(fulladdr,sname[i%3])
        # print('{0} --> {1} ({2}) {3} {4} {5}'.format(hex(addr),fulladdr,hex(fulladdr),mname,mtype,stype)) 
