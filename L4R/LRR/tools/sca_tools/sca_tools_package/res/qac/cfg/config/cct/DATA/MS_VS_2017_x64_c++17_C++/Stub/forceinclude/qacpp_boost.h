// qacpp_boost.h
//

#ifndef INCLUDED_QACPP_BOOST
#define INCLUDED_QACPP_BOOST

#include "boost/config.hpp"
#if defined (BOOST_CONFIG_HPP) && ! defined (BOOST_TYPEOF_EMULATION)
#  define BOOST_TYPEOF_NATIVE
   template<typename __type>
   struct __qacpp_remove_reference
   {
     typedef __type __result;
   };
   template<typename __type>
   struct __qacpp_remove_reference<__type &>
   {
     typedef __type __result;
   };
#  define __typeof__(__expr) __qacpp_remove_reference<decltype((__expr))>::__result
#  define BOOST_TYPEOF_KEYWORD __typeof__

#  define BOOST_TYPEOF_NATIVE_HPP_INCLUDED
#  define BOOST_TYPEOF_MSVC_TYPEOF_IMPL_HPP_INCLUDED
#  include <boost/typeof/typeof.hpp>
#  undef MSVC_TYPEOF_HACK
#  undef BOOST_TYPEOF_NATIVE_HPP_INCLUDED
#  include <boost/typeof/native.hpp>
#endif

#endif
