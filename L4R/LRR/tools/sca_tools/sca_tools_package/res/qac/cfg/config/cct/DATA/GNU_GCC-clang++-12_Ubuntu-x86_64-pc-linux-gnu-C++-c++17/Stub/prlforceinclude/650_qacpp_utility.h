// qacpp_utility.h
//

#ifndef PRLGCC_INCLUDED_QACPP_UTILITY
#define PRLGCC_INCLUDED_QACPP_UTILITY

#define _GLIBCXX_USE_MAKE_INTEGER_SEQ 1

template<typename _Ty, _Ty ... I>
struct __qacpp_integer_seq
{
  template<_Ty N>
  using append = __qacpp_integer_seq<_Ty, I ..., N>;
  using next = append<sizeof ... (I)>;

  template<template<typename _Ty1, _Ty1 ...> class _V>
  using type = _V<_Ty, I ...>;
};

template<class _Ty, _Ty _Size>
struct __qacpp_make_integer_seq
{
  typedef typename __qacpp_make_integer_seq<_Ty, _Size - 1>::type::next type;
};

template<class _Ty>
struct __qacpp_make_integer_seq<_Ty, 0>
{
  typedef __qacpp_integer_seq<_Ty> type;
};

template<template<typename _Ty1, _Ty1 ...> class _V, class _Ty, _Ty _Size>
using __make_integer_seq =
    typename __qacpp_make_integer_seq<_Ty, _Size>::type::template type<_V>;

#endif
