#ifndef PRLGCC_INCLUDED_QNX
#define PRLGCC_INCLUDED_QNX

#ifdef __QNX__
#include <__refstring>
#endif

// For openacc.h
#if __cplusplus >= 201103
#define __GOACC_NOTHROW noexcept
#endif

#endif
