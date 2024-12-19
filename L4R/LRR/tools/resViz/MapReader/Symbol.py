# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  @copyright (c) 2019 - 2020 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
# =============================================================================
#  P R O J E C T   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  Projectname            : resViz (Mapfile based memory resource analysis)
# =============================================================================
#  F I L E   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  @brief : parse GHS symbol lines - Global,Local, (mapfile_type2-) Symbols sections
#           and create internal symbol representations instances (of CSymbol)
#           CSymbolMap used to 'maintain symbol list'
#           uses CLoSection and CLiSection
#  @state : waiting for cleanup
# =============================================================================

# pylint: disable=all

import re
import sys
import Util

# global symbol:
#     rbLinker_dsram2.data 50014490+000018   rbOsSetup_TaskBGC2_st
#    ([osection] addr+size [ |D|U] symbol)
#      b008fd40+000000   rbLinkerRamStartAdr4QM_lmu1_nc
#      00000000+000004 D ASSERT_FILE_SPU_CFG_ADC_1D_FFT_CFAR
#
# local  symbol:  rbLinker_dsram2.bss 5000b9e4+000010   libdsp.a(agc.o)       instance__L0__getInstance__3AGCSFv
#    (osection addr+size source symbol)
#
# m2 symbol
# Time_StmReInitMon                g 800dc6f4-800dc6ff 00000c DriveBlock0   rbLinker_DriveBlock0.user_text .text            librbTime.a(rbTime.o)
#   (symbol [g|l] start_addr-end_addr size memname osectin isection source
# Adc_GetGroupStatus               g 00000000-00000017 000018 dummy_mem  D                                   librba_cubas.a(Adc.o)
# Time_StmReInitMon                g 800dc6f4-800dc6ff 00000c DriveBlock0   rbLinker_DriveBlock0.user_text .text            librbTime.a(rbTime.o)
# rbLinker_DriveBlock0_user_text_END g 801b0e34-801b0e34 000000 DriveBlock0   rbLinker_DriveBlock0.user_text rbLinker_DriveBlock0.user_text <section map>
# rbLinkerFlashStartAdr4QM_DriveBlock0 g 801b0e40-801b0e40 000000 DriveBlock0                                     <section map>
# _ctors                           g 800b2940-800b2af3 0001b4 DriveBlock0   rbLinker_DriveBlock0.rodata .rodata          <C++ ctors and dtors>


class SymbolError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def p_ignore_symbol(kind, symbol_name, section_name, output_sections, p_verbose=False):
    result = False
    ignore_reason = "by name"
    if output_sections.p_ignore_section(section_name):
        result = True
        ignore_reason = 'allocated to section "{0}"'.format(section_name)
    if not result:
        result = symbol_name.startswith("__ghs_eofn_")
    if result and p_verbose:
        print('Ignoring {0} Symbol "{1}" {2}'.format(kind, symbol_name, ignore_reason))
    return result


def symbolCreator(
    line, lformat, inputsections, inputSectionIndex, outputSections, verbose=False, mapfile=None
):
    result = None
    if lformat == "local":
        result = localSymbol(
            line, inputsections, inputSectionIndex, outputSections, verbose, mapfile
        )
    elif lformat == "global":
        result = globalSymbol(
            line, inputsections, inputSectionIndex, outputSections, verbose, mapfile
        )
    elif lformat == "m2":
        result = m2Symbol(line, inputsections, inputSectionIndex, outputSections, verbose, mapfile)
    else:
        raise SymbolError('symbolCreator - unsupported line format "{0}"'.format(lformat))
    return result


def globalSymbol(line, inputsections, inputSectionIndex, outputSections, verbose, mapfile):
    result = None
    m1 = re.match(r"^\s+(\S+)?\s+([0-9a-f]{8})\+([0-9a-f]{6})\s([ DU])\s(.+)$", line)
    if m1:
        localSym = False
        oSection = None
        oSectionName = m1.group(1)
        address = int(m1.group(2), 16)
        size = int(m1.group(3), 16)
        notLinked = m1.group(4).strip()  # 'U|D'
        name = m1.group(5)
        iSection = None
        iSectionName = ""
        linkerSymbol = False
        source = "mf1_g"
        if not p_ignore_symbol("global", name, oSectionName, outputSections):
            if not bool(notLinked):
                if bool(oSectionName):

                    # print('globalSymbol {0} findInputSection at index {2} for address {3}'.format(name,inputSectionIndex(),hex(address)))
                    iSection = inputsections.getInputSection(inputSectionIndex, address)
                    if not bool(iSection):
                        # print('globalSymbol {0} findInputSection failed at index {1} for address {2} '.format(name,inputSectionIndex(),hex(address)))
                        linkerSymbol = True
                        oSection = outputSections.getSectionByName(
                            oSectionName, "symbol." + name, size
                        )
                    else:
                        oSection = outputSections.getSectionByName(oSectionName, "", 0)
                elif size == 0:
                    linkerSymbol = True
            result = CSymbol(
                name,
                address,
                size,
                localSym,
                iSection,
                iSectionName,
                oSection,
                oSectionName,
                source,
                linkerSymbol,
                notLinked,
            )
            result.checkOutputSectionRequired()
            result.checkOutputSectionName(verbose)
        else:
            pass
            # print('### IGNORE global symbol "{0}"'.format(name))
    else:
        print("### Unmatched global symbol line\n\t{0}".format(line))
    return result


def localSymbol(line, inputsections, inputSectionIndex, outputSections, verbose, mapfile):
    result = None
    m1 = re.match(r"^\s+(\S+)\s+([0-9a-f]{8})\+([0-9a-f]{6})\s+(\S+)\s+(.+)$", line)
    if m1:
        name = m1.group(5)
        address = int(m1.group(2), 16)
        size = int(m1.group(3), 16)
        localSym = True
        inputSection = None
        inputSectionName = ""
        outputSection = None
        outputSectionName = m1.group(1)
        source = "mf1_l"
        sourceStr = m1.group(4)
        linkerSymbol = False
        notLinked = ""
        if not p_ignore_symbol("local", name, outputSectionName, outputSections):
            if bool(outputSectionName):
                lib, module, tempLinkerSym, source = Util.getSource(sourceStr)
                inputSection = inputsections.getInputSection(inputSectionIndex, address)
                if not bool(inputSection):
                    raise SymbolError("ERROR local symbol {0} without intput section".format(name))
                outputSection = outputSections.getSectionByName(outputSectionName, "", 0)
                # print('InputSection for {0} : {1}'.format(name,inputSection))
                result = CSymbol(
                    name,
                    address,
                    size,
                    localSym,
                    inputSection,
                    inputSectionName,
                    outputSection,
                    outputSectionName,
                    source,
                    linkerSymbol,
                    notLinked,
                )
                result.checkOutputSectionName(verbose)
                result.checkSource(module, lib, verbose)
            else:
                raise SymbolError("ERROR local symbol {0} without output section".format(name))
        else:
            pass
            # print('### IGNORE local symbol "{0}"'.format(name))
    else:
        print("### Unmatched local symbol line\n\t{0}".format(line))
    return result


def m2Symbol(line, inputsections, inputSectionIndex, outputSections, verbose, mapfile):
    result = None
    m1 = re.match(
        r"^\s+(\S+)\s+(g|l)\s+([0-9a-f]{8})-([0-9a-f]{8})\s([0-9a-f]{6})\s(\S+)\s+(.+)$", line
    )
    if m1:
        name = m1.group(1)
        localSym = m1.group(2).lower() == "l"
        address = int(m1.group(3), 16)
        end_address = int(m1.group(4), 16)
        size = int(m1.group(5), 16)
        memname = m1.group(6)
        addData = m1.group(7)
        inputSection = None
        inputSectionName = ""
        outputSection = None
        outputSectionName = ""
        source = "mf2"
        linkerSymbol = False
        notLinked = ""
        m2 = re.match(r"^(D|U)\s+(\S+)$", addData)
        if m2:
            notLinked = m2.group(1)
            sourceStr = m2.group(2)
        else:
            m2 = re.match(r"^(\S+)\s+(\S+)\s+(.*)$", addData)
            if m2:
                outputSectionName = m2.group(1)
                inputSectionName = m2.group(2)
                sourceStr = m2.group(3)
            #            elif addData in ['<C++ ctors and dtors>','<section map>','<elxr>']:
            #                m2 = True
            else:
                sourceStr = addData
        p_ignore_this_symbol = p_ignore_symbol(
            "{0} M2".format("local" if localSym else "global"),
            name,
            outputSectionName,
            outputSections,
        )
        if not p_ignore_this_symbol:
            lib, module, linkerSymbol, source = Util.getSource(sourceStr)
            if not linkerSymbol and not bool(notLinked):
                inputSection = inputsections.getInputSection(inputSectionIndex, address)
                if not inputSection:
                    raise SymbolError("ERROR local symbol {0} without intput section".format(name))
            if bool(outputSectionName):
                if not bool(inputSection):
                    outputSection = outputSections.getSectionByName(
                        outputSectionName, "symbol" + name, size
                    )
                else:
                    outputSection = outputSections.getSectionByName(outputSectionName, "", 0)
            result = CSymbol(
                name,
                address,
                size,
                localSym,
                inputSection,
                inputSectionName,
                outputSection,
                outputSectionName,
                source,
                linkerSymbol,
                notLinked,
            )
            result.checkOutputSectionRequired()
            result.checkOutputSectionName(verbose)
            result.checkInputSectionName(verbose)
            result.checkSource(module, lib, verbose)
    else:
        print("### Unmatched symbol line\n\t{0}".format(line))
    return result


# result = CSymbol(name,address,size,True,lib,module,source,linkerSym,'','','',osection)
class CSymbol:
    def __init__(
        self,
        name,
        address,
        size,
        local,
        inputSection,
        inputSectionName,
        outputSection,
        outputSectionName,
        source,
        linkerSymbol,
        notlinked,
    ):
        self.__name = name
        self.__address = address
        self.__size = size
        self.__local = local
        self.__inputSection = inputSection
        self.__inputSectionName = inputSectionName
        self.__outputSection = outputSection
        self.__outputSectionName = outputSectionName
        self.__source = source
        self.__linkerSymbol = linkerSymbol
        self.__notlinked = notlinked
        if local:
            self.__globalName = ""
        else:
            self.__globalName = name
        self.__decodedName = ""
        self.__namespace = ""
        self.__alias = []
        self.__gapsize = 0

    def __str__(self):
        m_name = "{0} \n\t".format(self.__name)
        m_prop = 'addr: {0}  size: {1} (+ {2} ) linked: "{3}" {4} linkerSym: {5} aliases: {6}\n\t'.format(
            hex(self.__address),
            hex(self.__size),
            hex(self.__gapsize),
            self.__notlinked,
            ("local" if self.__local else "global"),
            self.__linkerSymbol,
            self.getAliasCount(),
        )
        m_sec = "InputSection: {0} OutputSection({1}): {2} \n\t".format(
            self.getInputSectionName(), self.p_haveOutputSection(), self.getOutputSectionName()
        )
        m_source = "lib: {0} mod: {1} source: {2}\n\t".format(
            self.getLibrary(), self.getModule(), self.getSource()
        )
        m_memprop = "MemName: {0} MemType: {1} SectionType: {2}".format(
            self.getMemName(), self.getMemType(), self.getSectionType()
        )
        return m_name + m_prop + m_sec + m_source + m_memprop

    def setDecodedName(self, dname):
        if not dname is None:
            self.__decodedName = dname

    def getDecodedName(self):
        return self.__decodedName

    def setNamespace(self, namespace):
        if not namespace is None:
            self.__namespace = namespace

    def checkOutputSectionRequired(self):
        if (
            self.__size > 0
            and not bool(self.__notlinked)
            and not (bool(self.__outputSection) or bool(self.__inputSection))
        ):
            raise SymbolError(
                "ERROR global symbol {0} of size {1} without output section\n\t{3}".format(
                    self.__name, self.__size, str(self)
                )
            )

    def checkOutputSectionName(self, verbose):
        if (
            verbose
            and bool(self.__outputSectionName)
            and self.getOutputSectionName() != self.__outputSectionName
        ):
            message = " symbol {0} of size {1} outputsection mismatch: {2} <-> {3}".format(
                self.__name, self.__size, self.__outputSectionName, self.getOutputSectionName()
            )
            print("### " + message)

    def checkInputSectionName(self, verbose):
        if (
            verbose
            and bool(self.__inputSectionName)
            and self.getInputSectionName() != self.__inputSectionName
        ):
            print(
                "### symbol {0} inputSectionName mismatch {2} <-> {3} \n\t{4}".format(
                    self.__name, self.__inputSectionName, self.getInputSectionName(), str(self)
                )
            )

    def checkSource(self, module, lib, verbose):
        if verbose and bool(self.__inputSection):
            sourceError = False
            message = "ERROR symbol {0} source mismatch".format(self.__name)
            if self.__inputSection.getModule() != module:
                sourceError = True
                message += "\n\tmodule name {1} <-> {2}".format(
                    module, self.__inputSection.getModule()
                )
            if self.__inputSection.getLibrary() != lib:
                sourceError = True
                message += "\n\tlibary name {1} <-> {2}".format(
                    lib, self.__inputSection.getLibrary()
                )
            if self.__inputSection.getSource() != self.__source:
                sourceError = True
                message += "\n\tsource string {1} <-> {2}".format(
                    self.__source, self.__inputSection.getSource()
                )
            if sourceError:
                print("### " + message)

    def getName(self):
        return self.__name

    def getNamespace(self):
        return self.__namespace

    def getAddress(self):
        return self.__address

    def getGapSize(self):
        return self.__gapsize

    def getSize(self, includeGap=""):
        result = self.__size
        if includeGap == "ALL":
            result += self.__gapsize
        elif includeGap == "ALIGNMENT":
            if self.__gapsize < 4:
                result += self.__gapsize
        return result

    def p_local(self):
        return self.__local

    def p_linkerSymbol(self):
        return self.__linkerSymbol

    def getInputSection(self):
        return self.__inputSection

    def getInputSectionStartAddress(self):
        result = -1
        if bool(self.__inputSection):
            result = self.__inputSection.getAddress()
        return result

    def getInputSectionName(self):
        result = ""
        if bool(self.__inputSection):
            result = self.__inputSection.getName()
        elif bool(self.__inputSectionName):
            result = self.__inputSectionName
        return result

    def getOutputSectionName(self):
        result = ""
        if bool(self.__outputSectionName):
            result = self.__outputSectionName
        else:
            if bool(self.__inputSection):
                result = self.__inputSection.getOutputSectionName()
        return result

    def getOutputSection(self):
        result = self.__outputSection
        if not bool(result) and bool(self.__inputSection):
            result = self.__inputSection.getOutputSection()
        return result

    def p_haveOutputSection(self):
        result = bool(self.__outputSection) or bool(self.__outputSection)

    def getLibrary(self, undefDefault=""):
        result = undefDefault
        if bool(self.__inputSection):
            result = self.__inputSection.getLibrary()
            if result is None:
                result = undefDefault
        return result

    def getModule(self, undefDefault=""):
        result = undefDefault
        if bool(self.__inputSection):
            result = self.__inputSection.getModule()
            if result is None:
                result = undefDefault
        return result

    def getSource(self):
        result = self.__source
        if bool(self.__inputSection):
            result = self.__inputSection.getSource()
        return result

    def getSectionType(self):
        result = ""
        if bool(self.__inputSection):
            result = self.__inputSection.getSectionType()
        elif bool(self.__outputSection):
            result = self.__outputSection.getSectionType()
        return result

    def getMemName(self):
        result = ""
        if bool(self.__inputSection):
            result = self.__inputSection.getMemName()
        elif bool(self.__outputSection):
            result = self.__outputSection.getMemName()
        return result

    def getMemType(self):
        result = ""
        if bool(self.__inputSection):
            result = self.__inputSection.getMemType()
        elif bool(self.__outputSection):
            result = self.__outputSection.getMemType()
        return result

    def getMemStartAddress(self):
        result = -1
        if bool(self.__outputSection):
            result = self.__outputSection.getMemStartAddress()
        return result

    def getNotLinked(self):
        return self.__notlinked

    def p_notLinked(self):
        return not bool(self.__notlinked)

    def p_literal(self):
        return not bool(self.__notlinked) and not bool(self.__outputSection) and self.__linkerSymbol

    def p_sameLocalSym(self, other):
        return (
            self.__local
            and other.__local
            and self.__address == other.__address
            and self.__size == other.__size
            and self.__osectionName == other.__osectionName
            and self.__module == other.__module
            and self.__lib == other.__lib
        )

    # use only in mapfile type 2 addSymol (or ensure module lib is setup properly)
    def p_sameLocalAsGlobalSym(self, local):
        return (
            self.__local != local.__local
            and self.__address == local.__address
            and self.__size == local.__size
            and self.__osectionName == local.__osectionName
            and self.__module == local.__module
            and self.__lib == local.__lib
        )

    def p_sameSym(self, other):
        return (
            self.__address == other.__address
            and self.__size == other.__size
            and self.__outputSection == other.__outputSection
            and self.getModule() == other.getModule()
            and self.getLibrary() == other.getLibrary()
        )

    def getLocalId(self):
        return ":".join([self.getLibrary(), self.getModule(), self.__name])

    def p_linked(self):
        return self.__notlinked == ""

    # def updateSoureData(self,isection,module,lib,source,osection):
    # if self.__osectionName == osection:
    # if module:
    # self.__isectionName = isection
    # self.__lib = lib
    # self.__module = module
    # self.__source = source
    # else:
    # self.__linkerSym = True
    # elif not bool(osection):
    # self.__linkerSym = True
    # elif self.__size == 0:
    # # TODO check aliases instead
    # pass
    # else:
    # raise SymbolError('TODO osection for symbol {0} --- {1}'.format(osection,str(self)))

    def incGapsize(self, size):
        self.__gapsize += size

    def getSizeToInputSectionEnd(self, address):
        result = -1
        if bool(self.__inputSection):
            result = self.__inputSection.getSizeToSectionEnd(address)
        return result

    def getSizeToOutputSectionEnd(self, address):
        #        print('getSizeToOutputSectionEnd {0}'.format(hex(address)))
        result = -1
        if bool(self.__outputSection):
            result = self.__outputSection.getSizeToSectionEnd(address)
        return result

    def p_symbolInSameSection(self, other):
        result = self.getOutputSectionName() == other.getOutputSectionName()
        if not result and len(self.__alias) > 0:
            for asym in self.__alias:
                if asym.getOutputSectionName() == other.getOutputSectionName():
                    result = True
                    break
        return result

    def addSymbolGaps(self, nextSym, verbose):
        gapSize = 0
        sameOsection = False
        if bool(nextSym):
            sameOsection = self.p_symbolInSameSection(nextSym)
            # sameIsection = ( self.getInputSectionName() == nextSym.getInputSectionName() )
            igapSize = 0
            if not self.__linkerSymbol or self.__size > 0:
                # if not sameIsection:
                # igapSize = self.getSizeToInputSectionEnd(self.__address) - self.__size
                if sameOsection:
                    gapSize = nextSym.__address - self.__address - self.__size
                else:
                    # gapSize = self.getSizeToInputSectionEnd(self.__address) - self.__size
                    gapSize = self.getSizeToOutputSectionEnd(self.__address) - self.__size
                    # if gapSize  != ogapSize:
                    # print('addSymbolGaps OSECTION {0} {1}  -  {2} O {3}'.format(self.getName(),hex(self.getAddress()),gapSize,ogapSize))
                    if gapSize < 0:
                        if self.__size == 0:
                            gapSize = 0
                        else:
                            print(
                                "SYMBOL (gapsize {0}) crossing section border\n{1}\n{2}".format(
                                    gapSize, self, nextSym
                                )
                            )
                # if not sameIsection and igapSize != gapSize:
                # print('addSymbolGaps ISECTION {0} {1}  -  {2} I {3}'.format(self.getName(),hex(self.getAddress()),gapSize,igapSize))
        elif not self.__linkerSymbol or self.__size > 0:
            gapSize = self.getSizeToInputSectionEnd(self.__address) - self.__size
        if gapSize > 0:
            self.__gapsize = gapSize
        elif gapSize < 0:
            print(
                "addSymbolGaps (sameOsection: {4}) failed {0} ... sym {1} .. {2}  next sym {3}".format(
                    gapSize,
                    hex(self.__address),
                    hex(self.__address + self.__size),
                    (hex(nextSym.__address) if bool(nextSym) else "EOL"),
                    sameOsection,
                )
            )

        if self.__gapsize != 0 and verbose:
            print(
                "addSymbolGaps GAP(sameOsection: {4})  {0} at end of ... {1} {2} next: {3}".format(
                    gapSize,
                    hex(self.__address),
                    hex(self.__size),
                    (hex(nextSym.__address) if bool(nextSym) else "EOL"),
                    sameOsection,
                )
            )
        return gapSize

    def getGapSize(self, includeGap="ALL"):
        result = 0
        if includeGap == "ALL":
            result += self.__gapsize
        elif includeGap == "ALIGNMENT":
            if self.__gapsize < 4:
                result += self.__gapsize
        return result

    def aliasAppend(self, symbol):
        self.__alias.append(symbol)

    def aliasExtend(self, symbolList):
        self.__alias.extend(symbolList)

    def aliasClear(self):
        self.__alias.clear()

    def getAlias(self):
        return self.__alias

    def getAliasCount(self):
        return len(self.__alias)

    # def setInputSection(self,isection,p_mapfileType1=True):
    # if self.__isection is None:
    # self.__isection = isection
    # else:
    # raise SymbolError('setInputSection: inputsection already set in symbol {0}'.format(self))
    # if p_mapfileType1:
    # if isection is None:
    # self.__linkerSym = True
    # else:
    # osectionName = isection.getOSectionName()
    # isectionName = isection.getName()
    # if self.__osectionName == osectionName:
    # self.__isectionName = isectionName
    # if self.__local:
    # pass
    # else:
    # self.__library = isection.getLib()
    # self.__module = isection.getModule()
    # self.__source  = isection.getSource()
    # else:
    # raise SymbolError('ERROR osection  {0} differs for symbol {1}'.format(osectionName,str(self)))
    # else:
    # if not isection is None:
    # osectionName = isection.getOSectionName()
    # if self.__osectionName != osectionName:
    # raise SymbolError('ERROR osection  {0} differs for symbol {1}'.format(osectionName,str(self)))
    # isectionName = isection.getName()
    # if self.__isectionName != isectionName:
    # raise SymbolError('ERROR isection  {0} differs for symbol {1}'.format(isectionName,str(self)))

    def updateFromLocalSymbol(self, localSym):
        if (
            self.__size == localSym.__size
            and self.getInputSection() == localSym.getInputSection()
            and self.getOutputSection() == localSym.getOutputSection()
        ):
            self.__globalName = self.__name
            self.__name = localSym.__name
            self.__local = True
        else:
            raise SymbolError(
                "global symbol and local symbol at same address but different size\n{0}\n{1}".format(
                    str(self), str(localSym)
                )
            )


class CSymbolMap:
    def __init__(self, type=""):
        self.__byAddr = dict()
        self.__addrIndex = None
        self.__literal = []
        self.__deleted = []
        self.__undef = []
        self.__lalias = dict()
        self.__laliasAddress = dict()
        self.__mapType = type

    def addSymbol(self, symbol, verbose=False):
        saddr = symbol.getAddress()
        ul = symbol.getNotLinked()
        if saddr == 0 and ul in ["U", "D"]:
            # print('### unsued {0} {1}'.format(len(self.__deleted),str(symbol)))
            if ul == "D":
                self.__deleted.append(symbol)
            elif ul == "U":
                self.__undef.append(symbol)
        elif symbol.p_literal():
            # print('### literal {0}'.format(str(symbol)))
            self.__literal.append(symbol)
        elif saddr in self.__byAddr:
            # print('### alias  {0}'.format(str(symbol)))
            osym = self.__byAddr[saddr]
            if symbol.getSize() == 0:
                osym.aliasAppend(symbol)
            else:
                if osym.getSize() == 0:
                    self.__byAddr[saddr] = symbol
                    symbol.aliasExtend(osym.getAlias())
                    symbol.aliasAppend(osym)
                    osym.aliasClear()
                else:
                    if symbol.p_sameSym(osym):
                        self.addLAlias(symbol, osym)
                    else:
                        raise SymbolError(
                            'CSymbolMap: found more than 1 non zero sized symbols "{0}" "{1}"at same address  {2}'.format(
                                osym.getName(), symbol.getName(), hex(saddr)
                            )
                        )
        else:
            self.__byAddr[saddr] = symbol

    def addLAlias(self, symbol1, symbol2):
        sid1 = symbol1.getLocalId()
        sid2 = symbol2.getLocalId()
        # print('### create alias {0}  <->  {1}'.format(sid1,sid2))
        if not sid1 in self.__lalias:
            self.__lalias[sid1] = []
            self.__laliasAddress[sid1] = symbol1.getAddress()
        self.__lalias[sid1].append(sid2)
        if not sid2 in self.__lalias:
            self.__lalias[sid2] = []
        self.__lalias[sid2].append(sid1)

    def getIndex(self):
        return self.__addrIndex

    def getExistentSymbol(self, addr):
        result = None
        if addr in self.__addrIndex:
            result = self.__byAddr[addr]
        return result

    def getSymbol(self, addr):
        result = None
        if addr in self.__byAddr:
            result = self.__byAddr[addr]
        else:
            raise SymbolError("no symbol at addr {0}".format(hex(addr)))
        return result

    def getDeletedSymbols(self):
        return self.__deleted

    def getSymbolList(self):
        if not bool(self.__addrIndex):
            result = [sym for sym in self.__byAddr.values()]
        else:
            result = [self.__byAddr[addr] for addr in self.__addrIndex]
        return result

    def createIndex(self):
        if not self.__addrIndex:
            self.__addrIndex = [x for x in self.__byAddr.keys()]
            self.__addrIndex.sort()

    def recreateIndex(self):
        self.__addrIndex = [x for x in self.__byAddr.keys()]
        self.__addrIndex.sort()

    def dump(self, specialSymbols=True):
        self.createIndex()
        for saddr in self.__addrIndex:
            print("{0}".format(str(self.__byAddr[saddr])))
        if specialSymbols:
            for sym in self.__literal:
                print("LIT {0}".format(str(sym)))
            for sym in self.__deleted:
                print("DEL {0}".format(str(sym)))
            for sym in self.__undef:
                print("UND {0}".format(str(sym)))


if __name__ == "__main__":
    sm = CSymbolMap()
    gloLines = [
        "                  00000000+000004 D ASSERT_FILE_SPU_CFG_ADC_1D_FFT_CFAR",
        "                  00000000+000012 D Rte_memcpy",
        "                  00000000+000000   SBST_CPU_Enter_Callback",
        "                  00000000+000002 D Xcp_MemWriteMainFunction",
        "                  00000000+000000   _LITERAL_DATA_",
        "                  00000000+000000 U _Mtx_destroy",
        "                  00000000+000000 U _Mtx_init",
        "                  00000000+000000 U _Mtx_lock",
        "                  00000000+000000 U _Mtx_unlock",
        "                  00000000+000000   _SMALL_DATA_A8_",
        "                  00000000+000000   _SMALL_DATA_A9_",
        "                  00000000+00002c D __CPR1089____vtbl__650Q3_5daddy6sender273TExtensionStaticConnection__tm__238_Q3_J14JJ20J218TExtensionDynamicSubscriber__tm__182_Q3_J14JJ20J119TSenderPortBase__tm__96_Q3_J14JJ20J77TInterface__tm__59_Q3_J14J7mempool22CConstMemPoolInterfaceXCbL_1_0XCUiL_1_0XCUiL_1_2Q4_J14J8receiver9interface5CBase__Q3_J14JJ20J337TExtensionProxyIntervention__tm__301_Q3_J14JJ20JJ27JXCbL_1_0__Q3_J14JJ20J407TExtensionPortMetaData__tm__376_Q3_J14JJ20JJ321JQ2_J14J9CInternal..C.3A.5CGIT.5Cpjif.5CgeneratedFiles.5CRadar_C0_MXL.5CCMakeFiles.5Cdaddy_qualification_tests.2Edir.5CC_.5CGIT.5Cpjif.5Cip_if.5Cmom.5Cdaddy.5Ctest.5Cqualification_tests.5Csrc.5Cdaddy_check_for_data_availability.",
        "                  00000001+000000   __ghs_cxx_do_thread_safe_local_static_inits",
        "                  00000002+000000   __ghs_log_fee_level",
        "                  00000018+000000   rbLinker_dsram1_data_SIZE",
        "                  00000018+000000   rbLinker_dsram2_data_SIZE",
        "                  0000001c+000000   rbLinker_lmu0_nc_bss_SIZE",
        "                  00000090+000000   rbLinker_dsram0_data_SIZE",
        "                  00000114+000000   rbLinker_dlmu0_nc_data_SIZE",
        " rbLinker_dsram2.sbst 50000000+000000   rbLinker_dsram2_sbst_START",
        " rbLinker_dsram2.sbst 50000100+000000   rbLinker_dsram2_sbst_END",
        " rbLinker_dsram2.ustack 50000100+000000   rbLinker_dsram2_ustack_START",
        " rbLinker_dsram2.csa 50008100+000000   rbLinker_dsram2_csa_START",
    ]
    locLines = [
        " rbLinker_dsram0.bss 70018c28+000001   librba_cubas.a(Dcm_Dsl_Session.o) Dcm_isResetToDefaultRequested_b",
        " rbLinker_dsram0.bss 70018c89+000001   librba_cubas.a(EcuM_MainFunction.o) EcuM_Prv_ShutDownflgCoresStopped",
        " rbLinker_dsram0.bss 70018c8a+000001   librba_cubas.a(EcuM_MainFunction.o) EcuM_Prv_ShutDownflgCoresTimeout",
        " rbLinker_dsram0.bss 70018c8c+000008   librba_cubas.a(EthTrcv_DiagnosticApis.o) EthTrcv_Prv_PhyIdentifier_au32",
        " rbLinker_dsram0.bss 70018c94+000001   librba_cubas.a(EthTrcv_DiagnosticApis.o) EthTrcv_Prv_IdentifierIndex_u8",
        " rbLinker_dsram0.bss 70018ca8+000004   librba_cubas.a(rba_FlsIfx_Erase.o) rba_FlsIfx_LastErasedSectorNum_u32",
        " rbLinker_dsram0.bss 70018cac+000001   librba_cubas.a(rba_FlsIfx_Erase.o) rba_FlsIfx_NumSector_u8",
        " rbLinker_dsram0.bss 70018cad+000001   librba_cubas.a(rba_FlsIfx_Erase.o) rba_FlsIfx_EraseRetries_u8",
    ]
    lines = [
        " ASSERT_FILE_DSP_MNP_WORKER       g 00000000-00000003 000004 dummy_mem  D                                   libdsp.a(dsp_assert.o)",
        " __UNNAMED_1                      l 80093534-80093537 000004 DriveBlock0   rbLinker_DriveBlock0.rodata .ghs.linkonce.7..rodata.__ct__Q2_3net28CNetRx_CANFD_RxPduArrayLargeFv libnet_x.a(rbNetCom_BusReceiverCANFD.o)",
        " __ghs_GetCurrentThreadID         g 00000000-00000000 000000 dummy_mem  U                                   libsedgnoe.a(guard.o)",
        " BRIDGE                           g f0040008-f0040008 000000 lmu1_nc                                        <section map>",
        " _dtors                           g 800b2af4-800b2af7 000004 DriveBlock0   rbLinker_DriveBlock0.rodata .rodata          <C++ ctors and dtors>",
        " _tls_ctors                       g 800b2af8-800b2afb 000004 DriveBlock0   rbLinker_DriveBlock0.rodata .rodata          <C++ ctors and dtors>",
        " _BUILDINFO_START                 g 800b2afc-800b2afc 000000 DriveBlock0   rbLinker_DriveBlock0.rodata rbLinker_DriveBlock0.rodata <section map>",
        " rbLinkerBlockCurrentDriveBlock0  g 800b2afc-800b2afc 000000 DriveBlock0                                     <section map>",
        " rbLinker_DriveBlock0_dsram0_data_START g 800b2afc-800b2afc 000000 DriveBlock0                                     <section map>",
        " rbLinker_DriveBlock0_rodata_END  g 800b2afc-800b2afc 000000 DriveBlock0   rbLinker_DriveBlock0.rodata rbLinker_DriveBlock0.rodata <section map>",
        " rbLinker_DriveBlock0_user_rodata_END g 800b2afc-800b2afc 000000 DriveBlock0   rbLinker_DriveBlock0.user_rodata rbLinker_DriveBlock0.user_rodata <section map>",
        " rbLinker_DriveBlock0_user_rodata_START g 800b2afc-800b2afc 000000 DriveBlock0   rbLinker_DriveBlock0.user_rodata rbLinker_DriveBlock0.user_rodata <section map>",
        " rbLinker_DriveBlock0_dsram1_data_START g 800b2b8c-800b2b8c 000000 DriveBlock0                                     <section map>",
    ]
    for line in gloLines:
        # globalSymbol 'global'
        # localSymbol 'local'
        # symbol 'm2'
        sy = symbolCreator(line, "global")
        if sy:
            print("SY {0} : {1}".format(line, str(sy)))
            sm.addSymbol(sy)
        else:
            print("SY {0} : {1}".format(line, "none"))
    sm.dump()
