#ifndef _QACPP_MSC_EXT_OUTER
#define _QACPP_MSC_EXT_OUTER
#define _QACPP_WinNT_OUTER
#pragma push_macro("_MSC_EXTENSIONS")
#define _MSC_EXTENSIONS 1
#endif

#include_next <winnt.h>

#ifdef _QACPP_WinNT_OUTER
#pragma pop_macro("_MSC_EXTENSIONS")
#undef _QACPP_WinNT_OUTER
#undef _QACPP_MSC_EXT_OUTER
#endif
