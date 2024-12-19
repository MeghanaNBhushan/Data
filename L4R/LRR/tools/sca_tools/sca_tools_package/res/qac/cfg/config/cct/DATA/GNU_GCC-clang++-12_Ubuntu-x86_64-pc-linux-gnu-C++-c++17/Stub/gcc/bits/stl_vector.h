// stl_vector.h
//

#ifndef INCLUDED_PRLGCC_STL_VECTOR_H
#define INCLUDED_PRLGCC_STL_VECTOR_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 3)

#    include <bits/4.3/stl_vector.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 4)

#    include <bits/4.4/stl_vector.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 7)

#    include <bits/4.7/stl_vector.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 8)

#    include <bits/4.8/stl_vector.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 9)

#    include <bits/4.9/stl_vector.h>

#  else

#    include_next <bits/stl_vector.h>

#  endif

#else

#  include_next <bits/stl_vector.h>

#endif

#endif
