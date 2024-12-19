#ifndef _QACPP_MSC_EXT_OUTER
#define _QACPP_MSC_EXT_OUTER
#define _QACPP_PropIdl_OUTER
#pragma push_macro("_MSC_EXTENSIONS")
#define _MSC_EXTENSIONS 1
#endif

#include_next <PropIdl.h>

#ifdef _QACPP_PropIdl_OUTER
#pragma pop_macro("_MSC_EXTENSIONS")
#undef _QACPP_PropIdl_OUTER
#undef _QACPP_MSC_EXT_OUTER
#endif
