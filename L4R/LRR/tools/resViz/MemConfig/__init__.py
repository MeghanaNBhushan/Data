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
#  @brief : dispatch MapConfig
#  @state : waiting for cleanup 
#=============================================================================


import os
import sys

class MemConfigFError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message

def MemConfig(type='BUILTIN',**taggedValues):
    if type.upper() == 'BUILTIN':
        controller = ''
        if 'controller' in taggedValues:
            controller = taggedValues['controller']
        if controller.upper().startswith('TC_'):
            from TriCoreMemConfig import CMemConfig
            return CMemConfig(controller)
        else:
            raise MemConfigFError('no builtin memconfig for controller {0}'.format(controller))
    elif type.upper() == 'CUSTOM':
        cfgFile = os.path.join(os.path.dirname(__file__),'tc_default_mcfg.json')
        if 'cfgfile' in taggedValues:
            cfgFile = taggedValues['cfgfile']
        from CustomMemconfig import CMemConfig
        return CMemConfig(cfgFile)
    else:
        raise MemConfigFError('unsupported memconfig type {0}'.format(type))

sys.path.append( os.path.dirname(__file__))

