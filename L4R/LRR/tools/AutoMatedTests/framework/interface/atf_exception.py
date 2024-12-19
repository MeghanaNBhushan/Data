#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
# @copyright (c) 2021 - 2022 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
#=============================================================================
#  P R O J E C T   I N F O R M A T I O N
#-----------------------------------------------------------------------------
#     Projectname: L4 Radar
#=============================================================================
#  I N I T I A L   A U T H O R   I D E N T I T Y
#-----------------------------------------------------------------------------
#        Name: BAD2LR
#  Department: XC-AD/PJ-AS12
#=============================================================================
# @file  atf_exception.py
#=============================================================================


class CNoDerivedClassError(Exception):
    """Exception raised if the class/function is directly instantiated.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

        
        
        