// gthread.h
//

#ifndef PRLGCC_INCLUDED_GTHREAD
#define PRLGCC_INCLUDED_GTHREAD

#include_next "glib/gthread.h"

#if defined (PRL_GCC_07)

#  if defined (g_once_init_enter)
#    undef g_once_init_enter
#    define g_once_init_enter(location) \
       (g_once_init_enter((location)))
#  endif // g_once_init_leave

#  if defined (g_once_init_leave)
#    undef g_once_init_leave
#    define g_once_init_leave(location, result) \
      (g_once_init_leave((location), (gsize) (result)))
#  endif // g_once_init_leave

#endif

#endif
