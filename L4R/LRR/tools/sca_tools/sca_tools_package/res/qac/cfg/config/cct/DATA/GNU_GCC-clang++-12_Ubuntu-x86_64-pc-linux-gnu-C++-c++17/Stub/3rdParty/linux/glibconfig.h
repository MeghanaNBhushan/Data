// glibconfig.h
//

#ifndef PRLGCC_INCLUDED_GLIBCONFIG
#define PRLGCC_INCLUDED_GLIBCONFIG

#include_next <glibconfig.h>

#if defined (PRL_GCC_07)
#  if defined (G_ATOMIC_LOCK_FREE)
#    undef G_ATOMIC_LOCK_FREE
#  endif
#endif

#endif
