// prlgcc_cppconfig.h
//

#ifndef INCLUDED_PRLGCC_CPPCONFIG
#define INCLUDED_PRLGCC_CPPCONFIG

//
// Conditionally include the 'c++config.h' file to determine versions
// for GNU C++ stubs.
#if defined (__GNUC__) && defined (__cplusplus)
#include <bits/c++config.h>
#endif

#endif
