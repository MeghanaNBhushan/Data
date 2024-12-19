import sys
import time
import os

sys.path.append(os.path.abspath('../scheduling'))

import atf_globalconstants as globalConstants

# performs a Power On Reset of the Debuggers. 

def flash_ecu_run_fr5cu(t32_api, logger, args):
    
    logger.info(f"Turn synch off for flashing in uC1 and uC2")
    t32_api[globalConstants.k_atf_hardwareLrrUc2].synch_off()
    t32_api[globalConstants.k_atf_hardwareLrrUc1].synch_off()
  
    # flash Plant container
    logger.info(f"Start flashing '{args.hexfileuC2}'")
    t32_api[globalConstants.k_atf_hardwareLrrUc2].flash_hex(args.hexfileuC2)
    logger.info(f"Start flashing '{args.hexfileuC1}'")
    t32_api[globalConstants.k_atf_hardwareLrrUc1].flash_hex(args.hexfileuC1)

    # load symbols
    logger.info(f"Loading symbols '{args.elffileuC2}'")
    t32_api[globalConstants.k_atf_hardwareLrrUc2].load_elf(args.elffileuC2)  
    logger.info(f"Loading symbols '{args.elffileuC1}'")
    t32_api[globalConstants.k_atf_hardwareLrrUc1].load_elf(args.elffileuC1)

    # initialise Script to avoid an exception due to a system reset after a diagnosis reset
    logger.info(f"Turn synch on after flashing in uC1 and uC2")
    t32_api[globalConstants.k_atf_hardwareLrrUc2].reset("PORST", "RestoreGo")
    t32_api[globalConstants.k_atf_hardwareLrrUc1].reset("PORST", "RestoreGo")
    t32_api[globalConstants.k_atf_hardwareLrrUc2].synch_on()
    t32_api[globalConstants.k_atf_hardwareLrrUc1].synch_on()
    time.sleep(3)
    
    logger.info("Execute SysResetException script")
    absolutePathToScript = os.path.abspath('./framework/config/cmmScripts/SysResetExeptionWorkaround_Init.cmm')
    t32_api[globalConstants.k_atf_hardwareLrrUc1].execute_t32_script(absolutePathToScript)
    t32_api[globalConstants.k_atf_hardwareLrrUc2].execute_t32_script(absolutePathToScript)
    
    logger.info("Set Reset Behaviour to RunRestore (required for diagnostic reset)")
    t32_api[globalConstants.k_atf_hardwareLrrUc1].execute_t32_command("SYStem.Option RESetBehavior RunRestore")
    t32_api[globalConstants.k_atf_hardwareLrrUc2].execute_t32_command("SYStem.Option RESetBehavior RunRestore")


def resetLauterbach(t32_api, logger):
    logger.debug("Resetting Lauterbach...")
    hw = list(t32_api.keys())
    if hw[0] == globalConstants.k_atf_hardwareLrrUc1 or hw[0] == globalConstants.k_atf_hardwareLrrUc2:
        logger.debug("Turn synch off for reset in uC1 and uC2")
        t32_api[globalConstants.k_atf_hardwareLrrUc2].synch_off()
        t32_api[globalConstants.k_atf_hardwareLrrUc1].synch_off()
              
        logger.debug("Perform reset..........")
        t32_api[globalConstants.k_atf_hardwareLrrUc2].reset("PORST", "RestoreGo")
        t32_api[globalConstants.k_atf_hardwareLrrUc1].reset("PORST", "RestoreGo")
    
        logger.debug("Turn synch on after reset in uC1 and uC2")
        t32_api[globalConstants.k_atf_hardwareLrrUc2].synch_on()
        t32_api[globalConstants.k_atf_hardwareLrrUc1].synch_on()
        time.sleep(3)
    else:
        # last supported release for NR5CP was xRR_LGU_PF_V7.0.0
        raise Exception("NR5CP is not supported anymore. last supported release was xRR_LGU_PF_V7.0.0")        
        

# set Lauterbach debugger into System Mode "NoDebug" to ensure that the debugger does not have an effect on e.g. the startup behaviour
def setSystemModeNoDebug(lauterbachApi, logger, apiName):
    lauterbachApi.execute_t32_command("SYStem.Mode NoDebug")
    logger.debug(f"Set {apiName} Debugger into 'NoDebug' mode")

# set Lauterbach debugger into System Mode "Attach" to be able to read symbols
def setSystemModeAttach(lauterbachApi, logger, apiName):
    lauterbachApi.execute_t32_command("SYStem.Mode Attach")
    logger.debug(f"Set {apiName} Debugger into 'Attach' mode")
    
