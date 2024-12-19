// move.h
//

#ifndef PRLGCC_INCLUDED_47_MOVE
#define PRLGCC_INCLUDED_47_MOVE

#include_next <bits/move.h>

//
// Wrapper for calls to swap due to late parsing of member exception
// specifications. (PR-21835).
namespace std
{
  template < typename _Tp > 
  inline void __qacpp_swap__ ( _Tp & __a , _Tp & __b ) noexcept ( noexcept (swap (__a, __b)) )
  {
    swap (__a, __b);
  }
}


#endif
