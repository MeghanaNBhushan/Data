// gbitlock.h
//

#ifndef PRLGCC_INCLUDED_GBITLOCK
#define PRLGCC_INCLUDED_GBITLOCK

#include_next <glib/gbitlock.h>

#if defined (PRL_GCC_07)

#  if defined (g_pointer_bit_lock)
#    undef g_pointer_bit_lock
#    define g_pointer_bit_lock(address, lock_bit)          \
        g_pointer_bit_lock ((address), (lock_bit))
#  endif

#  if defined (g_pointer_bit_trylock)
#    undef g_pointer_bit_trylock
#    define g_pointer_bit_trylock(address, trylock_bit)    \
  g_pointer_bit_trylock ((address), (trylock_bit))
#  endif

#  if defined (g_pointer_bit_unlock)
#    undef g_pointer_bit_unlock
#    define g_pointer_bit_unlock(address, unlock_bit)      \
        g_pointer_bit_unlock ((address), (unlock_bit))
#  endif

#endif // PRL_GCC_07

#endif // PRLGCC_INCLUDED_GBITLOCK
