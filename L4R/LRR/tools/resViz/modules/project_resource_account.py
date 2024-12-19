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
#  @brief : project resoutce account - store symbols derived resource usage
#           on different aggregation levels - domain, library, object and
#           symbol itself
#           provide interface to configuration data
# =============================================================================


from budget import Budget as Account


class ContainerAccount:
    def __init__(self, object_name, library_name, named_memory_list, kind):
        self._object_name = object_name
        self._library_name = library_name
        self._account = Account()
        self._kind = kind
        self._name_memory_use = {}
        for named_memory in named_memory_list:
            self._name_memory_use[named_memory] = 0

    def add_symbol_accout(self, symbol):
        self._account += symbol["account"]
        for resource in symbol["account"].keys():
            if resource in symbol["memoryname"]:
                self._name_memory_use[symbol["memoryname"][resource]] += symbol["account"][resource]

    def __getitem__(self, item):
        if item == "account":
            return self._account
        elif item == "named_memory":
            return self._name_memory_use
        elif item == "libraryname":
            return self._library_name
        elif item == "objectname":
            return self._object_name
        elif item == "named_memory":
            return self._name_memory_use
        else:
            raise KeyError(item)

    def dump(self):
        if self._kind == "library":
            print(
                "CONTAINER {0}  {1} ... {2}".format(self._kind, self._library_name, self._account)
            )
        elif self._kind == "object":
            print(
                "CONTAINER {0}  {1} ... {2}({3})".format(
                    self._kind, self._library_name, self._object_name, self._account
                )
            )
        print("\t{0}".format(self._name_memory_use))


class ProjectResourceAccount:
    def __init__(self, project_config, named_memory_data):
        self._project_config = project_config
        self._named_memory_list = []
        for kind in named_memory_data:
            self._named_memory_list.extend(named_memory_data[kind])
        temp = project_config.get_resource_mapped_memory()
        self._resource_named_memory_blocks = {}
        for resource in temp:
            self._resource_named_memory_blocks[resource] = []
        for name in self._named_memory_list:
            for resource in temp:
                if name in temp[resource]:
                    self._resource_named_memory_blocks[resource].append(name)
                    break
        self._domain_account_sum = Account()
        self._domain_account = {}
        for domain in project_config.get_domain_list():
            self._domain_account[domain] = Account()
        self._library_account = {}
        self._library_account_sum = Account()
        self._object_account = {}
        self._object_account_sum = Account()
        self._symbols = []
        self._symbol_account_sum = Account()
        self._reserved_memory = Account()
        self._reserved_output_sections = []

    def add_symbol_account(self, resource_symbol):
        account = resource_symbol["account"]
        domain = resource_symbol["domain"]
        self._domain_account[domain] += account
        library_name = resource_symbol["library"]
        object_name = resource_symbol["object"]
        if library_name not in self._library_account:
            self._library_account[library_name] = ContainerAccount(
                object_name, library_name, self._named_memory_list, "library"
            )
        self._library_account[library_name].add_symbol_accout(resource_symbol)
        qualifiedobject = resource_symbol["qualifiedobject"]
        if qualifiedobject not in self._object_account:
            self._object_account[qualifiedobject] = ContainerAccount(
                object_name, library_name, self._named_memory_list, "object"
            )
        self._object_account[qualifiedobject].add_symbol_accout(resource_symbol)
        self._symbols.append(resource_symbol)
        self._symbol_account_sum += account

    def calc_sum_account(self):
        for domain in self._domain_account:
            self._domain_account_sum += self._domain_account[domain]
        for library in self._library_account:
            self._library_account_sum += self._library_account[library]["account"]
        for obj in self._object_account:
            self._object_account_sum += self._object_account[obj]["account"]

    def calc_reserved_memory_size(self, output_section_list):
        """
        sum up size of reserved linker output sections.
        Currently section defined in linker script without allocated
        input sections having size > 0. u/i - stack, csa ...
        """
        for output_section in output_section_list:
            size = output_section.getSize()
            if size > 0 and not output_section.p_used():
                if output_section.getMemType().lower() == "ram":
                    self._reserved_memory["ram"] += size
                    self._reserved_output_sections.append(output_section)

    ### name_memory
    def get_resource_named_memory_blocks(self):
        return self._resource_named_memory_blocks

    ### library
    def get_library_list(self):
        return sorted(list(self._library_account.keys()))

    def get_library_data(self, library):
        return self._library_account[library]

    def get_library_account_sum(self):
        return self._library_account_sum

    #### object
    def get_object_list(self):
        return sorted(list(self._object_account.keys()))

    def get_object_data(self, object_file):
        return self._object_account[object_file]

    def get_object_account_sum(self):
        return self._object_account_sum

    def get_symbol_list(self):
        return self._symbols

    def get_symbol_account(self, symbol):
        return symbol["account"]

    def get_symbol_account_sum(self):
        return self._symbol_account_sum

    def get_domain_list(self):
        return self._project_config.get_domain_list()

    def get_domain_budget(self, domain):
        return self._project_config.get_domain_budget(domain)

    def get_domain_account(self, domain):
        return self._domain_account[domain]

    def get_project_budget(self):
        return self._project_config.get_project_budget()

    def get_project_available_memory(self):
        return self._project_config.get_available_memory() - self._reserved_memory

    def get_project_domain_budget_sum(self):
        return self._project_config.get_domain_budget_sum()

    def get_domain_account_sum(self):
        return self._domain_account_sum

    def get_reserved_output_sections(self):
        return self._reserved_output_sections
