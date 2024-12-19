// stl_move.h
//

#ifndef INCLUDED_PRLGCC_STL_MOVE_4_1
#define INCLUDED_PRLGCC_STL_MOVE_4_1

#include_next <bits/stl_move.h>

#include "qacpp_reference_traits.h"

namespace std
{
  template <class T> T&& forward(typename __qacpp_remove_reference<T>::type& t) throw();
}


#endif
