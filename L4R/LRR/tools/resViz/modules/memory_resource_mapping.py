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
#  @brief : map named to accounted resource - currently not used
#
# =============================================================================


class MemoryResourceMapper:
    _memory_resource_mapping = {
        "CPU0_DataSratchPad": "ram",
        "CPU0_DataCache": "ram",
        "CPU0_DataCacheTag": "ram",
        "CPU0_PrgSratchPad": "ram",
        "CPU0_PrgCache": "ram",
        "CPU0_PrgCacheTag": "ram",
        "CPU1_DataSratchPad": "ram",
        "CPU1_DataCache": "ram",
        "CPU1_DataCacheTag": "ram",
        "CPU1_PrgSratchPad": "ram",
        "CPU1_PrgCache": "ram",
        "CPU1_PrgCacheTag": "ram",
        "CPU2_DataSratchPad": "ram",
        "CPU2_DataCache": "ram",
        "CPU2_DataCacheTag": "ram",
        "CPU2_PrgSratchPad": "ram",
        "CPU2_PrgCache": "ram",
        "CPU2_PrgCacheTag": "ram",
        "CPU3_DataSratchPad": "ram",
        "CPU3_DataCache": "ram",
        "CPU3_DataCacheTag": "ram",
        "CPU3_PrgSratchPad": "ram",
        "CPU3_PrgCache": "ram",
        "CPU3_PrgCacheTag": "ram",
        "CPU4_DataSratchPad": "ram",
        "CPU4_DataCache": "ram",
        "CPU4_DataCacheTag": "ram",
        "CPU4_PrgSratchPad": "ram",
        "CPU4_PrgCache": "ram",
        "CPU4_PrgCacheTag": "ram",
        "CPU5_DataSratchPad": "ram",
        "CPU5_DataCache": "ram",
        "CPU5_DataCacheTag": "ram",
        "CPU5_PrgSratchPad": "ram",
        "CPU5_PrgCache": "ram",
        "CPU5_PrgCacheTag": "ram",
        "PFI0": "rom",
        "PFI1": "rom",
        "PFI2": "rom",
        "PFI3": "rom",
        "PFI4": "rom",
        "PFI5": "rom",
        "PFI0_NC": "rom",
        "PFI1_NC": "rom",
        "PFI2_NC": "rom",
        "PFI3_NC": "rom",
        "PFI4_NC": "rom",
        "PFI5_NC": "rom",
        "CPU0_DLMU_RAM": "ram",
        "CPU1_DLMU_RAM": "ram",
        "CPU2_DLMU_RAM": "ram",
        "CPU3_DLMU_RAM": "ram",
        "LMU0_RAM": "ram",
        "LMU1_RAM": "ram",
        "LMU2_RAM": "ram",
        "CPU4_DLMU_RAM": "ram",
        "CPU5_DLMU_RAM": "ram",
        "DAM0": "ram",
        "DAM1": "ram",
        "EMEM0": "ram",
        "EMEM1": "ram",
        "EMEM2": "ram",
        "EMEM3": "ram",
        "CPU0_DLMU_RAM_NC": "ram",
        "CPU1_DLMU_RAM_NC": "ram",
        "CPU2_DLMU_RAM_NC": "ram",
        "CPU3_DLMU_RAM_NC": "ram",
        "LMU0_RAM_NC": "ram",
        "LMU1_RAM_NC": "ram",
        "LMU2_RAM_NC": "ram",
        "CPU4_DLMU_RAM_NC": "ram",
        "CPU5_DLMU_RAM_NC": "ram",
        "DAM0_NC": "ram",
        "DAM1_NC": "ram",
        "EMEM0_NC": "ram",
        "EMEM1_NC": "ram",
        "EMEM2_NC": "ram",
        "EMEM3_NC": "ram",
    }

    @classmethod
    def get_resource_list(cls):
        return sorted(set(cls._memory_resource_mapping.values()))

    @classmethod
    def get_resource_mapped_memory(cls):
        resource_mapped_memory = {}
        for memory_name in cls._memory_resource_mapping:
            resource = cls._memory_resource_mapping[memory_name]
            if resource not in resource_mapped_memory:
                resource_mapped_memory[resource] = []
            resource_mapped_memory[resource].append(memory_name)
        return resource_mapped_memory

    @classmethod
    def get_memory_resource(cls, memory_name):
        return cls._memory_resource_mapping[memory_name]

    @classmethod
    def get_default_mapped_resource(cls):
        return "rom"
