// alloc_traits.h
//

#ifndef INCLUDED_PRLGCC_ALLOC_TRAITS_H
#define INCLUDED_PRLGCC_ALLOC_TRAITS_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 7)

#    include <bits/4.7/alloc_traits.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 8)

#    include <bits/4.8/alloc_traits.h>

#  else

#    include_next <bits/alloc_traits.h>

#  endif

#else

#  include_next <bits/alloc_traits.h>

#endif

#endif
