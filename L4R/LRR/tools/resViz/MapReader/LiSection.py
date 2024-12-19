# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  @copyright (c) 2019 - 2021 by Robert Bosch GmbH. All rights reserved.
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
#  @brief : parse GHS module summary lines
#           and creates internal representation CLiSection instances
#           CLiSectionMap to maintain CLiSection list
#           uses CLoSection
#  @state : waiting for cleanup
# =============================================================================

# pylint: disable=all

import re
import Util
import sys


class LiSectionMapError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def p_headerLine(line):
    return re.match("^\s+Origin\+Size\s+Section\s+Module$", line)


def LiSection(line, osections, verbose, fileReader=None):
    result = None
    if not p_headerLine(line):
        smatch = re.match("^([0-9a-f]{8})\+([0-9a-f]{6,8})\s+(\S+)( -> (\S+))?\s+(.+)$", line)
        if smatch:
            address = int(smatch.group(1), 16)
            size = int(smatch.group(2), 16)
            name = smatch.group(3)
            os_name = name
            # print('m4 {0}   .... m5 {1}'.format(smatch.group(4),smatch.group(5)))
            if smatch.group(4):
                os_name = smatch.group(5)
            sourceStr = smatch.group(6)
            if not osections.p_ignore_section(name):
                lib, module, linkersource, source = Util.getSource(sourceStr)
                osection = osections.getSectionByName(os_name, name, size)
                if not bool(osection):
                    print(
                        "### IS ignoring {0} no output section found by name {1} ".format(
                            name, os_name
                        )
                    )
                else:
                    result = CLiSection(
                        name, address, size, os_name, osection, source, module, lib, linkersource
                    )
            else:
                pass
                # print("###  Ignore LiSection line\n\t{0}".format(line))
        else:
            print("###  Unmatched LiSection line\n\t{0}".format(line))
    return result


class LiSectionIndex(object):
    def __init__(self, n=0):
        self.__pos = n

    def update(self, n):
        self.__pos = n

    def __call__(self, n=-1):
        result = self.__pos
        if n >= 0:
            self.__pos = n
        return result


class CLiSection(object):
    def __init__(self, name, address, size, os_name, osection, source, module, lib, linkersource):
        self.__name = name
        self.__address = address
        self.__size = size
        self.__osectionName = os_name
        self.__osection = osection
        self.__source = source
        self.__module = module
        self.__lib = lib
        self.__linkersource = linkersource

    def getName(self):
        return self.__name

    def getSize(self):
        return self.__size

    def p_addressInSection(self, address):
        return self.__address <= address and address < self.__address + self.__size

    def getSizeToSectionEnd(self, address):
        result = -1
        if self.p_addressInSection(address):
            result = self.__address + self.__size - address
        return result

    def getAddress(self):
        return self.__address

    def getSource(self):
        return self.__source

    def getModule(self):
        return self.__module

    def getLibrary(self):
        return self.__lib

    def getSectionType(self):
        result = ""
        if self.__osection:
            result = self.__osection.getSectionType()
        return result

    def getMemType(self):
        result = ""
        if self.__osection:
            result = self.__osection.getMemType()
        return result

    def getMemName(self):
        result = ""
        if self.__osection:
            result = self.__osection.getMemName()
        return result

    def getOutputSectionName(self):
        result = self.__osectionName
        if self.__osection:
            result = self.__osection.getName()
        return result

    def getOutputSection(self):
        return self.__osection

    def __str__(self):
        return "IS {0} ({1} + {2}) os: {3} [defined({4})] lib {5} mod {6} (source >>{7}<<) linkersource {8}".format(
            self.__name,
            hex(self.__address),
            hex(self.__size),
            self.__osectionName,
            bool(self.__osection),
            self.__lib,
            self.__module,
            self.__source,
            self.__linkersource,
        )


class CLiSectionMap:
    def __init__(self):
        self.__byAddr = {}
        self.__addrIndex = None

    def addLiSection(self, lisection):
        saddr = lisection.getAddress()
        if saddr in self.__byAddr:
            raise LiSectionMapError(
                "CLosectionMap: linker output section {0} and {1} mapped to same address {2] ".format(
                    lisection.getName(), self.__byAddr[saddr].getName(), saddr
                )
            )
        self.__byAddr[saddr] = lisection

    def createIndex(self):
        self.__addrIndex = [x for x in self.__byAddr.keys()]
        self.__addrIndex.sort()

    # def getLiSectionId(self,addr):
    # lastAddr = -1
    # for iaddr in self.__addrIndex:
    # if iaddr > addr:
    # break
    # lastAddr = iaddr
    # if lastAddr > 0:
    # lis = self.__byAddr[lastAddr]
    # if addr >= (lastAddr + lis.getSize()):
    # lastAddr = -1
    # if lastAddr < 0:
    # # TODO handle linker symbols
    # raise LiSectionMapError('CLisectionMap - addr {0} not found section in section map'.format(str(addr)))
    # return lastAddr

    # def binSearch(self,addr):
    # return self.binRSearch(0,len(self.__addrIndex),addr)

    # def binRSearch(self,start,end,addr):
    # result = None
    # if end - start < 2:
    # i = start
    # while i < end:
    # eaddr = self.__addrIndex[i]
    # entry = self.__byAddr[eaddr]
    # size = entry.getSize()
    # if eaddr <= addr and eaddr + size > addr:
    # result = entry;
    # break
    # else:
    # mid = int(( start + end ) / 2)
    # if self.__addrIndex[mid] <= addr:
    # result = binRSearch(self,mid,end,addr)
    # else:
    # result = binRSearch(self,start,mid-1,addr)
    # return result

    def getInputSection(self, posObj, addr):
        # print('getInputSection({0},{1})'.format(posObj(),hex(addr)))
        currPos = posObj()
        newPos, section = self.findLiSection(currPos, addr)
        if newPos != currPos:
            posObj(newPos)
        return section

    def findLiSection(self, index, addr):
        foundSection = None
        work_index = index
        lasti = index
        li = len(self.__addrIndex)
        while work_index < li:
            # print('findLiSection loopo {0} , {1} LI {2}'.format(work_index, li,hex(self.__addrIndex[work_index])))
            if addr < self.__addrIndex[work_index]:
                break
            else:
                lasti = work_index
            work_index += 1
        sectionaddress = self.__addrIndex[lasti]
        tempsection = self.__byAddr[sectionaddress]
        sectionSize = tempsection.getSize()
        # print('{0} {1} :: {2}'.format(sectionaddress,sectionaddress + sectionSize,addr))
        if sectionaddress <= addr and addr < (sectionaddress + sectionSize):
            foundSection = tempsection
        if not bool(foundSection):
            lasti = index
        # if addr > int('5000b9e4',16):
        # sys.exit(0)
        return lasti, foundSection

    def dump(self):
        skl = [x for x in self.__byAddr.keys()]
        skl.sort()
        for saddr in skl:
            lis = self.__byAddr[saddr]
            print("{0}".format(str(lis)))


if __name__ == "__main__":
    sm = CLiSectionMap()
    lines = [
        " Origin+Size    Section          Module",
        "800d80f8+000af0  .text -> rbLinker_DriveBlock0.user_text  spu_sbst.o",
        "800740f0+00ed30  .rodata -> rbLinker_DriveBlock0.rodata spu_sbst.o",
        "00000000+000038  .debug_frame     spu_sbst.o",
        "00000000+00c230  .debug_info      spu_sbst.o",
        "00000000+0003cb  .debug_abbrev    spu_sbst.o",
        "00000000+000047  .comment         spu_sbst.o",
        "800b8000+01138a  .text.ifx_sbst0 -> rbLinker_DriveBlock0.ifx_sbst0 CPU_SBST.o"
        "800ca604+000188  .text.ifx_sbst2 -> rbLinker_DriveBlock0.ifx_sbst2 CPU_SBST.o",
        "800c938c+001278  .text.ifx_sbst1 -> rbLinker_DriveBlock0.ifx_sbst1 CPU_SBST.o",
        "800d0478+000804  .text.ifx_sbst6 -> rbLinker_DriveBlock0.ifx_sbst6 CPU_SBST.o",
        "00000047+000047  .comment         CPU_SBST.o",
        "80300050+000010  rbLinkerSubBlockTableSectionHead1 -> rbLinker_DriveBlock1.SubBlockTable  librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "801ffbd0+000020  rbLinkerEpilogTableSection0 -> rbLinker_DriveBlock0.BlockEpilog  librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "801ffbc0+000010  rbLinkerEpilogTableSectionHead0 -> rbLinker_DriveBlock0.BlockEpilog librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "804c7bd0+000020  rbLinkerEpilogTableSection1 -> rbLinker_DriveBlock1.BlockEpilog  librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "804c7bc0+000010  rbLinkerEpilogTableSectionHead1 -> rbLinker_DriveBlock1.BlockEpilog librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "80074000+000050  rbLinkerBlockHeaderSection0 -> rbLinker_DriveBlock0.BlockHeader  librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "80300000+000050  rbLinkerBlockHeaderSection1 -> rbLinker_DriveBlock1.BlockHeader  librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "0000c230+001053  .debug_info      librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "000003cb+0000cb  .debug_abbrev    librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "000005cc+0007cb  .debug_line      librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "00000000+00080c  .debug_macinfo   librbLinkerPL.a(rbLinker_BlockStructure.o)",
        "800d8be8+0015f4  .text -> rbLinker_DriveBlock0.user_text  librbStartup.a(rba_SysPreInit_Cfg.o)",
        "00000eee+000e3c  .comment         librbStartup.a(rba_SysPreInit_Cfg.o)",
        "0000d283+00d19a  .debug_info      librbStartup.a(rba_SysPreInit_Cfg.o)",
        "00000496+000196  .debug_abbrev    librbStartup.a(rba_SysPreInit_Cfg.o)",
        "00000d97+006d59  .debug_line      librbStartup.a(rba_SysPreInit_Cfg.o)",
        "0000080c+005fdf  .debug_macinfo   librbStartup.a(rba_SysPreInit_Cfg.o)",
        "00000038+000120  .debug_frame     librbStartup.a(rba_SysPreInit_Cfg.o)",
        "800da1dc+0000fa  .text -> rbLinker_DriveBlock0.user_text  librbStartup.a(Cpu0_Main.o)",
    ]
    n = 0
    for line in lines:
        li = LiSection(line, n)
        if li:
            print("LI {0} \n\t{1}".format(line, str(li)))
            sm.addLiSection(li)
        else:
            print("LI {0} : {1}".format(line, "none"))
        n += 1

    sm.dump()
