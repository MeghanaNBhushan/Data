// hashtable.h
//

#ifndef INCLUDED_PRLGCC_HASHTABLE_H
#define INCLUDED_PRLGCC_HASHTABLE_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 9)

#    include <bits/4.9/hashtable.h>

#  else

#    include_next <bits/hashtable.h>

#  endif

#else

#  include_next <bits/hashtable.h>

#endif

#endif
