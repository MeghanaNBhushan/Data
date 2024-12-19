#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
#  @copyright (c) 2019 - 2020 by Robert Bosch GmbH. All rights reserved.
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
#  @brief : commonly used utilities
#  @status: waiting for becoming more
#=============================================================================

import re

def getSource(sourceStr):
    lib = None
    module = None
    linkersym = False
    source = sourceStr
    sourceMatch = re.match(r'^([^\(\)]+)\(([^\(\)]+)\)',sourceStr)
    if sourceMatch:
        lib = sourceMatch.group(1)
        module = sourceMatch.group(2)
    elif re.search(r'\.o(bj)?$',source):
        module = source
    else:
        linkersym = True
    return lib,module,linkersym,source
