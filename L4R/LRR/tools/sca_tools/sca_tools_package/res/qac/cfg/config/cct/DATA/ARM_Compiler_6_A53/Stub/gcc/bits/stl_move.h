// stl_move.h
//

#ifndef INCLUDED_PRLGCC_STL_MOVE
#define INCLUDED_PRLGCC_STL_MOVE

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ <= 2)

#    include <bits/4.1/stl_move.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 2)

#    include <bits/4.3/stl_move.h>

#  else

#    include_next <bits/stl_move.h>

#  endif

#else

#  include_next <bits/stl_move.h>

#endif

#endif
