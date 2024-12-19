cmake_minimum_required(VERSION 3.5.1 FATAL_ERROR)
message(STATUS "+++++++++  ${CMAKE_CURRENT_LIST_FILE}")
set(BUILD_RECURSIVE_CALL_OPTIONS )
if(RB_PROJECT_VARIANT_CFG_DIRECTORY)
  list(APPEND BUILD_RECURSIVE_CALL_OPTIONS "-DRB_PROJECT_VARIANT_CFG_DIRECTORY=${RB_PROJECT_VARIANT_CFG_DIRECTORY}")  
endif(RB_PROJECT_VARIANT_CFG_DIRECTORY)


# initial checks -----------------------------------------------------------------------------------------
if( NOT ( RB_TARGET_PRODUCT AND RB_TARGET_PRODUCT STRGREATER "" ) ) 
	message(FATAL_ERROR "RB_TARGET_PRODUCT must be defined")
endif() 

if(NOT ${RB_TARGET_PRODUCT} STREQUAL "DASY" )
	if( NOT ( RB_TARGET_SYSTEM AND RB_TARGET_SYSTEM STRGREATER "" ) ) 
		message(FATAL_ERROR "RB_TARGET_SYSTEM / Hardware must be defined")
	endif() 
	if( NOT ( RB_TARGET_VARIANT AND RB_TARGET_VARIANT STRGREATER "" ) ) 
		message(FATAL_ERROR "RB_TARGET_VARIANT must be defined")
	endif() 
endif() 

set(RB_KNOWN_PRODUCTS DASY DASYMC RADAR VIDEO)
list(FIND RB_KNOWN_PRODUCTS ${RB_TARGET_PRODUCT} l_index)
if(l_index EQUAL -1 )
	message(FATAL_ERROR "PRODUCT ${RB_TARGET_PRODUCT} not supported - product must be in ${RB_KNOWN_PRODUCTS}" )
endif(l_index EQUAL -1 )


# set initial variables ----------------------------------------------------------------------------------
set(RB_TARGET_PRODUCT ${RB_TARGET_PRODUCT} CACHE STRING "PROJECT PRODUCT DEFINITION" FORCE)
set(RB_TARGET_SYSTEM ${RB_TARGET_SYSTEM} CACHE STRING "PROJECT SYSTEM DEFINITION" FORCE)
set(RB_TARGET_VARIANT ${RB_TARGET_VARIANT} CACHE STRING "PROJECT VARIANT DEFINITION" FORCE)
set(RB_PROJECT_DIR ${CMAKE_CURRENT_LIST_DIR} CACHE FILEPATH "PROJECT SRC DIRECTORY" FORCE)
set(GENERATED_FILES_PATH ${CMAKE_SOURCE_DIR}/generatedFiles/cmake/${RB_TARGET_VARIANT} CACHE FILEPATH "GENERATED FILES PATH" FORCE)


# get tools's folder path ---------------------------------------------------------------------------------
function(rb_utils_get_file_path)	
	set(l_Options)
    set(l_OneValueArgs FILE_NAME SEARCH_PATH FILE_PATH_OUT)
    set(l_MultiValueArgs)
    cmake_parse_arguments(f "${l_Options}" "${l_OneValueArgs}" "${l_MultiValueArgs}" ${ARGN})
	
	file(GLOB_RECURSE l_Files
			"${f_SEARCH_PATH}/${f_FILE_NAME}"
		)
	
	list(LENGTH l_Files l_FilesLength)
	
	if(l_FilesLength GREATER 0)
		list(GET l_Files 0 l_FirstFileFound)
		file(RELATIVE_PATH l_file_path ${f_SEARCH_PATH} ${l_FirstFileFound})
		get_filename_component(l_file_path ${l_FirstFileFound} DIRECTORY)
		set(${f_FILE_PATH_OUT} "${l_file_path}" PARENT_SCOPE)
	else()
		set(${f_FILE_PATH_OUT} "NOT_FOUND" PARENT_SCOPE)
	endif()
endfunction()

set(l_fileToSearch "ip_if/tools/searchToolFileESM.esm")
set(l_filePath "")
rb_utils_get_file_path(
	FILE_NAME ${l_fileToSearch} 
	SEARCH_PATH ${CMAKE_SOURCE_DIR}
	FILE_PATH_OUT l_filePath
	)
if(l_filePath STREQUAL "NOT_FOUND")
	set(RB_TOOLS_PATH ${CMAKE_SOURCE_DIR}/ip_if/tools CACHE FILEPATH "TOOLS PATH" FORCE)
else()
	set(RB_TOOLS_PATH ${l_filePath} CACHE FILEPATH "TOOLS PATH" FORCE)
endif()


# includes -------------------------------------------------------------------------------------------
set(CMAKE_MODULE_PATH ${RB_TOOLS_PATH}/cmake CACHE FILEPATH "CMAKE CUSTOMATION MODULES PATH" FORCE)
set(RB_CMAKE_LIB_PATH ${CMAKE_MODULE_PATH} CACHE FILEPATH "CMAKE TOOL CONFIG" FORCE)
include(${RB_CMAKE_LIB_PATH}/vswitch_lib.cmake)
include(${RB_CMAKE_LIB_PATH}/rb_utils.cmake)
include(${RB_CMAKE_LIB_PATH}/utils/rb_msg.cmake)


# include tcc tools path file ------------------------------------------------------------------------
if(BUILD_TCC_TOOLS_PATH_FILE)
	include("${BUILD_TCC_TOOLS_PATH_FILE}")
else(BUILD_TCC_TOOLS_PATH_FILE)
	find_file(TCC_TOOLS_PATH_FILE TCC_ToolPaths.cmake ${CMAKE_BINARY_DIR})
	if(TCC_TOOLS_PATH_FILE STREQUAL "TCC_TOOLS_PATH_FILE-NOTFOUND")
		rb_utils_warning_message("TCC tools path file is not found.")
	else()
		rb_utils_status_message("Including TCC tools path file found at: ${TCC_TOOLS_PATH_FILE}")
		include("${TCC_TOOLS_PATH_FILE}")
		set(BUILD_TCC_TOOLS_PATH_FILE "${TCC_TOOLS_PATH_FILE}")
		list(APPEND BUILD_RECURSIVE_CALL_OPTIONS "-DBUILD_TCC_TOOLS_PATH_FILE=${BUILD_TCC_TOOLS_PATH_FILE}")
	endif()
endif(BUILD_TCC_TOOLS_PATH_FILE)


# set project variables ----------------------------------------------------------------------------------
set(RB_PROJECT_NAME ${RB_TARGET_PRODUCT})
if(${RB_TARGET_PRODUCT} STREQUAL "DASY" )
	project(${RB_TARGET_PRODUCT} )
endif(${RB_TARGET_PRODUCT} STREQUAL "DASY" )


# includes -----------------------------------------------------------------------------------------------
include(rb_features)
include("${RB_CMAKE_LIB_PATH}/${RB_TARGET_PRODUCT}.cmake")
include("${RB_CMAKE_LIB_PATH}/doxygen/rb_doxygen.cmake")
include("${RB_CMAKE_LIB_PATH}/doxygen/rb_doxygen_components.cmake")
include("${RB_CMAKE_LIB_PATH}/doxygen/rb_pdf_latex_per_component.cmake")
include("${RB_CMAKE_LIB_PATH}/doxygen/rb_pdf_latex_whole_proj.cmake")
include("${RB_CMAKE_LIB_PATH}/calcres/rb_calcres.cmake")
include("${RB_CMAKE_LIB_PATH}/coverity/rb_coverity.cmake")
include("${RB_CMAKE_LIB_PATH}/shadowfiles/rb_shadowfiles.cmake")
include("${RB_CMAKE_LIB_PATH}/help/rb_help.cmake")

# dc_ml include -----------------------------------------------------------------------------------------
set(dc_ml_DIR ${CMAKE_CURRENT_SOURCE_DIR}/ip_if/dc_ml) 

add_library(daddy_env
	${dc_ml_DIR}/daddy/src/monitor/daddy_monitor.cpp
	${dc_ml_DIR}/daddy/src/mempool/daddy_mempool_base.cpp
	${dc_ml_DIR}/daddy/src/port/receiver/proxy/daddy_interface_controller.cpp
	${dc_ml_DIR}/daddy/open_variation_point/aurix_plus/adapter/os_aurixPlus_speciallocks.cpp
)

target_include_directories(daddy_env SYSTEM
	PUBLIC
		${dc_ml_DIR}/daddy/inc
		${dc_ml_DIR}/daddy/../vfc/include
		${dc_ml_DIR}/daddy/config/proxy_aurix_plus
	INTERFACE
		${dc_ml_DIR}/daddy/../vfc/include/vfc
		${dc_ml_DIR}/daddy/../vfc/include/vfc/core
		${dc_ml_DIR}/daddy/../vfc/include/vfc/container
) 

target_link_libraries(${RB_TARGET_VARIANT}  daddy_env)

# print project summary -----------------------------------------------------------------------------------
rb_print_project_summary()
