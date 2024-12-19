// parse_numbers.h
//

#ifndef INCLUDED_PRLGCC_PARSE_NUMBERS_H
#define INCLUDED_PRLGCC_PARSE_NUMBERS_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 9)

#    include <bits/4.9/parse_numbers.h>

#  else

#    include_next <bits/parse_numbers.h>

#  endif

#else

#  include_next <bits/parse_numbers.h>

#endif

#endif
