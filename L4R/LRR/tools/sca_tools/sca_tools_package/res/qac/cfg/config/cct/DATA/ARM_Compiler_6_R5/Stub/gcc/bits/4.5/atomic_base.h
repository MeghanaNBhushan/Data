#ifndef PRLGCC_INCLUDED_ATOMIC_BASE
#define PRLGCC_INCLUDED_ATOMIC_BASE

#if defined (PRL_GCC_01)
#  define ATOMIC_FLAG_INIT ( false )
#  if ((__QACPP_MAJOR__ > 32) || ((__QACPP_MAJOR__ == 32) && (__QACPP_MINOR__ >= 2)))
#    define ATOMIC_FLAG_INIT _ignore_modification
#  endif
#endif

#include_next "bits/atomic_base.h"

#endif
