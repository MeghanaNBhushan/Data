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
#  @brief : dispatch MapReader
#  @state : waiting for cleanup 
#=============================================================================


import sys
import os

class DemanglerFError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message

def Demangler(compiler='GHS',**taggedValues):
    if compiler.upper() == 'GHS':
        if 'demangleDll' in taggedValues:
            demangleDll = taggedValues['demangleDll']
            if os.path.isfile(demangleDll):
                from GHS_Demangler import CDllDemangler
                return CDemangler(demangleDll)
            else:
                raise DemanglerFError('no such file {0}'.format(demangleDll))
        elif 'ghsdir' in taggedValues:
            demangleDll = os.path.join(taggedValues['ghsdir'],'demangle_ghs.so')
            if os.path.isfile(demangleDll):
                from GHS_Demangler import CDllDemangler
                return CDllDemangler(demangleDll)
            else:
                raise DemanglerFError('no such file {0}'.format(demangleDll))
        else:
            from GHS_Demangler import CFallBackDemangler
            return CFallBackDemangler()
    else:
        raise DemanglerFError('compiler "{0}" not supported'.format(compiler))
        
sys.path.append( os.path.dirname(__file__))
