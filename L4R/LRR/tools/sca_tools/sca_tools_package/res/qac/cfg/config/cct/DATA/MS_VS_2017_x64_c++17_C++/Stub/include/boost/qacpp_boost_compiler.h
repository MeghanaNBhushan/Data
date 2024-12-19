// qacpp_boost_compiler.h
//

#ifndef INCLUDED_QACPP_BOOST_COMPILER
#define INCLUDED_QACPP_BOOST_COMPILER

#include <boost/version.hpp>

#undef BOOST_COMPILER_CONFIG

#if !defined(BOOST_NO_COMPILER_CONFIG) && !defined(BOOST_NO_CONFIG)
# if BOOST_VERSION >= 106500
#  include <boost/config/detail/select_compiler_config.hpp>
# else
#  include <boost/config/select_compiler_config.hpp>
# endif
#endif

#ifdef BOOST_COMPILER_CONFIG
#  include BOOST_COMPILER_CONFIG
#endif

#if defined (BOOST_MSVC)
// needed when _MSC_EXTENSIONS is not defined
#  undef BOOST_DISABLE_WIN32

// use native auto instead of typeof
#  define BOOST_AUTO(Var, Expr) auto Var = Expr
#  define BOOST_AUTO_TPL BOOST_AUTO

// do not use forward decls in boost/detail/container_fwd.hpp
#  define BOOST_DETAIL_NO_CONTAINER_FWD

#  define BOOST_SCOPE_EXIT_AUX_TYPEOF_THIS_MSVC_WORKAROUND_01 0
#  define BOOST_NO_CXX11_HDR_TUPLE
#elif defined (__GNUC__)
#  define BOOST_NO_EXTERN_TEMPLATE 1
#  define BOOST_ASIO_DISABLE_THREAD_KEYWORD_EXTENSION 1
#endif

#if !defined (__QACPP_MAJOR__)
#  error "only QAC++ 3.0.1 or later supports Boost fully"
#endif

#if __QACPP_MAJOR__ <= 30
#  define BOOST_NO_RVALUE_REFERENCES
#endif

#if __QACPP_MAJOR__ <= 31
#  define BOOST_NO_CXX11_LAMBDAS
#  define BOOST_NO_LAMBDAS
#endif

#if __QACPP_MAJOR__ < 41
#define BOOST_NO_CXX11_UNICODE_LITERALS 1
#define BOOST_NO_CXX11_CHAR32_T 1
#define BOOST_NO_CXX11_CHAR16_T 1
#define BOOST_NO_CXX11_RAW_LITERALS 1
#endif

#if __QACPP_MAJOR__ < 42
#define BOOST_NO_CXX11_DECLTYPE_N3276 1
#define BOOST_NO_CXX11_STATIC_ASSERT 1
#endif

#define BOOST_NO_CXX11_CONSTEXPR 1
#define BOOST_NO_ALIGNMENT 1

// do not use type trait intrinsics in BOOST
#define BOOST_TT_INTRINSICS_HPP_INCLUDED

// force strict pre-processor configuration
#define BOOST_PP_CONFIG_FLAGS() 0x0001
#define BOOST_PP_VARIADICS 0

#endif
