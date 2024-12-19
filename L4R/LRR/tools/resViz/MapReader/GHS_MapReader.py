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
#  @brief : parse GHS mapfile to create a list of symbols 
#           and its relevant attributes for memory consumption anylysis
#           used memconfig
#  @state : waiting for cleanup 
#=============================================================================


import sys
from GHS_FileReader import FileReader
from LoSection import LoSection, CLoSectionMap
from LiSection import LiSection, CLiSectionMap,LiSectionIndex
from Symbol import symbolCreator,CSymbolMap
from MemConfig import MemConfig
class GHS_MapReaderError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message
        
class GHS_MapReader(object):
    def __init__(self,filename,memCfg,demangler=None):
        self.__mapfile = FileReader(filename)
        self.__memCfg = memCfg
        self.__demangler = demangler
        self.__loadMap = {}
        self.__losections = None
        self.__lisections = None
        self.__symbols = None
        self.__localSymbols = None
        self.__globalSymbols = None
        self.__verbose = 0
        self.__mapfileType = -1
        self.__verbose_functions = {
                'imageSummaryReader':0,
                'moduleSummaryReader':0,
                'globalSymolsReader':0,
                'localSymolsReader':0,
                'symbolsReader':0,
                'generateMap1SymbolList': 0,
                'addSymbolGaps':0,
                'parse': 0,
                'generateSymbolNamespace':0
            }
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

    def p_validMapFile(self):
        eloadMap = ['imageSummaryReader','moduleSummaryReader']
        if self.__mapfileType == 1:
            eloadMap.extend(['globalSymolsReader', 'localSymolsReader'])
        elif self.__mapfileType == 2:
            eloadMap.extend(['symbolsReader'])
        else:
            raise GHS_MapReaderError('GHS_MapReader: invalid map file type {0} in file {1}'.format(str(self.__mapfileType),self.__mapfile.getFilename()))
        for mapfilesection in eloadMap:
            if not mapfilesection in self.__loadMap:
                raise GHS_MapReaderError('GHS_MapReader: missing mapfile section {0} in file {1}'.format(mapfilesection,self.__mapfile.getFilename()))
        return True

    def parse(self):
        #print('JUPP .... {0}'.format(self.__mapfile.getFilename()))
        verbose_level = self.getVerbosityLevel()
        while not self.__mapfile.p_eof():
            sectionHeader = self.__mapfile.nextLine()
            sectionHandler = self.getSectionHandler(sectionHeader)
            if bool(sectionHandler):
                sectionHandler()
            else:
                raise GHS_MapReaderError('GHS_MapReader: unknown section found {0} in file {1} line {2}'.format(sectionHeader,self.__mapfile.getFilename(),str(self.__mapfile.currentLineNumber())))
        if self.p_validMapFile():
            if self.__mapfileType == 1:
                #self.updateGlobalSymbols()
                self.generateMap1SymbolList()
            self.addSymbolGaps()
            if bool(self.__demangler):
                self.generateSymbolNamespace()
            if (verbose_level & 2) > 1:
                print('####################### SYMBOLS START')
                self.__symbols.dump()
                print('####################### SYMBOLS END')
                print('####################### OSectionSummary')
                self.createOSectionSummary()
                print('####################### ObejctListSummary')
                self.createSymbolSummary()
            if (verbose_level & 4) > 1:
                sys.exit(0)

    def generateSymbolNamespace(self):
        verbose_level = self.getVerbosityLevel()
        for sym in self.getSymbolList():
            if not sym.p_linkerSymbol():
                name = sym.getName()
                namespace = ''
                decodedName = self.__demangler.decodeName(name)
                if decodedName != name:
                    namespace = self.__demangler.getNamespace(decodedName)
                    sym.setDecodedName(decodedName)
                else:
                    namespace = self.__demangler.getNamespace(name)
                if bool(namespace):
                    sym.setNamespace(namespace)
                if (verbose_level & 2) > 0:
                    #print('{3} SYM: {0} DECO: {1} NS: {2}'.format(name,decodedName,namespace,hex(sym.getAddress())[2:]))
                    if namespace is None:
                        namespace = ''
                    if decodedName is None:
                        decodedName = ''
                    print('{0} NS: {1} NAME: {2} DNAME: {3}'.format(hex(sym.getAddress())[2:],namespace,name,decodedName))
                    #print('### {0} --> {1}'.format(hex(sym.getAddress()),namespace))
        if (verbose_level & 4) > 1:
            sys.exit(0)

    def getSymbolList(self):
        result = []
        if bool(self.__symbols):
            result = self.__symbols.getSymbolList()
        return result
    def getDeletedSymbols(self):
        ds = None
        if not self.__globalSymbols is None:
            ds =  self.__globalSymbols.getDeletedSymbols()
        else:
            ds = self.__symbols.getDeletedSymbols()
        return ds

    def getOSectionList(self):
        return self.__losections.getSectionList()
    
    def getOSectionByName(self,name):
        return self.__losections.getSectionByName(name)

    def getMemCfg(self):
        return self.__memCfg
        
    def getPhysMemName(self,addr):
        self.__memCfg.getMemName(addr)
        
    def updateRomCopySections(self,romCopyMap=None):
        if romCopyMap:
            for oSection in self.getOSectionList():
                oSectionName = oSection.getName()
                if oSectionName in romCopyMap:
                    oSection.setRomCopySection(self.getOSectionByName(romCopyMap[oSectionName].getSectionCopy()),True)
        else:
            defSectionPrefix = 'rbLinker_'
            ramSectionNames = []
            flashSectionNames = []
            for oSection in self.getOSectionList():
                if oSection.getMemType() == 'RAM': 
                    if oSection.getSectionType() in ['text','data']:
                        ramSectionNames.append(oSection.getName())
                else :
                    flashSectionNames.append(oSection.getName())
            for rsn in ramSectionNames:
                rsSuffix = rsn
                if rsSuffix.startswith(defSectionPrefix):
                    rsSuffix = rsSuffix[len(defSectionPrefix):]
                for fsn in flashSectionNames:
                    if fsn.endswith(rsSuffix):
                        ramSection = self.getOSectionByName(rsn)
                        flashSection = self.getOSectionByName(fsn)
                        if ramSection.getSize() == flashSection.getSize():
                            ramSection.setRomCopySection(flashSection)
                            break

    def getSectionHandler(self,sectionLine):
        sectionHandler = None
        if self.p_verbose():
            print('getSectionHandler({0})'.format(sectionLine))
        if sectionLine == 'Image Summary':
            sectionHandler = self.imageSummaryReader
        elif sectionLine == 'Module Summary':
            sectionHandler = self.moduleSummaryReader
        elif sectionLine == 'Global Symbols (sorted numerically)':
            sectionHandler = self.globalSymolsReader
        elif sectionLine == 'Local Symbols (sorted numerically)':
            sectionHandler = self.localSymolsReader
        elif sectionLine == 'Global Cross Reference':
            sectionHandler = self.globalCrossRefReader
        elif sectionLine == 'Symbols (sorted numerically)':
            sectionHandler = self.symbolsReader
        return sectionHandler


    
    def markSectionAsParsed(self,sectionname):
        caller = sys._getframe().f_back.f_code.co_name
        if caller in self.__loadMap:
            raise GHS_MapReaderError('duplicate section {0} in file {1}'.format(caller,self.__mapfile.getFilename()))
        else:
            self.__loadMap[caller] = 1
        if caller == 'symbolsReader':
            if self.__mapfileType > 0:
                 raise GHS_MapReaderError('GHS_MapReader: invalid Mapfile {0} unexpected section {1} found mapfile type {2}'.format(
                                self.__mapfile.getFilename(),
                                caller,
                                str(self.__mapfileType))
                    )
            else:
                self.__mapfileType = 2
        elif caller in ['globalSymolsReader', 'localSymolsReader']:
            if self.__mapfileType > 1:
                 raise GHS_MapReaderError('GHS_MapReader: invalid Mapfile {0} unexpected section {1} found mapfile type {2}'.format(
                                self.__mapfile.getFilename(),
                                caller,
                                str(self.__mapfileType))
                    )
            else:
                self.__mapfileType = 1

    def imageSummaryReader(self):
        verbose_level = self.getVerbosityLevel()
        verbose_mode = (verbose_level & 1) > 0
        self.markSectionAsParsed('imageSummary')
        sm = CLoSectionMap()
        self.__losections = sm
        line = self.__mapfile.nextLine()
        while bool(line):
            if verbose_mode:
                print('imageSummaryReader {0}'.format(line))
            losection = LoSection(line,self.__memCfg,verbose_mode,self.__mapfile)
            if bool(losection):
                if verbose_mode:
                    print('{0}'.format(str(losection)))
                sm.addLoSection(losection)
            line = self.__mapfile.nextLine()
        sm.createIndex()
        #self.updateRomCopySections()
        if (verbose_level & 2) > 0 :
           sm.dump()
        if (verbose_level & 4) > 0:
            sys.exit(0)

    def moduleSummaryReader(self):
        verbose_level = self.getVerbosityLevel()
        verbose_mode = (verbose_level & 1) > 0
        self.markSectionAsParsed('moduleSummary')
        sm = CLiSectionMap()
        self.__lisections = sm
        line = self.__mapfile.nextLine()
        while bool(line):
            if verbose_mode:
                print('moduleSummaryReader {0}'.format(line))
            lisection = LiSection(line,self.__losections,verbose_mode,self.__mapfile)
            if bool(lisection):
                if verbose_mode:
                    print('{0}'.format(lisection))
                sm.addLiSection(lisection)
            line = self.__mapfile.nextLine()
        sm.createIndex()
        if (verbose_level & 2) > 0:
           sm.dump()
        if (verbose_level & 4) > 0:
            sys.exit(0)

    def globalSymolsReader(self):
        verbose_level = self.getVerbosityLevel()
        verbose_mode = (verbose_level & 1) > 0
        self.markSectionAsParsed('globalSymols')
        sm  = CSymbolMap('globalSymols')
        self.__globalSymbols = sm
        sectionIndex = LiSectionIndex()
        line = self.__mapfile.nextLine()
        while bool(line):
            if verbose_mode:
                print('globalSymolsReader {0}'.format(line))
            sym = symbolCreator(line,'global',self.__lisections,sectionIndex,self.__losections,verbose_mode,self.__mapfile)
            if sym:
                sm.addSymbol(sym)
                if verbose_mode:
                    print("G {0}".format(str(sym)))
            line = self.__mapfile.nextLine()
        sm.createIndex()   
        if (verbose_level & 2) > 0:
           sm.dump()
        if (verbose_level & 4) > 0:
            sys.exit(0)
        
    def localSymolsReader(self):
        verbose_level = self.getVerbosityLevel()
        verbose_mode = (verbose_level & 1) > 0
        self.markSectionAsParsed('localSymols')
        sm  = CSymbolMap('localSymols')
        self.__localSymbols = sm
        sectionIndex = LiSectionIndex()
        line = self.__mapfile.nextLine()
        while bool(line):
            if verbose_mode:
                print('localSymolsReader {0}'.format(line))
            sym = symbolCreator(line,'local',self.__lisections,sectionIndex,self.__losections,verbose_mode,self.__mapfile)
            if sym:
                sm.addSymbol(sym)
                if verbose_mode:
                    print("L {0}".format(str(sym)))
            line = self.__mapfile.nextLine()
        sm.createIndex()   
        if (verbose_level & 2) > 0:
           sm.dump()
        if (verbose_level & 4) > 0:
            sys.exit(0)

    def symbolsReader(self):
        verbose_level = self.getVerbosityLevel()
        verbose_mode = (verbose_level & 1) > 0
        self.markSectionAsParsed('symbols')
        sm  = CSymbolMap('symbols')
        self.__symbols = sm
        sectionIndex = LiSectionIndex()
        line = self.__mapfile.nextLine()
        while bool(line):
            if verbose_mode:
                print('symbolsReader {0}'.format(line))
            sym = symbolCreator(line,'m2',self.__lisections,sectionIndex,self.__losections,verbose_mode,self.__mapfile)
            if sym:
                if verbose_mode:
                   print("M2 {0}".format(str(sym)))
                sm.addSymbol(sym)
            line = self.__mapfile.nextLine()
        sm.createIndex()   
        if (verbose_level & 2) > 0:
           sm.dump()
        if (verbose_level & 4) > 0:
            sys.exit(0)


    def globalCrossRefReader(self):
        sectionKey = 'globalCrossRef'
        self.markSectionAsParsed('globalCrossRef')
        line = self.__mapfile.nextLine()
        while bool(line):
            #print('globalCrossRefReader {0}'.format(line))
            line = self.__mapfile.nextLine()
           
################################################################
    
    def generateMap1SymbolList(self):
        verbose_level = self.getVerbosityLevel()
        index = 0
        sm  = CSymbolMap()
        self.__symbols = sm
        globalSymbolIndex = self.__globalSymbols.getIndex()
        for addr in globalSymbolIndex:
            gsym = self.__globalSymbols.getSymbol(addr)
            lsym = self.__localSymbols.getExistentSymbol(addr)
            sm.addSymbol(gsym)
            if bool(lsym):
                if gsym.getSize() != 0:
                    gsym.updateFromLocalSymbol(lsym)
                else:
                    sm.addSymbol(lsym)
        localSymbolIndex = self.__localSymbols.getIndex()
        for addr in localSymbolIndex:
            lsym = self.__localSymbols.getSymbol(addr)
            gsym = self.__globalSymbols.getExistentSymbol(addr)
            if not gsym:
                sm.addSymbol(lsym)
        sm.createIndex()
        if (verbose_level & 2) > 0:
           sm.dump()
        if (verbose_level & 4) > 0:
            sys.exit(0)

    def updateGlobalSymbols(self):
        index = 0
        gIndex = self.__globalSymbols.getIndex()
        for addr in gIndex:
            sym = self.__globalSymbols.getSymbol(addr)
            if self.p_extraVerbose():
                print('updateGlobalSymbols: {0}'.format(str(sym)))
            if self.p_allocatedAddr(addr):
                if sym.p_linked(): 
                    index,lisection = self.__lisections.findLiSection(index,addr)
                    if self.p_extraVerbose():
                        print('updateGlobalSymbols: {0} index {1} found {2}'.format(hex(addr), index,str(lisection)))
                    if lisection:
                        #print('KKKKKKKKK found isection {0}'.format(str(lisection)))
                        isection,module,lib,source,osection = lisection.getISectionData()
                        #print('lllll found isection {0}, {1}, {2}, {3}, {4}'.format(isection,lib,module,source,osection))
                        #sym.updateSoureData(isection,module,lib,source,osection)
                        sym.setInputSection(lisection,self.p_MapFileType1())
                    else:
                        print('HHHHHHHHHHHHHHHHHHHHH missing isection {0} for symbol {1}'.format(index,str(sym)))
                        sym.setInputSection(None)
                else:
                    if self.p_verbose():
                        print('symbol not in linked {0}'.format(str(sym)))
            else:
                if self.p_verbose():
                    print('symbol not in valid addr range {0}'.format(str(sym)))
            if self.p_extraVerbose():
                print('updateGlobalSymbols: done {0}'.format(str(sym)))


            
    def createOSectionSummary(self):
        mn_result =  {}
        mn_unallocated = {}
        st_result =  {}
        mt_result =  {}
        print('###########  OutputsectionSectionSummary')
        for addr in self.__losections.getIndex():
            osect = self.__losections.getSectionByAddr(addr)
            sectionType = osect.getSectionType()
            memType = osect.getMemType()
            memName = osect.getMemName()
            osize = osect.getSize()
            if not memName in mn_result:
                mn_result[memName] = 0
                mn_unallocated[memName] = 0
            if not sectionType in st_result:
                st_result[sectionType] = 0
            if not memType in mt_result:
                mt_result[memType] = 0
            if osect.p_used():
                mn_result[memName] += osize
                st_result[sectionType] += osize
                mt_result[memType] += osize
            else:
                mn_unallocated[memName] += osize
        print('##### OSECSUMMARY: MTYPE')
        for mmm in mt_result:
            print('{0} : {1}'.format(mmm,mt_result[mmm]))
        print('##### OSECSUMMARY: MNAME')
        for mmm in mn_result:
            print('{0} : {1} ({2})'.format(mmm,mn_result[mmm],mn_result[mmm] + mn_unallocated[mmm] ))
        print('##### OSECSUMMARY: STYPE')
        for mmm in st_result:
            print('{0} : {1}'.format(mmm,st_result[mmm]))
        print('##### OSECSUMMARY: OSECT')
        for addr in self.__losections.getIndex():
            osect = self.__losections.getSectionByAddr(addr)
            print('{0} : {1} {2}'.format(osect.getName(),osect.getSize(),osect.getAllocatedSize()))

            
    def createSymbolSummary(self):
        mn_result =  {}
        st_result =  {}
        mt_result =  {}
        os_result =  {}
        for addr in self.__losections.getIndex():
            osect = self.__losections.getSectionByAddr(addr)
            os_result[osect.getName()] = 0
        gIndex = self.__symbols.getIndex()
        # mdict = dict()
        for addr in gIndex:
            symbol = self.__symbols.getSymbol(addr)
            #print('{0} -- {1} -- {2} -- {3}'.format(hex(addr),section,memRange,sectionType))
            symSize = symbol.getSize('ALL')
            # gsize = symbol.getGapSize()
            # if symbol.getMemName() == 'CPU0_DLMU_RAM_NC':
                # mn = symbol.getModule()
                # osn = symbol.getOutputSectionName()
                # nisn = False
                # if not mn in mdict:
                    # mdict[mn] = 1
                    # nisn = True
                # print('JJJJJJJJJJ({0}) {1} {2} {3} {4}'.format(str(nisn),osn,symbol.getName(),symSize,gsize))
            if symSize > 0:
                sectionType = symbol.getSectionType()
                memType = symbol.getMemType()
                memName = symbol.getMemName()
                oSectName = symbol.getOutputSectionName()
                if not memName in mn_result:
                    mn_result[memName] = 0
                if not sectionType in st_result:
                    st_result[sectionType] = 0
                if not memType in mt_result:
                    mt_result[memType] = 0
                if not oSectName in os_result:
                    os_result[oSectName] = 0
                mn_result[memName] += symSize
                st_result[sectionType] += symSize
                mt_result[memType] += symSize
                os_result[oSectName] += symSize
        print('###########  SYMBOLSUMMARY')
        print('##### SYMBOLSUMMARY: MTYPE')
        for mmm in mt_result:
            print('{0} : {1}'.format(mmm,mt_result[mmm]))
        print('##### SYMBOLSUMMARY: MNAME')
        for mmm in mn_result:
            print('{0} : {1}'.format(mmm,mn_result[mmm]))
        print('##### SYMBOLSUMMARY: STYPE')
        for mmm in st_result:
            print('{0} : {1}'.format(mmm,st_result[mmm]))
        print('##### SYMBOLSUMMARY: OSECT')
        for addr in self.__losections.getIndex():
            osect = self.__losections.getSectionByAddr(addr)
            mmm = osect.getName()
            print('{0} : {1} {2}'.format(mmm,osect.getSize(),os_result[mmm]))

    def addSymbolGaps(self):
        sIndex = self.__symbols.getIndex()
        lastSym = None
        currSym = None
        for addr in sIndex:
            currSym = self.__symbols.getSymbol(addr)
            gapSize = 0
            if lastSym:
                gapSize = lastSym.addSymbolGaps(currSym,self.p_verbose())
            if gapSize >= 0:
                lastSym = currSym
        if currSym:
            lastSym.addSymbolGaps(None,self.p_verbose())
