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
#  Projectname            : Build Tool Chain
# =============================================================================
#  F I L E   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  @brief         : Writes the output of resViz tool to an excel sheet
#
# =============================================================================


import xlsxwriter


class OutputWriter:
    def __init__(self, output_file):
        self._output_file = output_file

    def write_xlsx(self, resource_data, memory_block_data):
        """Writes output to an excel sheet"""
        workbook = xlsxwriter.Workbook(self._output_file)

        self._write_domain_sheet(workbook, resource_data)
        self._write_symbol_sheet(workbook, resource_data)
        self._write_lib_sheet(workbook, resource_data)
        self._write_object_sheet(workbook, resource_data)
        self._write_memrange_use(workbook, memory_block_data)

        workbook.close()

    def _write_domain_sheet(self, workbook, resource_data):
        """Creates worksheet with domain specific memory usage"""
        cell_format_red = workbook.add_format({"bg_color": "red"})
        domain_list = resource_data.get_domain_list()
        ### Write domains down ###
        worksheet_domains = workbook.add_worksheet("Domains")
        worksheet_domains.conditional_format(
            1,
            3,
            len(domain_list) + 2,
            3,
            {"type": "cell", "criteria": ">", "value": 100, "format": cell_format_red},
        )
        worksheet_domains.conditional_format(
            1,
            7,
            len(domain_list) + 2,
            7,
            {"type": "cell", "criteria": ">", "value": 100, "format": cell_format_red},
        )
        worksheet_domains.write(0, 0, "Domain")
        worksheet_domains.write(0, 1, "ROM Budget")
        worksheet_domains.write(0, 2, "ROM Usage")
        # add data bars to usage
        worksheet_domains.conditional_format(1, 2, len(domain_list), 2, {"type": "data_bar"})
        worksheet_domains.write(0, 3, "ROM Quota")
        worksheet_domains.write(0, 4, "ROM free")
        worksheet_domains.write(0, 5, "RAM Budget")
        worksheet_domains.write(0, 6, "RAM Usage")
        # add data bars to usage
        worksheet_domains.conditional_format(1, 6, len(domain_list), 6, {"type": "data_bar"})
        worksheet_domains.write(0, 7, "RAM Quota")
        worksheet_domains.write(0, 8, "RAM free")
        # Add auto filter
        worksheet_domains.autofilter(0, 0, 0, 8)
        # Set width for column 0 to 30
        worksheet_domains.set_column(0, 0, 30)
        # Set width for column 1 till 6 to 15
        worksheet_domains.set_column(1, 8, 15)
        row = 1
        for domain in domain_list:
            row = self._write_budget(worksheet_domains, row, resource_data, domain)

        # keep one line free
        row += 1

        ### Write sums down ###
        available_memory = resource_data.get_project_available_memory()
        project_budget = resource_data.get_project_budget()
        domain_budget_sum = resource_data.get_project_domain_budget_sum()
        domain_account_sum = resource_data.get_domain_account_sum()

        row = self._write_summary_budget(
            worksheet_domains, row, "Available Memory (AM)", available_memory
        )
        row = self._write_summary_budget(
            worksheet_domains, row, "Global Budget (GB)", project_budget
        )
        row = self._write_summary_budget(
            worksheet_domains, row, "Sum of Domain Budgets (DB)", domain_budget_sum
        )
        row = self._write_summary_budget(
            worksheet_domains, row, "Sum of Used Memory (UM)", domain_account_sum
        )

        # Red field if more than 100% is used for ROM and RAM (column 3 and 6)
        worksheet_domains.conditional_format(
            row,
            3,
            row + 3,
            3,
            {"type": "cell", "criteria": ">", "value": 100, "format": cell_format_red},
        )
        worksheet_domains.conditional_format(
            row,
            7,
            row + 3,
            7,
            {"type": "cell", "criteria": ">", "value": 100, "format": cell_format_red},
        )
        row = self._write_summary_usage(
            worksheet_domains,
            row,
            "GB of AM",
            project_budget,
            available_memory,
        )

        row = self._write_summary_usage(
            worksheet_domains,
            row,
            "UM of AM",
            domain_account_sum,
            available_memory,
        )
        row = self._write_summary_usage(
            worksheet_domains,
            row,
            "DB of GB",
            domain_budget_sum,
            project_budget,
        )
        row = self._write_summary_usage(
            worksheet_domains,
            row,
            "UM of GB",
            domain_account_sum,
            project_budget,
        )

    def _write_budget(self, worksheet, row, resource_data, domain):
        """Writes memory usage for one domain to domain sheet"""
        budget = resource_data.get_domain_budget(domain)
        account = resource_data.get_domain_account(domain)
        worksheet.write(row, 0, domain)
        worksheet.write(row, 1, budget["rom"])
        worksheet.write(row, 2, account["rom"])
        if budget["rom"] == 0:
            quota = "infinity"
        else:
            quota = self._normalize_percentage(account["rom"] / budget["rom"] * 100, 2)
        worksheet.write(row, 3, quota)
        worksheet.write(row, 4, budget["rom"] - account["rom"])
        worksheet.write(row, 5, budget["ram"])
        worksheet.write(row, 6, account["ram"])
        if budget["ram"] == 0:
            quota = "infinity"
        else:
            quota = self._normalize_percentage(account["ram"] / budget["ram"] * 100, 2)
        worksheet.write(row, 7, quota)
        worksheet.write(row, 8, budget["ram"] - account["ram"])
        return row + 1

    def _write_summary_budget(self, worksheet, row, name, data):
        """Writes sum of memory budgets to domain sheet"""
        worksheet.write(row, 0, name)
        worksheet.write(row, 1, data["rom"])
        worksheet.write(row, 5, data["ram"])
        return row + 1

    def _write_summary_usage(self, worksheet, row, name, account, budget):
        """"Writes sum of used memory to domain sheet"""
        worksheet.write(row, 0, name)
        worksheet.write(row, 1, budget["rom"])
        worksheet.write(row, 2, account["rom"])
        worksheet.write(row, 3, self._normalize_percentage(account["rom"] / budget["rom"] * 100, 2))
        worksheet.write(row, 4, budget["rom"] - account["rom"])
        worksheet.write(row, 5, budget["ram"])
        worksheet.write(row, 6, account["ram"])
        worksheet.write(row, 7, self._normalize_percentage(account["ram"] / budget["ram"] * 100, 2))
        worksheet.write(row, 8, budget["ram"] - account["ram"])
        return row + 1

    def _write_symbol_sheet(self, workbook, resource_data):
        """Creates worksheet with memory usage of symbols"""
        # Worksheet with libs and object files
        worksheet = workbook.add_worksheet("Symbols")
        worksheet.write(0, 0, "Domain")
        worksheet.write(0, 1, "Library")
        worksheet.write(0, 2, "Object File")
        worksheet.write(0, 3, "Symbol")
        worksheet.write(0, 4, "Symbol (demagled)")
        worksheet.write(0, 5, "Section")
        worksheet.write(0, 6, "ROM")
        worksheet.write(0, 7, "RAM")
        worksheet.write(0, 8, "PhysMem")
        worksheet.write(0, 9, "LoadMem")
        worksheet.autofilter(0, 0, 0, 9)  # Add auto filter
        worksheet.set_column(0, 5, 20)  # Set width for column 1 and 2 to 20
        row = 1
        for symbol in resource_data.get_symbol_list():
            symbol_account = symbol["account"]
            if symbol_account["ram"] > 0 or symbol_account["rom"] > 0:
                row = self._write_symbol(worksheet, row, symbol)

    def _write_symbol(self, worksheet, row, symbol):
        """Writes memory usage of one symbol to Symbols sheet"""
        worksheet.write(row, 0, symbol["domain"])
        worksheet.write(row, 1, symbol["library"])
        worksheet.write(row, 2, symbol["object"])
        worksheet.write(row, 3, symbol["name"])
        worksheet.write(row, 4, symbol["decodedname"])
        worksheet.write(row, 5, symbol["outputsection"])
        account = symbol["account"]
        memoryname = symbol["memoryname"]
        if account["rom"] > 0:
            worksheet.write(row, 6, account["rom"])
            if account["ram"] > 0:
                worksheet.write(row, 9, memoryname["rom"])
            else:
                worksheet.write(row, 8, memoryname["rom"])
        if account["ram"] > 0:
            worksheet.write(row, 7, account["ram"])
            worksheet.write(row, 8, memoryname["ram"])
        return row + 1

    def _write_lib_sheet(self, workbook, resource_data):
        """Creates worksheet with memory usage of libraries"""
        worksheet = workbook.add_worksheet("Libraries")
        worksheet.write(0, 0, "Library")
        worksheet.write(0, 1, "ROM")
        worksheet.write(0, 2, "RAM")
        worksheet.autofilter(0, 0, 0, 2)  # Add auto filter
        worksheet.set_column(0, 0, 20)  # Set width for column 1 and 2 to 20
        row = 1
        for lib in resource_data.get_library_list():
            row = self._write_library(worksheet, row, resource_data.get_library_data(lib))

    def _write_library(self, worksheet, row, lib):
        """Writes memory usage of one library to Libraries sheet"""
        worksheet.write(row, 0, lib["libraryname"])
        worksheet.write(row, 1, lib["account"]["rom"])
        worksheet.write(row, 2, lib["account"]["ram"])
        return row + 1

    def _write_object_sheet(self, workbook, resource_data):
        """Creates worksheet with memory usage of objects"""
        worksheet = workbook.add_worksheet("Objects")
        phys_mem_name_by_resource = resource_data.get_resource_named_memory_blocks()
        row = 0
        worksheet.write(row, 0, "Object File")
        worksheet.write(row, 1, "Library")
        worksheet.set_column(row, 1, 20)  # Set width for column 1 and 2 to 20
        column = 2
        resource_list = ["rom", "ram"]
        for resource in resource_list:
            for name_memory in phys_mem_name_by_resource[resource]:
                worksheet.write(row, column, name_memory)
                column += 1
            worksheet.write(row, column, resource.upper())
            column += 1
        row = 1
        for obj in resource_data.get_object_list():
            row = self._write_object_file(
                worksheet,
                row,
                resource_data.get_object_data(obj),
                resource_list,
                phys_mem_name_by_resource,
            )

    def _write_object_file(
        self, worksheet, row, object_file, resource_list, name_memory_by_resource
    ):
        """Writes memory usage of one object file to Objects sheet"""
        worksheet.write(row, 0, object_file["objectname"])
        worksheet.write(row, 1, object_file["libraryname"])
        column = 2
        for resource in resource_list:
            for name_memory in name_memory_by_resource[resource]:
                worksheet.write(row, column, object_file["named_memory"][name_memory])
                column += 1
            worksheet.write(row, column, object_file["account"][resource])
            column += 1
        return row + 1

    def _write_memrange_use(self, workbook, memrange_data):
        """Creates worksheet with memory usage in different memory sections"""
        worksheet_memrange_use = workbook.add_worksheet("Memory Use")
        worksheet_memrange_use.write(0, 0, "Name")
        worksheet_memrange_use.write(0, 1, "Address")
        worksheet_memrange_use.write(0, 2, "Size")
        worksheet_memrange_use.write(0, 3, "Used")
        worksheet_memrange_use.write(0, 4, "Used [%]")
        worksheet_memrange_use.write(0, 5, "Free")
        worksheet_memrange_use.write(0, 6, "Free [%]")
        row_count = 1
        mem_index = sorted(memrange_data)
        for mem_id in mem_index:
            size = memrange_data[mem_id]["size"]
            used = memrange_data[mem_id]["used"]
            used_percent = self._normalize_percentage(used * 100 / size, 2)
            free = size - used
            free_percent = self._normalize_percentage(free * 100 / size, 2)
            worksheet_memrange_use.write(row_count, 0, memrange_data[mem_id]["name"])
            worksheet_memrange_use.write(row_count, 1, hex(memrange_data[mem_id]["startAddress"]))
            worksheet_memrange_use.write(row_count, 2, size)
            worksheet_memrange_use.write(row_count, 3, used)
            worksheet_memrange_use.write(row_count, 4, used_percent)
            worksheet_memrange_use.write(row_count, 5, free)
            worksheet_memrange_use.write(row_count, 6, free_percent)
            row_count += 1

    def _normalize_percentage(self, percentage, decimals):
        return int(percentage * 10 ** decimals) / 10 ** decimals

    # how is excel representing inf?
    @classmethod
    def normalize_percentage_1(cls, act_value, ref_value):
        if ref_value == 0:
            val = "inf"
            if act_value < 0:
                val = "-inf"
        else:
            val = "{0:.2f}".format(act_value * 100 / ref_value)
        return float(val)
