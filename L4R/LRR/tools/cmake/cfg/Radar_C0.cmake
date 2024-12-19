# Include guards to make sure the file is included only once
if(RB_CUSTOMER_CONFIG_FILE_INCLUDE_GUARD)
  return()
endif(RB_CUSTOMER_CONFIG_FILE_INCLUDE_GUARD)
set(RB_CUSTOMER_CONFIG_FILE_INCLUDE_GUARD true)

# Set variable to generate type2 map file
set(RB_PROJECT_GENRATE_LINKER_MAPFILE_TYPE_2 ON)

# Set variable to access CANTATA startup library path
set(RB_PROJECT_CANTATA_TARGET_STARTUP_LIBRARY_PATH "ad_radar_apl/tools/cantata/uC_support")


# Main Flux file, which is the entry point for flux build generator
set(RB_PROJECT_FLUXFILE "ad_radar_apl/arch/system.flux" CACHE INTERNAL "Flux file")
#compiler option selection
set(RB_PROJECT_OPTION_SETS "IFX6DEFAULT" CACHE INTERNAL "Selecting option set IFX6 default")
# Add all global include directories  
set(RB_PROJECT_GLOBAL_EXTRA_INCLUDE_DIRS 
    #1.Please do not add here any vfc/include/ or daddy/inc paths, its all handled by the
    #  forward headers generated by the Flux compensator.
    #2.Please do not add daddy/open_variation_point/aurix_plus path. Just check your target variation point (for eg Radar_C0,DASY_INT_DEFAULT_ENH )
    #  in system flux file which daddy configuration (for eg aurix_plus_Sequential, proxy_aurix_plus ...) is used
    #3.Should you have any questions, please contact the MOM team - ccdaesi5teammom@bosch.com
	"${RB_ROOT_DIR}/ip_if/mom/daddy/test/mock/aurix_plus"
	"${RB_ROOT_DIR}/ip_if/mom/daddy/test/mock/target_common"
    # todo see https://rb-tracker.bosch.com/tracker08/browse/PJIF-13064
    "${RB_ROOT_DIR}/ip_if/mom/daddy/test/mock/variation_point/aurix_plus_deprecated"
	"${RB_ROOT_DIR}/customer_sources/customer_interface"
	"${RB_ROOT_DIR}/ip_dc/dc_fw/inc/dc_interfaces/per/daddy/output"
	"${RB_ROOT_DIR}/ip_dc/dc_fw/inc"
	"${RB_ROOT_DIR}/ip_dc/dc_fw/inc/dc_interfaces/dc_math/norms"
	CACHE INTERNAL ""
)
#include(globalDefines)
set (RB_ARCH_BUILD_CFG_DIR "${RB_ROOT_DIR}/ip_if/arch/uC/build_options")
# Global defines should be added here
if(${RB_SW_TARGET} STREQUAL "Cantata")
	set(RB_PROJECT_MODULE_TEST_ENABLED 1)
	set(RB_PROJECT_diag_x_COP_ENABLED 1)
	if(${RB_UT_TARGET} STREQUAL "host")
		set(RB_PROJECT_GLOBAL_DEFINES DSV IF_UWE_RADAR DSP_PARA_A CANTATA_HOST_BUILD CACHE INTERNAL "global defines")
		set(RB_PROJECT_GHS_DIAGNOSTIC_OPTIONS ${RB_PROJECT_GHS_DIAGNOSTIC_OPTIONS} --fpermissive --diag_suppress=114)
	endif(${RB_UT_TARGET} STREQUAL "host")
	if(${RB_UT_TARGET} STREQUAL "target")
		set(RB_PROJECT_LINKER_SCRIPT_C "${RB_ROOT_DIR}/ad_radar_apl/tools/Cantata/uC_support/tc39x_ghs.ld")
		set(CMAKE_SCRIPT_MODE_FILE "True")
		set(RB_PROJECT_GLOBAL_DEFINES DSV IF_UWE_RADAR DSP_PARA_A CANTATA_TARGET_BUILD CACHE INTERNAL "global defines")
		set(RB_PROJECT_GHS_DIAGNOSTIC_OPTIONS ${RB_PROJECT_GHS_DIAGNOSTIC_OPTIONS} --diag_suppress=114)
	endif(${RB_UT_TARGET} STREQUAL "target")
else ()
	set(RB_PROJECT_GLOBAL_DEFINES DSV IF_UWE_RADAR DSP_PARA_A CACHE INTERNAL "global defines")
endif(${RB_SW_TARGET} STREQUAL "Cantata")

# Add all the external libraries that needs to be linked    
set(RB_PROJECT_EXTERNAL_LINK_LIBS
	"${RB_ROOT_DIR}ad_radar_apl/component/net_x/lib/XcpSeedKey.a"
	CACHE INTERNAL "List of external libraries"
)

set(RB_PROJECT_LINKER_DEFINES "-v -keeptempfiles -tmp=./temp")

option(
    RB_BUILD_CUSTOMER_SOURCES 
    "Option to build customer sources" 
    OFF
)
# Add all the external object files that needs to be linked 
set(RB_PROJECT_EXTERNAL_LINK_OBJECTS
    CACHE INTERNAL "List of external object files"
)

# Linker source file
set(RB_PROJECT_LINKER_SOURCES ${RB_ROOT_DIR}/rc_fw/dsp/SW/src/dsp/fep/spu/sbst/spu_sbst.o CACHE INTERNAL "")

# Build information
set(RB_PROJECT_USE_BUILD_VERSION_INFO 1 CACHE INTERNAL "")
# set(RB_PROJECT_USE_BUILD_VERSION_INFO_SOURCE 1 CACHE INTERNAL "")
# set(RB_PROJECT_USE_BUILD_VERSION_INFO_SOURCE_AT_LINKTIME 1 CACHE INTERNAL "")
set(RB_PROJECT_VERSION_INFO_ARRAY_INITIALIZER 1)

set(A2L_TOOLSET_PATH "C:/tools/asap2toolset12sp2/Exec" CACHE INTERNAL "")
set(RB_SCOM_OUTPUT_XML_FILE "${RB_ROOT_DIR}/ad_radar_apl/ToBeCleanUp/scom_gen/scom.xml" CACHE INTERNAL "")
set(RB_SCOM_MDF_CHECKER_FILE "${RB_ROOT_DIR}/ip_if/tools/signal_extractor/mdf_checker.ini" CACHE INTERNAL "")
set(RB_SIGNAL_EXTRACTOR_INI "${RB_ROOT_DIR}/ip_if/tools/signal_extractor/signalExtractor.ini" CACHE INTERNAL "")


# Cantata 
set(RB_PROJECT_MODULE_TEST_ENABLED  1)


set(RB_PROJECT_RUN_dependency_check 0 CACHE INTERNAL "Run dependency check as post build step")
set(RB_PROJECT_RUN_adx_converter 1 CACHE INTERNAL "Run adx converter as post build step")
set(RB_PROJECT_RUN_log_parser 0 CACHE INTERNAL "Get warning log as post build step")
set(RB_PROJECT_RUN_elf_to_hex 1 CACHE INTERNAL "Generate hexfile as post build step")
set(RB_PROJECT_HEXFILE_SIGN_N_MERGE 1 CACHE INTERNAL "Sign and merge hexfile")
if (NOT DEFINED RB_PROJECT_HAWCC_MERGE_HEXFILES)
    set(RB_PROJECT_HAWCC_MERGE_HEXFILES "ad_radar_apl/cubas/cfg/EcuCybSec_VMS-2_PJIF/Hsm_MXL/HSM_7_8_R20_VMS_2_0_1__PJIF_MXL__001.hex" "ad_radar_apl/cubas/cfg/EcuCybSec_VMS-2_PJIF/HsmEnabling/UCB-HSM_DbgEnabled_HsmEnabled_09-0D-08-07.hex" CACHE INTERNAL "")
endif(NOT DEFINED RB_PROJECT_HAWCC_MERGE_HEXFILES)

# Extract defines from Flux
set(RB_PROJECT_EXTRACT_DEFINES 1 CACHE INTERNAL "Boolean value to append --extract-defines to Flux Build Generator invocation")

# Persistent Data Viewer (PDV) DB generator cfg:
set(RB_PROJECT_RUN_pdv_database_generation TRUE)
set(RB_PROJECT_PDV_GEN_CONFIG_TEMPLATE  ${RB_ROOT_DIR}/ip_if/radar_if/pdv/PDVConfig.xml )
# PDV Gen expects a PDM/InSerT extract (rbPdmDataBlocksReport.xml generated by InSerT), but PJIF has no PDM Blocks, so a fake file is given here
# Customer projects shall provide the path of the real file (and they have to make sure that is upto date at every time)
set(RB_PROJECT_PDV_PDM_XML_FILES  ${RB_ROOT_DIR}/ip_if/radar_if/pdv/fake-rbPdmDataBlocksReport.xml ) 
set(RB_PROJECT_FAILUREDOCUGEN_CONFIG_FILE ${RB_ROOT_DIR}/ip_if/radar_if/pdv/config_FailureDocumentationGenerator.yaml )
 

# Version control defined for build_version feature
set(RB_PROJECT_VERSION_CONTROL "GIT")