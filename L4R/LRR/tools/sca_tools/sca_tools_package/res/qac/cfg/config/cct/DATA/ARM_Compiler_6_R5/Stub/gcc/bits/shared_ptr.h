// shared_ptr.h
//

#ifndef INCLUDED_PRLGCC_SHARED_PTR_H
#define INCLUDED_PRLGCC_SHARED_PTR_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 4)

#    include <bits/4.4/shared_ptr.h>

#  else

#    include_next <bits/shared_ptr.h>

#  endif

#else

#  include_next <bits/shared_ptr.h>

#endif

#endif
