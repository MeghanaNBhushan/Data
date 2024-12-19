// bits/byteswap.h
//

#ifndef PRLGCC_INCLUDED_BITS_BYTESWAP
#define PRLGCC_INCLUDED_BITS_BYTESWAP

#include_next "bits/byteswap.h"

#if defined (PRL_GCC_07)

#  if defined(__bswap_16)
#    undef __bswap_16
#    define __bswap_16(x) __bswap_constant_16(x)
#  endif

#  if defined(__bswap_32)
#    undef __bswap_32
#    define __bswap_32(x) __bswap_constant_32(x)
#  endif

#  if defined(__bswap_64)
#    undef __bswap_64
#    define __bswap_64(x) __bswap_constant_64(x)
#  endif

#  endif // defined (PRL_GCC_07)

#endif // PRLGCC_INCLUDED_BITS_BYTESWAP
