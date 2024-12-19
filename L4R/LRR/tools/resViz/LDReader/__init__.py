#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
#  @copyright (c) 2019 - 2021 by Robert Bosch GmbH. All rights reserved.
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
#  @brief : dispatch LDReader
#=============================================================================



import os
import sys

class LDReaderError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message

def LDReader(compiler,filename):
    if compiler.upper() == 'GHS':
        fext = os.path.splitext(filename)[1].lower()
        if fext == '.ld':
            from GHS_LDReader import GHS_LDReader
            return GHS_LDReader(filename)
        else:
            raise LDReaderError('unsupported fileformat (fileextension) {0}'.format(fext))
    else:
        raise LDReaderError('unsupported Compiler {0}'.format(compiler))

sys.path.append( os.path.dirname(__file__))

