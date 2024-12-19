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
#  @brief : parse project configuration and provide domain configuration
#           domain mapper as part of it
# =============================================================================


import sys
import re
import json

from budget import Budget

from domain_mapper import DomainMapper
from domain_config import DomainConfig, DomainConfigError
from memory_resource_mapping import MemoryResourceMapper


class ProjectConfigError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


def get_project_configuration(config_file, available_memory_file):
    config = ProjectConfig(config_file, available_memory_file)
    config.init()
    return config


class ProjectConfig:

    _domain_mapper_order = ["scom", "symbols", "objs", "libs"]
    """list (order) of criteria to map a symbol to a software domain"""

    _resources = MemoryResourceMapper.get_resource_list()
    _default_domain_config = {key: 0 for key in _resources}
    """tracked default resources and their default config settings"""

    _scom_namespace = ["scom"]
    _scom_objectfile = ["libmain_x.a(scom.o)", "libmain_x.a(scom.cpp.o)"]
    """default scom namespace and scom object file"""

    _project_special_domains = ["LINKER", "NODOMAIN"]
    """domains to collect linker created symbols or symbols not mapped by configuration"""

    # setup Budget class to support resources defined here
    Budget.set_available_resources(_resources)

    @classmethod
    def get_available_resources(cls):
        return cls._resources

    @classmethod
    def get_qualified_object_file_name(cls, module_name, library_name):
        """ create combined (qualified) name out of library and object filename"""
        result = []
        if library_name:
            result.append("{0}({1})".format(library_name, module_name))
        return result

    @classmethod
    def get_qualified_symbol_name(cls, symbol_name, module_name, library_name):
        """ create combined (qualified) name out of library, objectfile and symbol symbol"""
        result = []
        if library_name:
            result.append("{0}({1}({2}))".format(library_name, module_name, symbol_name))
        if module_name:
            result.append("{0}({1})".format(module_name, symbol_name))
        return result

    @classmethod
    def get_memory_resource(cls, memory_name):
        try:
            return MemoryResourceMapper.get_memory_resource(memory_name)
        except KeyError:
            raise ProjectConfigError(
                'unconfigured memory_name "{0}" in memory_resource_mapping'.format(memory_name)
            )

    @classmethod
    def get_default_mapped_resource(cls):
        return MemoryResourceMapper.get_default_mapped_resource()

    @classmethod
    def get_resource_mapped_memory(cls):
        return MemoryResourceMapper.get_resource_mapped_memory()

    @classmethod
    def get_errored_mapped_memory_name(cls):
        return "_missing_mapped_memory_section_"

    def __init__(self, config_file_name, available_memory_file):
        self._config_file_name = config_file_name
        self._available_memory_file = available_memory_file
        self._available_memory = Budget()
        self._global_budget = Budget()
        self._domain_budget_sum = Budget()
        self._scom_namespace = ProjectConfig._scom_namespace
        self._scom_objectfile = ProjectConfig._scom_objectfile
        self._p_qualified_scom_objectfile = True
        self._special_domain_names = {}
        self._domain_mapper = DomainMapper(ProjectConfig._domain_mapper_order)
        self._domain_list = []
        self._domain_data = {}
        self._ambiguous_symbol_mapping = []
        self._unmapped_scom_symbols = []

    def get_unmapped_scom_symbols(self):
        """return scom (object file defined) symbols
        not mapped to a domain by 'scom' mapping function
        """
        return self._unmapped_scom_symbols

    def get_ambiguous_symbol_mapping(self):
        """return list of symbols mapped to more than one domain and their mapping configuration"""
        return self._ambiguous_symbol_mapping

    def get_unused_domain_mapping(self):
        """return mapping configurations which didn't map any symbol"""
        return self._domain_mapper.get_unused_mapper()

    def _p_is_scom_objectfile_symbol(self, module_name, qualified_module_name):
        """test object file is a scom object file"""
        if self._p_qualified_scom_objectfile and qualified_module_name:
            module_name = qualified_module_name[0]
        return module_name in self._scom_objectfile

    def map_symbol_into_domain(
        self, symbol, symbol_namespace, symbol_name, module_name, library_name
    ):
        """map symbol into a domain according project configuration
        apply mapper function function in the order described (not defined)
        in ProjectConfig._domain_mapper_order variable
        """
        domain_name = ""
        qualified_object_file_name = ProjectConfig.get_qualified_object_file_name(
            module_name, library_name
        )
        p_is_scom_object_file = self._p_is_scom_objectfile_symbol(
            module_name, qualified_object_file_name
        )
        if not domain_name:
            if p_is_scom_object_file:
                mapping = self._scom_mapper(symbol_namespace, symbol_name)
                domain_name = self._get_mapped_domain(symbol, mapping)
        # moved it down to symbol mapper
        #                if not domain_name:
        #                    self._unmapped_scom_symbols.append(symbol)
        if not domain_name:
            qualified_symbol_name = ProjectConfig.get_qualified_symbol_name(
                symbol_name, module_name, library_name
            )
            mapping = self._symbol_mapper(symbol_name, qualified_symbol_name)
            domain_name = self._get_mapped_domain(symbol, mapping)
            # allow scom symbols to mapped by its symbolname
            if p_is_scom_object_file and not domain_name:
                self._unmapped_scom_symbols.append(symbol)
        if not domain_name:
            mapping = self._object_mapper(module_name, qualified_object_file_name)
            domain_name = self._get_mapped_domain(symbol, mapping)
        if not domain_name:
            mapping = self._library_mapper(library_name, [])
            domain_name = self._get_mapped_domain(symbol, mapping)
        if not domain_name:
            special_domain_index = -1
            #  symbol.p_linkerSymbol() don't gives expected results (mapfile type 1)
            # TODO verify with both mapfile formats how to handle it
            if not module_name or module_name == "__linker__":
                special_domain_index = 0
            domain_name = self._special_domain_names[
                ProjectConfig._project_special_domains[special_domain_index]
            ]
        return domain_name

    def _scom_mapper(self, name_space, symbol_name):
        """use scom mapping configuration and rules to apply them, ie.
        if symbol is in scom namespace use symbolname for mapping
        else use namespace for mapping
        """
        mapping = []
        if name_space in self._scom_namespace:
            mapping = self._domain_mapper("scom", symbol_name, [])
        elif name_space:
            mapping = self._domain_mapper("scom", name_space, [])
        return mapping

    def _symbol_mapper(self, symbolname, qualified_symbolname):
        mapping = self._domain_mapper("symbols", symbolname, qualified_symbolname)
        return mapping

    def _object_mapper(self, object_filename, qualified_object_filename):
        mapping = self._domain_mapper("objs", object_filename, qualified_object_filename)
        return mapping

    def _library_mapper(self, libraryname, qualified_libraryname):
        mapping = self._domain_mapper("libs", libraryname, qualified_libraryname)
        return mapping

    def _get_mapped_domain(self, symbol, mapping_list):
        """evaluate mapping and store ambiguous mapping
        return domain name of first successful napping
        """
        result = ""
        ml_len = len(mapping_list)
        if ml_len > 0:
            if ml_len > 1:
                self._ambiguous_symbol_mapping.append((symbol, mapping_list))
            result = mapping_list[0].get_domain()
        return result

    def dump(self):
        print(
            "Domain Config name: {0} --- Available Memory Config Name: {1}".format(
                self._config_file_name, self._available_memory_file
            )
        )
        print("Domainlist:\n\t{0}".format("\n\t".join(self._domain_list)))
        print("Available Memory    {0}".format(self._available_memory))
        print("Global Budget       {0}".format(self._global_budget))
        print("Domain Budget Sum   {0}".format(self._domain_budget_sum))
        print("SCOM namespace      {0}".format(self._scom_namespace))
        print("SCOM objectfile      {0}".format(self._scom_objectfile))
        for domain in self._domain_list:
            print("{0}".format(self._domain_data[domain]))
        print("DOMAIN MAPPER:\n{0}".format(self._domain_mapper))

    def init(self):
        self._init_available_memory()
        self._init_global_and_domain_config()
        self._domain_list.sort()
        for domain in ProjectConfig._project_special_domains:
            self._domain_list.append(self._special_domain_names[domain])
        self._calc_domain_budget_sum()
        self._init_domain_mapper()

    def _init_available_memory(self):
        """parse available memory config file to set project available memory"""
        try:
            evaluated_lines = 0
            ifh = open(self._available_memory_file, "r")
            for line in ifh:
                if line.startswith("# Ignore Sections"):
                    break
                if line.startswith("#") or line == "":
                    continue
                mem_config_match = re.match(
                    r"^\s*(?:.+)\s*,\s*(?:.+)\s*,\s*(.+)\s*,\s*(RAM|ROM)\s*#?.*$", line
                )
                if mem_config_match:
                    evaluated_lines += 1
                    mem_size = mem_config_match.group(1)
                    mem_type = mem_config_match.group(2)
                    if mem_type.upper() == "ROM":
                        self._available_memory["rom"] += int(mem_size, 16)
                    elif mem_type.upper() == "RAM":
                        self._available_memory["ram"] += int(mem_size, 16)
                    else:
                        raise ProjectConfigError(
                            "could not identify memory type(RAM/ROM) in line:\n\t{0}".format(line)
                        )
            ifh.close()
        except OSError as exc:
            raise ProjectConfigError(
                "failed to open or config file '{0}' ... {1}".format(self._config_file_name, exc)
            )
        if evaluated_lines == 0:
            raise ProjectConfigError(
                "could not read available memory data from file {0}".format(
                    self._available_memory_file
                )
            )

    def _init_global_and_domain_config(self):
        """parse bugdet and domain mapping configuration"""
        try:
            jfh = open(self._config_file_name, "r")
            json_config = json.load(jfh)
            jfh.close()
        except OSError as exc:
            raise ProjectConfigError(
                "failed to open or config file '{0}' ... {1}".format(self._config_file_name, exc)
            )
        except json.JSONDecodeError as exc:
            raise ProjectConfigError(
                "error parsing json file '{0}' ... {1}".format(self._config_file_name, exc)
            )
        try:
            self._init_global_config(json_config["Global"])
            self._init_domain_config(json_config["Domains"])
        except KeyError as exc:
            raise ProjectConfigError('missing mandatory configuration item "{0}"'.format(exc))

    def _init_global_config(self, global_config_data):
        """parse 'Global' configuration: project budget
        conditional: LINKER, NODOMONAIN
        conditional: scom namespace [] and scom object file []
        """
        for res in ProjectConfig._resources:
            self._global_budget[res] = global_config_data[res]
        for special_domain_name in ProjectConfig._project_special_domains:
            special_domain = DomainConfig(special_domain_name)
            if special_domain_name in global_config_data:
                special_domain.parse_config(
                    global_config_data[special_domain_name],
                    ProjectConfig._domain_mapper_order,
                )
            else:
                special_domain.parse_config(
                    ProjectConfig._default_domain_config,
                    ProjectConfig._domain_mapper_order,
                )
            self._add_domain(special_domain)
            self._special_domain_names[special_domain_name] = special_domain.get_name()
        if "scom_config" in global_config_data:
            if "namespace" in global_config_data["scom_config"]:
                self._scom_namespace = [x for x in global_config_data["scom_config"]["namespace"]]
            if "objectfile" in global_config_data["scom_config"]:
                self._scom_objectfile = [x for x in global_config_data["scom_config"]["objectfile"]]
                self._p_qualified_scom_objectfile = False
                if "(" in self._scom_objectfile[0]:
                    self._p_qualified_scom_objectfile = True

    def _init_domain_config(self, domain_cfg_list):
        """parse 'Domains' configuration - per domain
        name and budget
        contionally mapping defintions
        """
        for domain_cfg in domain_cfg_list:
            try:
                domain_name = domain_cfg["name"]
                domain = DomainConfig(domain_name)
                try:
                    domain.parse_config(domain_cfg, ProjectConfig._domain_mapper_order)
                except DomainConfigError as exc:
                    raise ProjectConfigError(
                        'failed to parse domain "{0}" config data'.format(domain_name)
                    )
                self._add_domain(domain, domain_name)
                self._domain_list.append(domain_name)
            except KeyError as exc:
                raise ProjectConfigError('missing mandatory configuration item "{0}"'.format(exc))

    def _add_domain(self, domain, domain_name=None):
        """add domain cfg to project cfg - raise an error domain is configured more than once"""
        if domain_name is None:
            domain_name = domain.get_name()
        if domain_name in self._domain_data:
            raise ProjectConfigError('domain "{0}" already configured'.format(domain_name))
        self._domain_data[domain_name] = domain

    def _init_domain_mapper(self):
        """for each domain add mapping definitions to project domain mapper."""
        for domain in self._domain_list:
            for mapper in ProjectConfig._domain_mapper_order:
                try:
                    for mapper_def in self._domain_data[domain].get_mapper_config(mapper):
                        self._domain_mapper.add_mapper_defintion(domain, mapper, mapper_def)
                except KeyError as exc:
                    raise ProjectConfigError(
                        "domain not properly configured "
                        + "{0} missing required domain mapping entry{1}".format(domain, exc)
                    )

    def _calc_domain_budget_sum(self):
        """sum up budget of all domains"""
        for domain in self._domain_list:
            self._domain_budget_sum += self._domain_data[domain].get_budget()

    def get_domain_mapper(self):
        return self._domain_mapper

    def get_config_filename(self):
        return self._config_file_name

    def get_available_memory(self):
        return self._available_memory

    def get_project_budget(self):
        return self._global_budget

    def get_domain_budget_sum(self):
        return self._domain_budget_sum

    def get_domain_budget(self, domain_name):
        """return domain specific budget"""
        try:
            return self._domain_data[domain_name].get_budget()
        except KeyError:
            raise ProjectConfigError("unknown domain {0}".format(domain_name))

    def get_domain_list(self):
        return self._domain_list


def testmain():
    config = get_project_configuration(sys.argv[1], sys.argv[2])
    config.dump()
    print(
        "CHECK Global Budget {0}\n Available Memory{1}\n\t--> {2}".format(
            config.get_project_budget(),
            config.get_available_memory(),
            (config.get_project_budget() > config.get_available_memory()),
        )
    )
    print(
        "CHECK Domain_budget_sum {0}\n Global Budget{1}\n\t--> {2}".format(
            config.get_domain_budget_sum(),
            config.get_project_budget(),
            (config.get_domain_budget_sum() > config.get_project_budget()),
        )
    )
    print(
        "CHECK Global Budget {0}\n Domain_budget_sum{1}\n\t--> {2}".format(
            config.get_project_budget(),
            config.get_domain_budget_sum(),
            (config.get_project_budget() > config.get_domain_budget_sum()),
        )
    )
    print(
        "get_symbol_domain ... {0}".format(
            config.map_symbol_into_domain(
                CSymbolStub("libscom.a", "scom.o", "scom", "g_jupp_nase"),
                "scom",
                "g_jupp_nase",
                "scom.o",
                "libmain_x.a",
            )
        )
    )
    print(
        "get_symbol_domain ... {0}  ".format(
            config.map_symbol_into_domain(
                CSymbolStub("libscom.a", "scom.o", "scom", "g_jupp_nase"),
                "scom",
                "g_FsiCd_",
                "scom.o",
                "libmain_x.a",
            )
        )
    )
    # print("{0}".format(config.get_unused_domain_mapping()))
    print("{0}".format("\n".join([str(x) for x in config.get_unmapped_scom_symbols()])))
    print(
        "ProjectConfig.get_memory_resource({0}) -> {1}".format(
            "EMEM0_NC", ProjectConfig.get_memory_resource("EMEM0_NC")
        )
    )
    print("default_mapped_resource {0}".format(ProjectConfig.get_default_mapped_resource()))
    print(
        "get_errored_mapped_memory_name {0}".format(ProjectConfig.get_errored_mapped_memory_name())
    )


class CSymbolStub:
    # Disable Pylint check for naming conventions since stub has to use names of stubbed class
    # pylint: disable=invalid-name
    def __init__(self, library, objectfile, namespace, name):
        self._library = library
        self._objectfile = objectfile
        self._namespace = namespace
        self._name = name

    def getName(self):
        return self._name

    def getNamespace(self):
        return self._namespace

    def getModule(self):
        return self._objectfile

    def getLibrary(self):
        return self._library

    def p_linkerSymbol(self):
        return not (self._library or self._objectfile)

    def __str__(self):
        return "SYMBOLSTUB({4}) - namespace: {0} name: {1} object: {2} library: {3}".format(
            self._namespace,
            self._name,
            self._objectfile,
            self._library,
            int(self.p_linkerSymbol()),
        )


if __name__ == "__main__":
    testmain()
