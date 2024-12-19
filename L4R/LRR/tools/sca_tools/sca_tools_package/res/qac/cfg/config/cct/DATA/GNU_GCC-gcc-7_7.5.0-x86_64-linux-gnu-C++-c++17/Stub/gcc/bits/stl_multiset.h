// stl_multiset.h
//

#ifndef INCLUDED_PRLGCC_STL_MULTISET_H
#define INCLUDED_PRLGCC_STL_MULTISET_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (  ( (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 3) )   \
    ||   ( (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 4) ) )

#    include <bits/4.3/stl_multiset.h>

#  else

#    include_next <bits/stl_multiset.h>

#  endif

#else

#  include_next <bits/stl_multiset.h>

#endif

#endif
