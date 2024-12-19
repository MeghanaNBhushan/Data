// regex_compiler.h
//

#ifndef INCLUDED_PRLGCC_REGEX_COMPILER_H
#define INCLUDED_PRLGCC_REGEX_COMPILER_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 5)

#    include <bits/5.1/regex_compiler.h>

#  else

#    include_next <bits/regex_compiler.h>

#  endif

#else

#  include_next <bits/regex_compiler.h>

#endif

#endif
