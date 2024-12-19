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
#  @brief : parse GHS immage summary lines
#           and creates internal representation CLoSection instances
#           uses MemConfig
#  @state : waiting for cleanup
# =============================================================================

# pylint: disable=all

import re


class LoSectionMapError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def p_headerLine(line):
    return re.match("^\s+Section\s+Base\s+Size\(hex\)\s+Size\(dec\)\s+SecOffs$", line)


def LoSection(line, memConfig, p_verbose=False, fileReader=None):
    result = None
    if not p_headerLine(line):
        smatch = re.match(
            "^\s+(\S+)\s+([0-9a-f]{8})\s+([0-9a-f]{8})\s+([0-9]+)\s+([0-9a-f]+)$", line
        )
        if smatch:
            name = smatch.group(1)
            address = smatch.group(2)
            daddress = int(address, 16)
            size = smatch.group(3)
            dsize = int(size, 16)
            if CLoSectionMap.p_ignore_section(name):
                pass
                # print("Ignoring section {0} ".format(name))
            elif memConfig.p_allocatedAddress(daddress):
                memName = memConfig.getMemName(daddress)
                startAddr = memConfig.getMemStartAddr(daddress)
                memType = memConfig.getMemType(daddress)
                sectionType = memConfig.getSectionType(daddress, name)
                result = CLoSection(name, daddress, dsize, memName, startAddr, memType, sectionType)
            elif p_verbose:
                print("Ignoring unallocated OSection {0}  at addr {1}".format(name, hex(daddress)))
        else:
            print("###  Unmatched LoSection line\n\t{0}".format(line))
    return result


class CLoSection:
    def __init__(self, name, address, size, memName, memStartAddress, memType, sectionType):
        self.__name = name
        self.__address = address
        self.__size = size
        self.__memName = memName
        self.__memStartAdress = memStartAddress
        self.__memType = memType
        self.__sectionType = sectionType  # bss,data,text
        self.__aliases = []
        self.__mappedSections = {}
        self.__allocationSize = 0
        self.__position = -1
        self.__romCopySection = None

    def setRomCopySection(self, romCopySection, forced=False):
        if self.__sectionType in ["data"]:
            if not self.__romCopySection:
                self.__romCopySection = romCopySection
            elif forced:
                self.__romCopySection = romCopySection
            elif self.__romCopySection != romCopySection:
                print(
                    'when setting romCopySection for section "{0}" - ignoring "{1}" already set to "{2}"'.format(
                        self.__name, romCopySection.getName(), self.__romCopySection.getName()
                    )
                )

    def getRomCopySection(self):
        return self.__romCopySection

    def getRomCopySectionMemName(self, default=""):
        result = default
        if bool(self.__romCopySection):
            result = self.__romCopySection.getMemName()
        return result

    def getRomCopySectionName(self):
        result = ""
        if bool(self.__romCopySection):
            result = self.__romCopySection.getName()
        return result

    def setPosition(self, n):
        self.__position = n

    def getPosition(self):
        return self.__position

    def getSizeToSectionEnd(self, address):
        result = -1
        # print('LO getSizeToSectionEnd for "{0}" in LOS \n{1}'.format(hex(address),str(self)))
        if address >= self.__address and address < (self.__address + self.__size):
            result = self.__address + self.__size - address
        return result

    def getName(self):
        return self.__name

    def getSize(self):
        return self.__size

    def getAddress(self):
        return self.__address

    def getSectionType(self):
        return self.__sectionType

    def getMemName(self):
        return self.__memName

    def getMemType(self):
        return self.__memType

    def getMemStartAddress(self):
        return self.__memStartAdress

    def getAllocatedSize(self):
        return self.__allocationSize

    def addMappedSection(self, name, size=0):
        if bool(name) and name not in self.__mappedSections:
            self.__mappedSections[name] = 1
        self.__allocationSize += size

    def p_used(self):
        return self.__allocationSize > 0

    def getRefCount(self):
        return len(self.__mappedSections.keys())

    def __str__(self):

        return "OutputSection: {0} at {1} .. {2} size {3} alisas({4}) pos {8} - MemInfo {5} {6} {7} - RomCopy {9}".format(
            self.__name,
            hex(self.__address),
            hex(self.__address + self.__size),
            self.__size,
            len(self.__aliases),
            self.__memName,
            self.__memType,
            self.__sectionType,
            self.__position,
            self.getRomCopySectionName(),
        )

    def mvAliasesFrom(self, otherSection):
        self.__aliases.extend(otherSection.__aliases)
        self.__aliases.append(otherSection.__name)
        otherSection.__aliases.clear()

    def addAlias(self, name):
        self.__aliases.append(name)


class CLoSectionMap:
    @classmethod
    def p_ignore_section(cls, section_name):
        result = False
        if section_name is not None:
            result = (
                section_name
                in [
                    "/DISCARD/",
                    ".gstackfix",
                    ".comment",
                ]
                or section_name.startswith(".debug_")
            )
        return result

    def __init__(self, memConfig=None):
        self.__memConfig = memConfig
        self.__byAddr = {}
        self.__addrIndex = None
        self.__byName = {}

    def addLoSection(self, losection):
        saddr = losection.getAddress()
        name = losection.getName()
        if name in self.__byName:
            raise LoSectionMapError(
                "CLoSectionMap: duplicate linker output section {0} and {1}".format(name)
            )
        self.__byName[name] = saddr
        if saddr in self.__byAddr:
            osAtAddr = self.__byAddr[saddr]
            csize = losection.getSize()
            if csize > 0:
                if osAtAddr.getSize() == 0:
                    # print('### Ignore LoSection \n\t{0}'.format(str(self.__byAddr[saddr])))
                    self.__byAddr[saddr] = losection
                    losection.mvAliasesFrom(osAtAddr)
                else:
                    raise LoSectionMapError(
                        "CLoSectionMap: linker output section {0} and {1} mapped to same address {2}".format(
                            name, osAtAddr.getName(), hex(saddr)
                        )
                    )
            else:
                osAtAddr.addAlias(name)
                # print('### Ignore LoSection \n\t{0}'.format(str(losection)))
                pass
        else:
            self.__byAddr[saddr] = losection

    def createIndex(self):
        self.__addrIndex = [x for x in self.__byAddr.keys()]
        self.__addrIndex.sort()
        pos = 0
        for ix in self.__addrIndex:
            # self.__byAddr[ix].__setPosition(pos)
            los = self.__byAddr[ix]
            los.setPosition(pos)
            pos += 1

    def getAdrressIndex(self):
        return self.__addrIndex

    def getSectionByAddr(self, addr):
        return self.__byAddr[addr]

    def getSectionNames(self):
        return list(self.__byName.keys())

    def getSectionByName(self, name, isectionName="", size=0):
        result = None
        if name in self.__byName:
            addr = self.__byName[name]
            result = self.__byAddr[addr]
            if bool(isectionName):
                result.addMappedSection(isectionName, size)
        return result

    def getSectionList(self):
        return [self.__byAddr[ix] for ix in self.__addrIndex]

    def getIndex(self):
        return self.__addrIndex

    def getLoSection(self, addr):
        lastAddr = -1
        for iaddr in self.__addrIndex:
            if iaddr > addr:
                break
            lastAddr = iaddr
        if lastAddr > 0:
            los = self.__byAddr[lastAddr]
            if addr >= (lastAddr + los.getSize()):
                lastAddr = -1
        if lastAddr < 0:
            raise LoSectionMapError(
                "CLoSectionMap - addr {0} not found section in section map".format(str(addr))
            )
        return lastAddr

    def dump(self):
        skl = [x for x in self.__byAddr.keys()]
        skl.sort()
        for saddr in skl:
            los = self.__byAddr[saddr]
            print("{0}".format(str(los)))


if __name__ == "__main__":
    from MemConfig import MemConfig

    sm = CLoSectionMap()
    mCfg = MemConfig()
    lines = [
        " Section              Base      Size(hex)    Size(dec)  SecOffs",
        "  rbLinker_dsram0.ustack 70000000  0000c000        49152   0000000",
        "  rbLinker_dsram0.data 70018d8c  00000090          144   003f2dc",
        "  rbLinker_DriveBlock1.RBSignature 804c7c00  00000400         1024   01e2978",
        "  .debug_frame         00000000  000a5c80       679040   01e2d78",
        "  .debug_info          00000000  129aa472    312124530   02889f8",
    ]
    for line in lines:
        lo = LoSection(line, mCfg, True)
        if lo:
            print("LO {0} : {1}".format(line, str(lo)))
            sm.addLoSection(lo)
        else:
            print("LO {0} : {1}".format(line, "none"))
    sm.dump()
