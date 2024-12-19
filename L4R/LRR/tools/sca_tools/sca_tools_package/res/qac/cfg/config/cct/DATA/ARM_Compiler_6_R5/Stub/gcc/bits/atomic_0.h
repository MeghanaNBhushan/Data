// atomic_0.h
//

#ifndef INCLUDED_PRLGCC_ATOMIC_0_H
#define INCLUDED_PRLGCC_ATOMIC_0_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 4)

#    include <bits/4.4/atomic_0.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 5)

#    include <bits/4.5/atomic_0.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 6)

#    include <bits/4.6/atomic_0.h>

#  else

#    include_next <bits/atomic_0.h>

#  endif

#else

#  include_next <bits/atomic_0.h>

#endif

#endif
