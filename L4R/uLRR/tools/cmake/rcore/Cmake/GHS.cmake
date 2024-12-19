

# --------------------------------------------------------------------------------------------------
# Toolchain configuration 
# --------------------------------------------------------------------------------------------------

# Configure the compiler version
set( COMPILER_VERSION "comp_201814_1fp_WIN64")

# The toolchain prefix for all toolchain executables
set(CMAKE_C_COMPILER_ABI "")

# configure the toolchain path
set(TOOLCHAIN_PATH "C:/TCC/Tools/greenhills_arm/${COMPILER_VERSION}")

# configure the liker file path
set(LINKER_FILE "${CMAKE_CURRENT_SOURCE_DIR}/cubas/cfg/LinkScript/rbl_Memory_LinkerFile_R5.ld")

# set file extension for assembly files
set(CMAKE_ASM_SOURCE_FILE_EXTENSIONS s;S;asm;arm)

# Warning avoidance
set(CMAKE_ASM_COMPILER_ID "ARM") 

set(CMAKE_ASM_COMPILER    "${TOOLCHAIN_PATH}/ccarm.exe"          CACHE FILEPATH "GHS Assembler"           FORCE)
set(CMAKE_C_COMPILER      "${TOOLCHAIN_PATH}/ccarm.exe"          CACHE FILEPATH "GHS C Compiler"          FORCE)
set(CMAKE_CXX_COMPILER    "${TOOLCHAIN_PATH}/cxarm.exe"          CACHE FILEPATH "GHS Cpp Compiler"        FORCE)
set(CMAKE_AR              "${TOOLCHAIN_PATH}/ax.exe"             CACHE FILEPATH "GHS Archiver"            FORCE)
set(CMAKE_LINKER          "${TOOLCHAIN_PATH}/cxarm.exe"          CACHE FILEPATH "GHS Linker"              FORCE)
set(CMAKE_NM              "${TOOLCHAIN_PATH}/gnm.exe"            CACHE FILEPATH "GHS nm symbol list"      FORCE)
set(CMAKE_OBJDUMP         "${TOOLCHAIN_PATH}/gdump.exe"          CACHE FILEPATH "GHS Object Dump"         FORCE)
set(CMAKE_ADDR2LINE       "${TOOLCHAIN_PATH}/gaddr2line.exe"     CACHE FILEPATH "GHS address translator"  FORCE)
set(CMAKE_STRIP           "${TOOLCHAIN_PATH}/gstrip.exe"         CACHE FILEPATH "GHS Strip Symbols"       FORCE)
set(CMAKE_MAKE_PROGRAM    "ninja.exe"                            CACHE FILEPATH "MAKE Tool"               FORCE)
set(CMAKE_OBJCOPY         "")
set(CMAKE_RANLIB          "")
set(CMAKE_READELF         "")

# The CMAKE_SYSTEM_NAME is the CMake-identifier of the target platform to build for.
set( CMAKE_SYSTEM_NAME Generic )
# The CMAKE_SYSTEM_PROCESSOR is the CMake-identifier of the target architecture to build for.
set( CMAKE_SYSTEM_PROCESSOR arm7 )
# The CMAKE_SYSROOT is optional, and may be specified if a sysroot is available.
# set( CMAKE_SYSROOT )
# shearch for programs in the build host directories
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER )
# Set cross compiling as true
set(CMAKE_CROSSCOMPILING "TRUE")
# Skip the cmake compiler check
set(CMAKE_C_COMPILER_WORKS 1)
# skip the cmake compiler check
set(CMAKE_CXX_COMPILER_WORKS 1)

# for libraries and headers in the target directories
set( CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY )
set( CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY )
set( CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY )
set( CMAKE_EXPORT_COMPILE_COMMANDS             ON)
set( CMAKE_C_USE_RESPONSE_FILE_FOR_INCLUDES    ON)
set( CMAKE_C_USE_RESPONSE_FILE_FOR_LIBRARIES   ON)
set( CMAKE_C_USE_RESPONSE_FILE_FOR_OBJECTS     ON)
set( CMAKE_CXX_USE_RESPONSE_FILE_FOR_INCLUDES  ON)
set( CMAKE_CXX_USE_RESPONSE_FILE_FOR_LIBRARIES ON)
set( CMAKE_CXX_USE_RESPONSE_FILE_FOR_OBJECTS   ON)
set( CMAKE_NINJA_FORCE_RESPONSE_FILE           ON)

# The CMAKE_<LANG>_COMPILER variables may be set to full paths, or to names
# of compilers to search for in standard locations. For toolchains that do 
# not support linking binaries without custom flags or scripts one may set 
# the CMAKE_TRY_COMPILE_TARGET_TYPE variable to STATIC_LIBRARY to tell CMake 
# not to try to link executables during its checks.
set( CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY )

# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Definition of common flags to use with this tool chain 
# --------------------------------------------------------------------------------------------------
# Definition of the CPU to Architecture
set(GREENHILLS_COMMON_FLAGS  "-cpu=cortexr5f")
# use floating point hardware suport (FPU)
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -fhard")
# adds support to gnu style assembly calls
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} --gnu_asm")
# Use C Language c99 with extensions
#set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -c99")
# Generates both a listing of symbols sorted alphabetically by name and a listing of symbols sorted numerically by address.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -Man")
# generation of cross-reference information in the map file
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -Mx")
# Adds an extra column to the map file's table of symbols that contains D for
# symbols which are unreferenced and therefore able to be deleted.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -Mu")
#Adds list of locals to the linker-generated map file. This list does
# not contain zero-sized symbols or compiler-generated symbols.
set(GREENHILL_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -Ml")
# Quit Building if Warnings are Generated
#set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} --quit_after_warnings")
# Extended format with additional details in global and local symbol tables.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -mapfile_type=2")
# uses the gmemfile utility program creates a binary memory image of a fully linked executable
# set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -memory")
# Throw Error if a function referenced or called when no prototype has been provided.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} --prototype_errors")
# Generates warnings in the event of inconsistent types for the definition and uses of global variables only where
# type-checking information is available.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -globalcheck=normal")
# Verifies in link-time global variable type qualifiers such as const and volatile
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -globalcheck_qualifiers")
# perform link-time argument type checking
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -argcheck=normal")
# Create a file with a list of section sizes.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -gsize")
# display globals
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -e=rba_SysPreinit_ResetHandler")
# Display linker warnings
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -linker_warnings")
# Issues errors for all overlapping sections, even when a section is zero bytes in size.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -strict_overlap_check")
# The C preprocessor resolves preprocessing directives such as #include, #if, and #ifdef. 
# The preprocessor expands macros in preprocessing directives, but not in the rest of the file.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} --preprocess_linker_directive_full")
# Forces the output of Gdump to be in little endian format
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -littleendian")
# Specifies output of Intel HEX386
#set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -hex386=./bin/${CMAKE_PROJECT_NAME}.hex")
# include/arm — Contains header files for ARM extensions for C and C++.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -I ${TOOLCHAIN_PATH}/include/arm/")
# ansi — Contains Standard C library header files.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -I ${TOOLCHAIN_PATH}/ansi")
#ensures that cpp libraies are linked to the final executable
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -language=cxx")
# scxx — Contains Standard C++ library header files.
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -I ${TOOLCHAIN_PATH}/scxx")
# eecxx — Contains Extended Embedded C++ library header files.
# set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -I ${TOOLCHAIN_PATH}/eecxx")
# ecxx — Contains Embedded C++ library header files.
# set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -I ${TOOLCHAIN_PATH}/ecxx")
# invokes the preprocessor to take advantage of preprocessor facilities 
# (such as include and #define) that are not normally available in assembly language
set(GREENHILLS_COMMON_FLAGS "${GREENHILLS_COMMON_FLAGS} -preprocess_assembly_files" 
                            CACHE STRING "Flags for GreenHills Compiler and Linker" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for Assembler - Common flags all build types
# --------------------------------------------------------------------------------------------------
# Add common Flags ASM/C/C++ flags
set(CMAKE_ASM_FLAGS  "${GREENHILLS_COMMON_FLAGS} " CACHE STRING "ASM Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for Assembler - Build Type Debug
# --------------------------------------------------------------------------------------------------
set(CMAKE_ASM_FLAGS_DEBUG   "" CACHE STRING "ASM Debug Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for Assembler - Build Type Release
# --------------------------------------------------------------------------------------------------
set(CMAKE_ASM_FLAGS_RELEASE "" CACHE STRING "ASM Debug Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for C Compiler - Common flags all build types
# --------------------------------------------------------------------------------------------------
set(CMAKE_C_FLAGS "${GREENHILLS_COMMON_FLAGS} " CACHE STRING "C Flags" FORCE)
# Wrap diagnostic messages when they are too long to fit on a single line.
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --wrap_diagnostics")

# TODO: INTEGRATION STEP - Downgrade compiler warnings to remark DURING INTEGRATION ONLY!  
# Unused funtions
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --diag_remark=177")
# A translation unit must contain at least one declaration
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --diag_remark=96")
# variable was set but never used
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --diag_remark=550")
# vMem_30_XXspi01_LL_InstanceInitializer two for loops with init expression with no effect.
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --diag_remark=174")

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --diag_remark=826")

# Issue a warning if the declaration of a local variable shadows the
# declaration of a variable of the same name declared at the global scope, or at an outer scope
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wshadow" CACHE STRING "C Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for C Compiler - Build Type Debug
# --------------------------------------------------------------------------------------------------
# generate Source Level debuging information
set(CMAKE_C_FLAGS_DEBUG     "-G -Odebug -dual_debug" CACHE STRING "C Debug Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for C Compiler - Build Type Release
# --------------------------------------------------------------------------------------------------
set(CMAKE_C_FLAGS_RELEASE   "" CACHE STRING "C Debug Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for C++ Compiler - Common flags all build types
# --------------------------------------------------------------------------------------------------
set(CMAKE_CXX_FLAGS        "${GREENHILLS_COMMON_FLAGS} " CACHE STRING "CXX Flags" FORCE)
# Disables support for exception handling
set(CMAKE_CXX_FLAGS       "${CMAKE_CXX_FLAGS} --C++11")
# disable Run-Time Type Information (RTTI) default for EC++ and EEC++
set(CMAKE_CXX_FLAGS       "${CMAKE_CXX_FLAGS} --no_rtti")
# Standard C++ (Violations Give Errors)
set(CMAKE_CXX_FLAGS       "${CMAKE_CXX_FLAGS} --STD")
# C++ without exceptions
set(CMAKE_CXX_FLAGS       "${CMAKE_CXX_FLAGS} --stdl")
# Disables support for exception handling
set(CMAKE_CXX_FLAGS       "${CMAKE_CXX_FLAGS} --no_exceptions" CACHE STRING "CXX Flags" FORCE)

set(CMAKE_CXX_FLAGS       "${CMAKE_CXX_FLAGS} -std=c++11 -pedantic")

# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for C++ Compiler - Build Type Debug
# --------------------------------------------------------------------------------------------------
set(CMAKE_CXX_FLAGS_DEBUG   "" CACHE STRING "CXX Debug Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for C++ Compiler - Build Type Release
# --------------------------------------------------------------------------------------------------
set(CMAKE_CXX_FLAGS_RELEASE "" CACHE STRING "CXX Debug Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Pre Build Libraries to link to the finnal executable
# --------------------------------------------------------------------------------------------------
# linker Libraries
set(CMAKE_EXE_LINKER_LIBS   "" CACHE STRING "Linker Libraries" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Add common flags to use with the linker
# --------------------------------------------------------------------------------------------------
set(CMAKE_EXE_LINKER_FLAGS "${GREENHILLS_COMMON_FLAGS} ")

# Provide the path to the linker file
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -T ${LINKER_FILE}")
# Generate User-Specified Map File
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -map --preprocess_linker_directive_full")
# keep the map file even if there is a link error
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -keepmap")
# Link all the necessary libraries to the project
#set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -l${CMAKE_EXE_LINKER_LIBS}")
# Issues errors for all overlapping sections, even when a section is zero bytes in size
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -strict_overlap_check" CACHE STRING "Linker Flags" FORCE)
# Print all the libraries linked to the executable
# set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -lnk=-v" CACHE STRING "Linker Flags" FORCE)
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -paddr_offset=0" CACHE STRING "Linker Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for linker - Build Type Debug
# --------------------------------------------------------------------------------------------------
set(CMAKE_EXE_LINKER_FLAGS_DEBUG   "" CACHE STRING "Linker Debug Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Setup Specific Flags for linker - Build Type Release
# --------------------------------------------------------------------------------------------------
set(CMAKE_EXE_LINKER_FLAGS_RELEASE "" CACHE STRING "Linker Release Flags" FORCE)
# --------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# Create a static archive incrementally for large object file counts.
# --------------------------------------------------------------------------------------------------
set(CMAKE_C_CREATE_STATIC_LIBRARY "<CMAKE_C_COMPILER>  <LINK_FLAGS> <OBJECTS> -archive -o <TARGET>")
set(CMAKE_CXX_CREATE_STATIC_LIBRARY "<CMAKE_CXX_COMPILER> <LINK_FLAGS> <OBJECTS> -archive -o <TARGET>")