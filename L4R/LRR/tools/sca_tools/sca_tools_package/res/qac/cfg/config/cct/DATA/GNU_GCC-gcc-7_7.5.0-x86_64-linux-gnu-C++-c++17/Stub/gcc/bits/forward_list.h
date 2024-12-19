// forward_list.h
//

#ifndef INCLUDED_PRLGCC_FORWARD_LIST_H
#define INCLUDED_PRLGCC_FORWARD_LIST_H

#include <bits/prlgcc_c++config.h>

#if defined (__PRL_GLIBCXX__)

#  if (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 4)

#    include <bits/4.4/forward_list.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 5)

#    include <bits/4.8/forward_list.h>

#  elif (__PRL_GLIBCXX__ == 4) && (__PRL_GLIBCXX_MINOR__ == 6)

#    include <bits/4.9/forward_list.h>

#  else

#    include_next <bits/forward_list.h>

#  endif

#else

#  include_next <bits/forward_list.h>

#endif

#endif
