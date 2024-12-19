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
#  @brief : CTestsymbol for testing XmlMapWriter
#            provides the same minimal interface MapReader.Symbol.CSymbol
#            for above purpose
#=============================================================================


class CTestsymbol(object):
    def __init__(self,name='',address=1,size=1,gapsize=1,local=False,lsym=False,isec='',osec='',module='',lib='',mName='',mType='',sType=''):
        self.name = name
        self.address = address
        self.size = size
        self.gapsize = gapsize
        self.local = local
        self.lsym = lsym
        self.isec = isec
        self.osec = osec
        self.module = module
        self.lib = lib
        self.mName = mName
        self.mType = mType
        self.sType = sType
        

    def getName(self):
        return self.name

    def p_local(self):
        return self.local

    def getAddress(self):
        return self.address
        

    def getSize(self):
        return self.size

    def getGapSize(self):
        return self.gapsize

    def p_linkerSymbol(self):
        return self.lsym

    def getModule(self):
        return self.module

    def getLibrary(self):
        return self.lib

    def getOuputSectionName(self):
        return self.osec

    def getInputSectionName(self):
         return self.isec

    def getMemName(self):
        return self.mName

    def getMemType(self):
        return self.mType

    def getSectionType(self):
        return self.sType
