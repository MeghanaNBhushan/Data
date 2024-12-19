// basic_string.h
//

#ifndef INCLUDED_PRLGCC_BASIC_STRING_H
#define INCLUDED_PRLGCC_BASIC_STRING_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 9)

#    include <bits/4.9/basic_string.h>

#  else

#    include_next <bits/basic_string.h>

#  endif

#else

#  include_next <bits/basic_string.h>

#endif

#endif
