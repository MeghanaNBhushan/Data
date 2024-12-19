// gtypes.h
//

#ifndef PRLGCC_INCLUDED_GTYPES
#define PRLGCC_INCLUDED_GTYPES

#include_next <glib/gtypes.h>

#if defined (PRL_GCC_07)

#    if defined (GUINT32_SWAP_LE_BE)
#      undef GUINT32_SWAP_LE_BE
#      define GUINT32_SWAP_LE_BE(val) ((guint32) __builtin_bswap32 ((gint32) (val)))
#    endif

#    if defined (GUINT64_SWAP_LE_BE)
#      undef GUINT64_SWAP_LE_BE
#      define GUINT64_SWAP_LE_BE(val) ((guint64) __builtin_bswap64 ((gint64) (val)))
#    endif

#endif // PRL_GCC_07

#endif // PRLGCC_INCLUDED_GTYPES
