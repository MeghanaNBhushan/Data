// gmacros.h
//

#ifndef PRLGCC_INCLUDED_GMACROS
#define PRLGCC_INCLUDED_GMACROS

#include_next <glib/gmacros.h>

#if defined (PRL_GCC_07)

#  if defined (G_LIKELY)
#    undef G_LIKELY
#    define G_LIKELY(expr) (expr)
#  endif

#  if defined (G_UNLIKELY)
#    undef G_UNLIKELY
#    define G_UNLIKELY(expr) (expr)
#  endif

#endif  // PRL_GCC_07

#endif  // PRLGCC_INCLUDED_GMACROS
