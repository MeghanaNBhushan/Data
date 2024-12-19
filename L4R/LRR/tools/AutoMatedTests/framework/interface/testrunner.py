# -*- coding: utf-8 -*-

from atf_exception import CNoDerivedClassError


## Abstract class as interface for all ATF test suites.  
#
class CTestRunner(object):

    ## @brief Abstract function for the implementation of the execution of FR5CU UC1 test cases. 
    #                  
    def executeFr5CuTestsUC1(self):
        raise CNoDerivedClassError("Function: executeFr5CuTestsUC1() has to be implemented in derived class")

    ## @brief Abstract function for the implementation of the execution of FR5CU UC2 test cases. 
    #    
    def executeFr5CuTestsUC2(self):
        raise CNoDerivedClassError("Function: executeFr5CuTestsUC2() has to be implemented in derived class")

    ## @brief Abstract function to get the component name of the derived test component.
    #                         
    def getComponentName(self):
        raise CNoDerivedClassError("Function: getComponentName() has to be implemented in derived class")        
    