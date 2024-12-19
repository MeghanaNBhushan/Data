// move.h
//

#ifndef INCLUDED_PRLGCC_MOVE_H
#define INCLUDED_PRLGCC_MOVE_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 4)

#    include <bits/4.4/move.h>

#  elif (((__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ >= 7)) || ((__PRL_GLIBCXX__ == 5)))

#    include <bits/4.7/move.h>

#  else

#    include_next <bits/move.h>

#  endif

#else

#  include_next <bits/move.h>

#endif

#endif
