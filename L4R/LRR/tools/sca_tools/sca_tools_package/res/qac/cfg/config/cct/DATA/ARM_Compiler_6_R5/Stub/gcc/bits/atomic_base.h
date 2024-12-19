// atomic_base.h
//

#ifndef INCLUDED_PRLGCC_ATOMIC_BASE_H
#define INCLUDED_PRLGCC_ATOMIC_BASE_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 5)

#    include <bits/4.5/atomic_base.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 7)

#    include <bits/4.7/atomic_base.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 8)

#    include <bits/4.8/atomic_base.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 9)

#    include <bits/4.9/atomic_base.h>

#  else

#    include_next <bits/atomic_base.h>

#  endif

#else

#  include_next <bits/atomic_base.h>

#endif

#endif
