// qacpp_typeof.h
//

#ifndef PRLGCC_INCLUDED_QACPP_TYPEOF
#define PRLGCC_INCLUDED_QACPP_TYPEOF

#include "500_qacpp_reference_traits.h"
#define typeof(__expr) typename __qacpp_remove_reference<decltype((__expr))>::type
#define __typeof typeof
#define __typeof__ typeof

#endif
