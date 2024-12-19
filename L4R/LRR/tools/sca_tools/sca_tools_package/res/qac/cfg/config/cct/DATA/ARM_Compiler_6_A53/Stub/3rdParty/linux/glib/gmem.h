// gmem.h
//

#ifndef PRLGCC_INCLUDED_GMEM
#define PRLGCC_INCLUDED_GMEM

#include_next <glib/gmem.h>

#if defined (PRL_GCC_07)

#  if defined (_G_NEW)
#    undef _G_NEW
#    define  _G_NEW(struct_type, n_structs, func) \
        ((struct_type *) g_##func##_n ((n_structs), sizeof (struct_type)))
#  endif

#  if defined (_G_RENEW)
#    undef _G_RENEW
#    define _G_RENEW(struct_type, mem, n_structs, func) \
        ((struct_type *) g_##func##_n (mem, (n_structs), sizeof (struct_type)))
#  endif

#endif  // PRL_GCC_07

#endif  // PRLGCC_INCLUDED_GMEM
