// c++config.h
//

#ifndef PRLGCC_INCLUDED_CPPCONFIG_H
#define PRLGCC_INCLUDED_CPPCONFIG_H

#include_next "bits/c++config.h"

// Set PRL_GLIBCXX variables for this libstdc++ version
#include "bits/qacpp_glibcxx.h"

// QA C++ prior to 4.0 supported nullptr through a class type
#include "bits/qacpp_nullptr_exception_ptr.h"

// Disable 128 bit int
#undef _GLIBCXX_USE_INT128

// Disable 128 bit float
#undef _GLIBCXX_USE_FLOAT128


#if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 8)
// Macros for ABI tag attributes (this is not in 4.8.1 but are in 4.8.3)
#  ifndef _GLIBCXX_ABI_TAG_CXX11
#   define _GLIBCXX_ABI_TAG_CXX11 __attribute ((__abi_tag__ ("cxx11")))
#  endif
#endif // (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 8)


// #if __GLIBCXX__ == 20181206
#if (__PRL_GLIBCXX__ == 7) && (__PRL_GLIBCXX_MINOR__ == 4)
// Used in cygwin g++ 7.4 type_traits, found in type_traits versions from 2017
#define __has_unique_object_representations(x) 0
#define __is_aggregate(x) 0
#endif


#endif // PRLGCC_INCLUDED_CPPCONFIG_H
