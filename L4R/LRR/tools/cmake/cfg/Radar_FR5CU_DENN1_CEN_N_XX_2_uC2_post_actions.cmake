#  F I L E  N A M E
#-----------------------------------------------------------------------------
#  File name should follow the following syntax or else it will not be included.
#  <variant_name>_post_actions.cmake.
#
#  File should be placed inside RB_CUSTOMER_CMAKE_DIR. It is same directory where
#  variant specific config files are kept.
#
#-----------------------------------------------------------------------------
#  H O W  T O  U S E
#-----------------------------------------------------------------------------
#  Copy and paste this template as it is without making any change. Add the 
#  post build steps as per project's requirement.
#
#=============================================================================

#=============================================================================
# DO NOT EDIT/REMOVE BELOW CODE BLOCK 
#=============================================================================
# Include guards to make sure the file is included only once

if(RB_CUSTOMER_DEFINED_POST_ACTIONS)
    return()
endif(RB_CUSTOMER_DEFINED_POST_ACTIONS)
set(RB_CUSTOMER_DEFINED_POST_ACTIONS true)
message(STATUS "Including customer maintained post build actions file.")

function(rb_smoke_test_pjifuc_setup)
    MESSAGE(STATUS "[--- post action build is started... -----------------------------]")
    #Run
    set(l_Command_call_Create_testEnv_directory 
        "${TCC_PYTHON3}/python.exe"
        "${RB_ROOT_DIR}/ad_radar_apl/tools/cmake/scripts/directory_creator.py"
        -d "${RB_BINARY_DIR}"
        -v "${RB_TARGET_BIN_NAME}"
        -dc "${RB_ROOT_DIR}/ad_radar_apl/tools/cmake/scripts/testEnv_directory_config.yaml"
    )
    add_custom_target(
        COPY_EXECUTABLES_TO_TESTENV ALL
        COMMAND ${l_Command_call_Create_testEnv_directory}
        COMMENT "Create testEnv directory using python script"
        VERBATIM
    )
    message(${l_Command_call_Create_testEnv_directory})
    add_dependencies(COPY_EXECUTABLES_TO_TESTENV HEX_FILE_MERGER) # HEX_FILE_MERGER is the last target built by ESM-maintained post build actions
endfunction()

if(NOT ${RB_SW_TARGET} STREQUAL "Cantata")
    rb_smoke_test_pjifuc_setup()
# generate the build information for Cantata
else()
    rb_build_version_generation()
endif(NOT ${RB_SW_TARGET} STREQUAL "Cantata")
