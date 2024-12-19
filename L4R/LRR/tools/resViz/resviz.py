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
#  @brief : resViz applicatation entry point
# =============================================================================

import os
import sys
import yaml

from MapReader import MapReader, MapReaderError
from MemConfig import MemConfig, MemConfigFError
from Demangler import Demangler, DemanglerFError
from LDReader import LDReader, LDReaderError

sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

from resviz_options import get_resviz_options
from modules.project_config import get_project_configuration, DomainConfigError
from project_resource_account import ProjectResourceAccount
from symbol_resource import get_symbol_resource
from output_writer import OutputWriter
from logger import Logger


class ResvizError(Exception):
    """ ResViz Application Exception """

    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __str__(self):
        return self._msg


def get_used_controller_memory_blocks(controller_memory_cfg, output_section_list, config):
    """
    find controller memory blocks used by current application - setup filter in object file sheet
    for this purpose investigate linker output sections having size > 0
    """
    physical_memory = {}
    temp = {}
    missing_rom_copy = []
    for output_section in output_section_list:
        output_section_size = output_section.getSize()
        if output_section_size > 0:
            output_section_address = output_section.getAddress()
            memory_id = controller_memory_cfg.getMemRangeId(output_section_address)
            output_section_memory_type = output_section.getMemType()
            if output_section_memory_type not in physical_memory:
                physical_memory[output_section_memory_type] = []
                temp[output_section_memory_type] = []
            if memory_id not in temp[output_section_memory_type]:
                temp[output_section_memory_type].append(memory_id)
            if output_section_memory_type == "RAM":
                if output_section.getSectionType() in ["data", "text"]:
                    if output_section.getRomCopySectionMemName(None) is None:
                        missing_rom_copy.append(memory_id)
    for key in temp:
        physical_memory[key] = [controller_memory_cfg.getMemName(x) for x in sorted(temp[key])]
    if missing_rom_copy:
        missing_mapped_memory = config.get_errored_mapped_memory_name()
        physical_memory["FLASH"].append(missing_mapped_memory)
    return physical_memory


def get_physical_memory_block_use(controller_memory_cfg, output_section_list):
    """for each of the used memory blocks calculate the size of used memory."""
    physical_memory_block_use = {}
    for output_section in output_section_list:
        output_section_size = output_section.getSize()
        if output_section_size > 0:
            output_section_address = output_section.getAddress()
            memory_range_id = controller_memory_cfg.getMemRangeId(output_section_address)
            memory_range = controller_memory_cfg.getMemRangeById(memory_range_id)
            shared_memory_range = memory_range.getSharedBy()
            if shared_memory_range is not None:
                memory_range_id = shared_memory_range
                memory_range = controller_memory_cfg.getMemRangeById(memory_range_id)
            physical_memory_block_id = memory_range_id
            if physical_memory_block_id not in physical_memory_block_use:
                physical_memory_block_use[physical_memory_block_id] = {
                    "name": memory_range.getName(),
                    "startAddress": memory_range.getStartAddress(),
                    "size": memory_range.getSize(),
                    "used": 0,
                }
            physical_memory_block_use[physical_memory_block_id]["used"] += output_section_size
    return physical_memory_block_use


def dump_physical_memory_block_use(physical_memory_block_use):
    """for each of the used memory blocks print the size of used memory (internal purpose)."""
    for physical_memory_block_id in sorted(physical_memory_block_use):
        memory_block_size = physical_memory_block_use[physical_memory_block_id]["size"]
        memory_block_use = physical_memory_block_use[physical_memory_block_id]["used"]
        memory_block_use_use_per_cent = float(
            "{0:.2f}".format(memory_block_use * 100 / memory_block_size)
        )
        memory_block_free = memory_block_size - memory_block_use
        memory_block_freee_per_cent = float(
            "{0:.2f}".format(memory_block_free * 100 / memory_block_size)
        )
        print(
            "{0} - {1} - {2} - {3} - {4} - {5} - {6}".format(
                physical_memory_block_use[physical_memory_block_id]["name"],
                hex(physical_memory_block_use[physical_memory_block_id]["startAddress"]),
                memory_block_size,
                memory_block_use,
                memory_block_use_use_per_cent,
                memory_block_free,
                memory_block_freee_per_cent,
            )
        )


def get_map_filedata(options, controller_memory_cfg):
    """
    parse all configured map files to create
    list of symbols and output sections being input for resource calculation
    """
    demangler_plugin_directory = options.get_compiler_path()
    demangler = None
    if demangler_plugin_directory:
        demangler = Demangler(ghsdir=demangler_plugin_directory)
    else:
        demangler = Demangler()
    demangler.init()
    combinded_symbols_list = []
    combinded_output_section_list = []
    for i in range(options.get_number_of_mapfiles()):
        mapfile, ldfile = options.get_mapfile_data(i)
        mfr = MapReader("GHS", mapfile, controller_memory_cfg, demangler)
        mfr.parse()
        if ldfile is not None:
            ld_reader = LDReader("GHS", ldfile)
            ld_reader.parse()
            mfr.updateRomCopySections(ld_reader.getSectionMap())
        else:
            mfr.updateRomCopySections()
        combinded_symbols_list.extend(mfr.getSymbolList())
        combinded_output_section_list.extend(mfr.getOSectionList())
    return combinded_symbols_list, combinded_output_section_list


def dump_project(project_resource_use):
    """dump project resource consumption in text format (internal purpose)."""
    available_memory = project_resource_use.get_project_available_memory()
    print("AVAILABLE_MEMORY: {0}".format(available_memory))

    project_budget = project_resource_use.get_project_budget()
    print("PROJECT_BUDGET: {0}".format(project_budget))
    print("\tVIOLATION BUDGET vs. AVAILABLE: {0}".format(project_budget > available_memory))

    domain_budget_sum = project_resource_use.get_project_domain_budget_sum()
    print("DOMAIN_BUDGET_SUM: {0}".format(domain_budget_sum))
    print(
        "\tVIOLATION BUDGET_BUDGET_SUM vs. DOMAIN: {0}".format(domain_budget_sum > project_budget)
    )

    domain_account_sum = project_resource_use.get_domain_account_sum()
    print("DOMAIN_ACCOUNT_SUM: {0}".format(domain_account_sum))
    print(
        "\tVIOLATION DOMAIN_ACCOUNT_SUM vs. BUDGET:{0}".format(domain_account_sum > project_budget)
    )

    for domain in project_resource_use.get_domain_list():
        print("###### {0}".format(domain))
        budget = project_resource_use.get_domain_budget(domain)
        print("BUDGET {0}".format(budget))
        account = project_resource_use.get_domain_account(domain)
        print("ACOUNT {0}".format(account))
        cmpresult = account > budget
        if cmpresult:
            print("\tBUDGET_VIOLATION {0}".format(cmpresult))
    for library in project_resource_use.get_library_list():
        libdata = project_resource_use.get_library_data(library)
        libdata.dump()
    for obj in project_resource_use.get_object_list():
        objdata = project_resource_use.get_object_data(obj)
        objdata.dump()
    for symbol in project_resource_use.get_symbol_list():
        symbol.dump()


def generate_budgetviolation_report(report_file, project_resource_use):
    """generate yml formatted domain budget violation report"""
    report_data = []
    domain_list = project_resource_use.get_domain_list()
    for domain in domain_list:
        domain_account = project_resource_use.get_domain_account(domain)
        domain_budget = project_resource_use.get_domain_budget(domain)
        violation_list = domain_account > domain_budget
        if violation_list:
            report = {domain: []}
            for violation in violation_list:
                report[domain].append(
                    {
                        violation.upper(): {
                            "budget": domain_budget[violation],
                            "used": domain_account[violation],
                        }
                    }
                )
            report_data.append(report)
    try:
        report_file_handle = open(report_file, "w")
        report_file_handle.write(yaml.dump(report_data))
        report_file_handle.close()
    except OSError as exc:
        raise ResvizError("Error opening or writing to file {0}\n\t{1}".format(report_file, exc))


def generate_logfile(log_file, project_config, project_resource_use):
    """
    generate log file to contain:
      unused domain mapping
      ambiguous symbol mappings (more than one rule of same level to map a symbol to a domain)
      unmapped scom symbols
    """
    try:
        log_file_handle = open(log_file, "w")

        unused_mapping = project_config.get_unused_domain_mapping()
        count = 0
        exit_state = 0
        for unused_mapping_category in unused_mapping:
            count += len(unused_mapping[unused_mapping_category])
        if count > 0:
            log_file_handle.write("unused domain mapping:\n")
            exit_state = 1
            for unused_mapping_category in unused_mapping:
                if unused_mapping[unused_mapping_category]:
                    log_file_handle.write(
                        "{0}\n".format(
                            "\n".join(
                                [x.log_format() for x in unused_mapping[unused_mapping_category]]
                            )
                        )
                    )

        ambiguous_mapping_list = project_config.get_ambiguous_symbol_mapping()
        if ambiguous_mapping_list:
            log_file_handle.write("\nambiguous mapping for symbols:\n")
            for ambi_symbol in ambiguous_mapping_list:
                log_file_handle.write(
                    "Symbol: {0}\n\t{1}\n".format(
                        ambi_symbol[0].getName(),
                        "\n\t".join([x.log_format() for x in ambi_symbol[1]]),
                    )
                )

        unmapped_symbols_list = project_config.get_unmapped_scom_symbols()
        if unmapped_symbols_list:
            log_file_handle.write("\nunmapped scom symbols:\n")
            for symbol in unmapped_symbols_list:
                log_file_handle.write("[{0}] {1}\n".format(symbol.getNamespace(), symbol.getName()))
        reserved_section_list = project_resource_use.get_reserved_output_sections()
        if reserved_section_list:
            log_file_handle.write(
                "\nlist of section sections reducing available memory resources:\n"
            )
            for reserved_section in reserved_section_list:
                log_file_handle.write(
                    "section: '{0}' resource: '{1}' size: {2}\n".format(
                        reserved_section.getName(),
                        reserved_section.getMemType().lower(),
                        reserved_section.getSize(),
                    )
                )

        log_file_handle.close()
        return exit_state
    except OSError as exc:
        raise ResvizError("Fatal error opening or writing to file {0}\n\t{1}".format(log_file, exc))


def generate_budget_violation_warning(project_resource_use):
    """write budget violation and and degree of use to console"""
    available_memory = project_resource_use.get_project_available_memory()
    project_budget = project_resource_use.get_project_budget()
    domain_budget_sum = project_resource_use.get_project_domain_budget_sum()
    db_of_gb_violation = domain_budget_sum > project_budget
    exit_state = 0 
    if db_of_gb_violation:
        print("Error: Sum of domain budgets is higher than global budget")
        exit_state = 1
    print(
        "Note: {0:.2%} of global ROM budget used for domain budgets".format(
            domain_budget_sum["rom"] / project_budget["rom"]
        )
    )
    print(
        "Note: {0:.2%} of global RAM budget used for domain budgets".format(
            domain_budget_sum["ram"] / project_budget["ram"]
        )
    )
    gb_of_am_violation = project_budget > available_memory
    if gb_of_am_violation:
        print(
            "Error: Global budget is higher than physical budget. ROM: {0}  RAM: {1}".format(
                available_memory["rom"], available_memory["ram"]
            )
        )
        exit_state = 1
    print(
        "Note: {0:.2%} of physical ROM used for global budget".format(
            domain_budget_sum["rom"] / available_memory["rom"]
        )
    )
    print(
        "Note: {0:.2%} of physical RAM used for global budget".format(
            domain_budget_sum["ram"] / available_memory["ram"]
        )
    )
    domain_list = project_resource_use.get_domain_list()
    for domain in domain_list:
        domain_account = project_resource_use.get_domain_account(domain)
        domain_budget = project_resource_use.get_domain_budget(domain)
        violation_list = domain_account > domain_budget
        if violation_list:
            for resource in violation_list:
                print(
                    "Error: Domain '{0}'  is using {1}  byte too much {2}.".format(
                        domain, domain_account[resource] - domain_budget[resource], resource.upper()
                    )
                )
                exit_state = 1
    return exit_state


def main():
    """
    top level control flow of resource calculation
    will call sys.exit(exit_state), ie. set accordlingly to signal errors to calling shell
    """

    if sys.platform.startswith("win"):
        logger = Logger()
        sys.stdout = logger
        sys.stderr = logger

    exit_state = 0
    options = get_resviz_options()
    if options:
        try:
            project_config = get_project_configuration(
                options.get_project_config(), options.get_memory_config()
            )
            controller_memory_cfg = MemConfig(controller="TC_DEFAULT")
            controller_memory_cfg.parse()
            symbols_list, output_section_list = get_map_filedata(options, controller_memory_cfg)
            used_physical_memory_blocks = get_used_controller_memory_blocks(
                controller_memory_cfg, output_section_list, project_config
            )
            physical_memory_block_use = get_physical_memory_block_use(
                controller_memory_cfg, output_section_list
            )
            project_resource_use = ProjectResourceAccount(
                project_config, used_physical_memory_blocks
            )
            project_resource_use.calc_reserved_memory_size(output_section_list)
            for map_symbol in symbols_list:
                resource_symbol = get_symbol_resource(map_symbol, project_config)
                if resource_symbol is not None:
                    project_resource_use.add_symbol_account(resource_symbol)
            project_resource_use.calc_sum_account()
            excel_output_writer = OutputWriter(options.get_output_file())
            excel_output_writer.write_xlsx(project_resource_use, physical_memory_block_use)
            budget_violation_report = options.get_budgetviolationreport()
            if budget_violation_report:
                generate_budgetviolation_report(budget_violation_report, project_resource_use)
            logfile = options.get_logfile()
            if logfile:
                exit_state += generate_logfile(logfile, project_config, project_resource_use)
            exit_state += generate_budget_violation_warning(project_resource_use)
        except DomainConfigError as exc:
            print("Fatal error parsing configuration files\n{0}".format(exc))
            exit_state += 1
        except MapReaderError as exc:
            print("Fatal error parsing map files\n{0}".format(exc))
            exit_state += 1
        except DemanglerFError as exc:
            print("Fatal error setting up Demangler module\n{0}".format(exc))
            exit_state += 1
        except MemConfigFError as exc:
            print("Fatal error parsing memory config\n{0}".format(exc))
            exit_state += 1
        except LDReaderError as exc:
            print("Fatal error parsing linker script\n{0}".format(exc))
            exit_state += 1
        except ResvizError as exc:
            print("Fatal error creating resViz output\n{0}".format(exc))
            exit_state += 1
    else:
        exit_state += 1
    sys.exit(exit_state)


if __name__ == "__main__":
    main()
