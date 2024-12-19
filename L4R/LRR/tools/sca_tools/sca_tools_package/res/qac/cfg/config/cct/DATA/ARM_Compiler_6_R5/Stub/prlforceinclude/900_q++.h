#ifndef PRLGCC_INCLUDED_QNX
#define PRLGCC_INCLUDED_QNX

#ifdef __QNX__
#include <__refstring>

// For openacc.h
#if __cplusplus >= 201103
#define __GOACC_NOTHROW noexcept
#endif

// See Case 680633
namespace std
{
   inline namespace __1
   { }
}
#endif

#endif
