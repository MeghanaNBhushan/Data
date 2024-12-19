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
#  @brief : TriCore Memory description - hard coded address ranges taken from 
#           Hardware documentation 
#           - still open to have project specific memory configuration
#           check to be a valid address
#           provide memory type (RAM / FLASH) and name (from HW docu) for address
#           provide section type (text,data,bss) for address and (output) section name
#  @state : waiting for cleanup 
#=============================================================================
from BaseMemconfig import CBaseMemconfig,CMemRange,CMemConfigError 

class CMemConfig(CBaseMemconfig):
    tc_default_memory = {
            int('7',16) :       ('CPU0_DataSratchPad','RAM',int('0x3C000',16),None),
            int('7003C',16) :   ('CPU0_DataCache', 'RAM',int('0x4000',16),None),
            int('700C',16) :    ('CPU0_DataCacheTag', 'RAM',int('0x1800',16),None),
            int('701',16):      ('CPU0_PrgSratchPad', 'RAM',int('0x10000',16),None),
            int('7011',16) :    ('CPU0_PrgCache', 'RAM',int('0x8000',16),None),
            int('701C',16) :    ('CPU0_PrgCacheTag', 'RAM',int('0x3000',16),None),

            int('6',16) :       ('CPU1_DataSratchPad', 'RAM',int('0x3C000',16),None),
            int('6003C',16) :   ('CPU1_DataCache', 'RAM',int('0x4000',16),None),
            int('600C',16) :    ('CPU1_DataCacheTag', 'RAM',int('0x1800',16),None),
            int('601',16):      ('CPU1_PrgSratchPad', 'RAM',int('0x10000',16),None),
            int('6011',16) :    ('CPU1_PrgCache', 'RAM',int('0x8000',16),None),
            int('601C',16) :    ('CPU1_PrgCacheTag', 'RAM',int('0x3000',16),None),

            int('5',16) :       ('CPU2_DataSratchPad', 'RAM',int('0x18000',16),None),
            int('50018',16) :   ('CPU2_DataCache', 'RAM',int('0x4000',16),None),
            int('500C',16) :    ('CPU2_DataCacheTag', 'RAM',int('0x1800',16),None),
            int('501',16):      ('CPU2_PrgSratchPad', 'RAM',int('0x10000',16),None),
            int('5011',16) :    ('CPU2_PrgCache', 'RAM',int('0x8000',16),None),
            int('501C',16) :    ('CPU2_PrgCacheTag', 'RAM',int('0x3000',16),None),

            int('4',16) :       ('CPU3_DataSratchPad', 'RAM',int('0x18000',16),None),
            int('40018',16) :   ('CPU3_DataCache', 'RAM',int('0x4000',16),None),
            int('400C',16) :    ('CPU3_DataCacheTag', 'RAM',int('0x1800',16),None),
            int('401',16):      ('CPU3_PrgSratchPad', 'RAM',int('0x10000',16),None),
            int('4011',16) :    ('CPU3_PrgCache', 'RAM',int('0x8000',16),None),
            int('401C',16) :    ('CPU3_PrgCacheTag', 'RAM',int('0x3000',16),None),

            int('3',16) :       ('CPU4_DataSratchPad', 'RAM',int('0x18000',16),None),
            int('30018',16) :   ('CPU4_DataCache', 'RAM',int('0x4000',16),None),
            int('300C',16) :    ('CPU4_DataCacheTag', 'RAM',int('0x1800',16),None),
            int('301',16):      ('CPU4_PrgSratchPad', 'RAM',int('0x10000',16),None),
            int('3011',16) :    ('CPU4_PrgCache', 'RAM',int('0x8000',16),None),
            int('301C',16) :    ('CPU4_PrgCacheTag', 'RAM',int('0x3000',16),None),

            int('1',16) :       ('CPU5_DataSratchPad', 'RAM',int('0x18000',16),None),
            int('10018',16) :   ('CPU5_DataCache', 'RAM',int('0x4000',16),None),
            int('100C',16) :    ('CPU5_DataCacheTag', 'RAM',int('0x1800',16),None),
            int('101',16):      ('CPU5_PrgSratchPad', 'RAM',int('0x10000',16),None),
            int('1011',16) :    ('CPU5_PrgCache', 'RAM',int('0x8000',16),None),
            int('101C',16) :    ('CPU5_PrgCacheTag', 'RAM',int('0x3000',16),None),

            int('8',16):        ('PFI0', 'FLASH',int('0x300000',16),None),
            int('803',16):      ('PFI1', 'FLASH',int('0x300000',16),None),
            int('806',16):      ('PFI2', 'FLASH',int('0x300000',16),None),
            int('809',16):      ('PFI3', 'FLASH',int('0x300000',16),None),
            int('80C',16):      ('PFI4', 'FLASH',int('0x300000',16),None),
            int('80F',16):      ('PFI5', 'FLASH',int('0x100000',16),None),

            int('A',16):        ('PFI0_NC', 'FLASH',int('0x300000',16),int('8',16)),
            int('A03',16):      ('PFI1_NC', 'FLASH',int('0x300000',16),int('803',16)),
            int('A06',16):      ('PFI2_NC', 'FLASH',int('0x300000',16),int('806',16)),
            int('A09',16):      ('PFI3_NC', 'FLASH',int('0x300000',16),int('809',16)),
            int('A0C',16):      ('PFI4_NC', 'FLASH',int('0x300000',16),int('80C',16)),
            int('A0F',16):      ('PFI5_NC', 'FLASH',int('0x100000',16),int('80F',16)),

            int('9',16):        ('CPU0_DLMU_RAM', 'RAM',int('0x10000',16),None),
            int('9001',16):     ('CPU1_DLMU_RAM', 'RAM',int('0x10000',16),None),
            int('9002',16):     ('CPU2_DLMU_RAM', 'RAM',int('0x10000',16),None),
            int('9003',16):     ('CPU3_DLMU_RAM', 'RAM',int('0x10000',16),None),
            int('9004',16):     ('LMU0_RAM', 'RAM',int('0x40000',16),None),
            int('9008',16):     ('LMU1_RAM', 'RAM',int('0x40000',16),None),
            int('900C',16):     ('LMU2_RAM', 'RAM',int('0x40000',16),None),
            int('901',16):      ('CPU4_DLMU_RAM', 'RAM',int('0x10000',16),None),
            int('9011',16):     ('CPU5_DLMU_RAM', 'RAM',int('0x10000',16),None),
            int('904',16):      ('DAM0', 'RAM',int('0x10000',16),None),
            int('9041',16):     ('DAM1', 'RAM',int('0x10000',16),None),
            int('99',16):       ('EMEM0', 'RAM',int('0x100000',16),None),
            int('991',16):      ('EMEM1', 'RAM',int('0x100000',16),None),
            int('992',16):      ('EMEM2', 'RAM',int('0x100000',16),None),
            int('993',16):      ('EMEM3', 'RAM',int('0x100000',16),None),
            int('B',16):        ('CPU0_DLMU_RAM_NC', 'RAM',int('0x10000',16),int('9',16)),
            int('B001',16):     ('CPU1_DLMU_RAM_NC', 'RAM',int('0x10000',16),int('9001',16)),
            int('B002',16):     ('CPU2_DLMU_RAM_NC', 'RAM',int('0x10000',16),int('9002',16)),
            int('B003',16):     ('CPU3_DLMU_RAM_NC', 'RAM',int('0x10000',16),int('9003',16)),
            int('B004',16):     ('LMU0_RAM_NC', 'RAM',int('0x40000',16),int('9004',16)),
            int('B008',16):     ('LMU1_RAM_NC', 'RAM',int('0x40000',16),int('9008',16)),
            int('B00C',16):     ('LMU2_RAM_NC', 'RAM',int('0x40000',16),int('900C',16)),
            int('B01',16):      ('CPU4_DLMU_RAM_NC', 'RAM',int('0x10000',16),int('901',16)),
            int('B011',16):     ('CPU5_DLMU_RAM_NC', 'RAM',int('0x10000',16),int('9011',16)),
            int('B04',16):      ('DAM0_NC', 'RAM',int('0x10000',16),int('904',16)),
            int('B041',16):     ('DAM1_NC', 'RAM',int('0x10000',16),int('9041',16)),
            int('B9',16):       ('EMEM0_NC', 'RAM',int('0x100000',16),int('990',16)),
            int('B91',16):      ('EMEM1_NC', 'RAM',int('0x100000',16),int('991',16)),
            int('B92',16):      ('EMEM2_NC', 'RAM',int('0x100000',16),int('992',16)),
            int('B93',16):      ('EMEM3_NC', 'RAM',int('0x100000',16),int('993',16))
        }
    
    tc_layouts = {
            'TC_DEFAULT' : tc_default_memory
        }
        
    def __init__(self,controller='TC_DEFAULT'):
        super().__init__()
        self.__controller = controller
    def getAddrFromAddrKey(self,key):
        result = key
        if not key is None:
            result =  int(((hex(key)[2:] + '00000000')[:8]),16)
        return result
        
    def parse(self):
        tc_memory = None
        if self.__controller in CMemConfig.tc_layouts:
            tc_memory = CMemConfig.tc_layouts[self.__controller]
        else:
            raise CMemConfigError('unsupported controller {0}'.format(self.__controller))
        for addr in tc_memory.keys():
            #fulladdr = int(((hex(addr)[2:] + '00000000')[:8]),16)
            fulladdr = self.getAddrFromAddrKey(addr)
            #super().addMemRange(CMemRange(tc_memory[addr][0],tc_memory[addr][1],fulladdr,tc_memory[addr][2]),addr)
            super().addMemRange(CMemRange(tc_memory[addr][0],tc_memory[addr][1],fulladdr,tc_memory[addr][2],self.getAddrFromAddrKey(tc_memory[addr][3])),fulladdr)
        
    def dump(self):
        super().dump()
        
    def p_allocatedAddress(self,address):
        return super().p_allocatedAddress(address)

    def getMemStartAddr(self,address):
        return super().getMemStartAddr(address)

    def getMemRange(self,address):
        return super().getMemRange(address)

    def getMemName(self,address):
        return super().getMemName(address)

    def getMemType(self,address):
        return super().getMemType(address)

        
    def getSectionType(self,address,sectionName):
        return super().getSectionType(address,sectionName)

    def createIndex(self):
        super().createIndex()
        
    def getMemRangeAdresses(self):
        return super().getMemRangeAdresses()

    def addDataSection(self,sectionName):
        super().addDataSection(sectionName)
        
    def getMemRangeList(self):
        tempi = [ x.getStartAddress() for x in super().getMemRangeList() ]
        tempi.sort()
        return [ self.getMemRange(ad) for ad in tempi ] 

    def dump1(self):
        for mr in self.getMemRangeList():
            print('#A#\n\t"Name" : "{0}",\n\t"Address" : "{1}",\n\t"Size" : "{2}",\n\t"Type":"{3}"\n#B#'.format(
                        mr.getName(),
                        hex(mr.getStartAddress()),
                        hex(mr.getSize()),
                        mr.getType()
                    )
                )

if __name__ == "__main__":
    print('JUPP')
    mcfg =  CMemConfig()
    mcfg.parse()
    mcfg.dump()
    #mcfg.dump1()
    # i = 0
    # for addr in mcfg.getMemRangeAdresses():
        # i += 1
        # fulladdr = int(((hex(addr)[2:] + '00000000')[:8]),16)
        # mname = mcfg.getMemName(fulladdr)
        # mtype = mcfg.getMemType(fulladdr)
        # sname = ['holla.bss','crammes.data', 'data.nase' ]
        # stype = mcfg.getSectionType(fulladdr,sname[i%3])
        # print('{0} --> {1} ({2}) {3} {4} {5}'.format(hex(addr),fulladdr,hex(fulladdr),mname,mtype,stype)) 
        
