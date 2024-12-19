# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  @copyright (c) 2021 by Robert Bosch GmbH. All rights reserved.
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
#  @brief : resource_symbol - enrich symbol provided by map reader with
#           resource calculation relevant data
# =============================================================================

from budget import Budget as Account


def get_symbol_resource(map_symbol, config):
    if map_symbol.getAddress == 0 or map_symbol.getSize("ALL") == 0:
        return None
    return SymbolResource(map_symbol, config)


class SymbolResource:
    def __init__(self, symbol, config):
        self._mapfile_symbol = symbol
        self._domain = config.map_symbol_into_domain(
            symbol, symbol.getNamespace(), symbol.getName(), symbol.getModule(), symbol.getLibrary()
        )
        self._objectfile = symbol.getModule()
        self._library = symbol.getLibrary()
        if not self._library:
            self._library = "nolib"
        qualified_object_filename = config.get_qualified_object_file_name(
            symbol.getModule(), symbol.getLibrary()
        )
        self._qualified_objectfile = None
        if qualified_object_filename:
            self._qualified_objectfile = qualified_object_filename[0]
        else:
            self._qualified_objectfile = symbol.getModule()
            if not self._qualified_objectfile or self._objectfile == "__linker__":
                self._qualified_objectfile = "linker"
                self._objectfile = "linker"
                self._library = "linker"

        self._account = Account()
        self._resource_memname = {}
        symbol_size = symbol.getSize("ALL")  # include gaps
        section_type = symbol.getSectionType()  # text,data,bss
        output_section = symbol.getOutputSection()
        memory_name = output_section.getMemName()  # phys memory block name
        memory_type = output_section.getMemType()  # RAM, FLASH
        resource = config.get_memory_resource(memory_name)
        self._account[resource] = symbol_size
        self._resource_memname[resource] = memory_name
        p_mapped_resource = False
        if section_type == "bss":
            # memoty_type == FLASH -> Fehler
            pass
        elif section_type == "text":
            if memory_type == "FLASH":
                pass
            else:
                p_mapped_resource = True
        elif section_type == "data":
            # memoty_type == FLASH -> Fehler
            p_mapped_resource = True
        if p_mapped_resource:
            mapped_memory_name = output_section.getRomCopySectionMemName(None)
            if mapped_memory_name is None:
                # Fehler handle default name + rom resouse
                mapped_resource = config.get_default_mapped_resource()
                mapped_memory_name = config.get_errored_mapped_memory_name()
            else:
                mapped_resource = config.get_memory_resource(mapped_memory_name)
            if mapped_resource == resource:
                # Fehler
                print("ERROR while mapping")
                self.p_mapped_resource = False
            else:
                self._mapped = True
                self._account[mapped_resource] = symbol_size
                self._resource_memname[mapped_resource] = mapped_memory_name

    def __getitem__(self, item):
        if item == "account":
            return self._account
        elif item == "domain":
            return self._domain
        elif item == "qualifiedobject":
            return self._qualified_objectfile
        elif item == "object":
            return self._objectfile
        elif item == "library":
            return self._library
        elif item == "name":
            return self._mapfile_symbol.getName()
        elif item == "namespace":
            return self._mapfile_symbol.getNamespace()
        elif item == "memoryname":
            return self._resource_memname
        elif item == "decodedname":
            return self._mapfile_symbol.getDecodedName()
        elif item == "outputsection":
            return self._mapfile_symbol.getOutputSectionName()
        else:
            raise KeyError(item)

    def _p_mapped_resource(self):
        return self._p_mapped_resource

    def dump(self):
        print(
            "#### s_id: {0} name: {1} domain: {2}  account: {3} res_mem {4}\n\tlibrary: {5} object: {6}".format(
                id(self._mapfile_symbol),
                self._mapfile_symbol.getName(),
                self._domain,
                self._account,
                self._resource_memname,
                self._library,
                self._objectfile,
            ),
        )
