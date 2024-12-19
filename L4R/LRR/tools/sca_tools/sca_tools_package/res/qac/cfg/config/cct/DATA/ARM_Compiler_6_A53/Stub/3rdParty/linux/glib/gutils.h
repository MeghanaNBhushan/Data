// gutils.h
//

#ifndef PRLGCC_INCLUDED_GUTILS
#define PRLGCC_INCLUDED_GUTILS

#if defined (PRL_GCC_12)
# if defined (__STRICT_ANSI__)
#  undef __STRICT_ANSI__
#  define PRLGCC_STRICT_ANSI_DEFINED
# endif
#endif

#include_next <glib/gutils.h>

#if defined (PRLGCC_STRICT_ANSI_DEFINED)
# define __STRICT_ANSI__ 1
#endif

#endif
