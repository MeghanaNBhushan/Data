// stl_pair.h
//

#ifndef INCLUDED_PRLGCC_STL_PAIR_H
#define INCLUDED_PRLGCC_STL_PAIR_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 3)

#    include <bits/4.3/stl_pair.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 4)

#    include <bits/4.4/stl_pair.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 7)

#    include <bits/4.7/stl_pair.h>

#  elif ( ( (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 8) )   \
    ||  ( (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 9) )     \
    ||    (__PRL_GLIBCXX__ == 5) )

#    include <bits/4.8/stl_pair.h>

#  else

#    include_next <bits/stl_pair.h>

#  endif

#else

#  include_next <bits/stl_pair.h>

#endif

#endif
