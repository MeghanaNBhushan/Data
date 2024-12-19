//
// PRQA edits
//

// $ used in identifiers
#define PRL_001 1

// using a class before it is defined
#define PRL_002 1

// __if_not_exists
#define PRL_003 1

// '[ ... ]' in a header file at global scope - .Net attribute
#define PRL_004 1

// overloading on calling convention, e.g. __cdecl, __stdcall
#define PRL_006 1


#ifdef PRL_002
class type_info;
#endif // PRL_002

#ifdef PRL_003
#define BEGIN_PROPERTY_MAP(theClass) \
   typedef ATL::_ATL_PROP_NOTIFY_EVENT_CLASS __ATL_PROP_NOTIFY_EVENT_CLASS; \
   typedef theClass _PropMapClass; \
   static const ATL::ATL_PROPMAP_ENTRY* GetPropertyMap()\
   {\
      static const ATL::ATL_PROPMAP_ENTRY pPropMap[] = \
      { \
         {OLESTR("_cx"), 0, &CLSID_NULL, NULL, offsetof(_PropMapClass, m_sizeExtent.cx), sizeof(long), VT_UI4}, \
         {OLESTR("_cy"), 0, &CLSID_NULL, NULL, offsetof(_PropMapClass, m_sizeExtent.cy), sizeof(long), VT_UI4},

#define DECLARE_REGISTRY_RESOURCEID(x)\
   static HRESULT WINAPI UpdateRegistry(BOOL bRegister) throw()\
   {\
      __if_exists(_GetMiscStatus) \
      { \
         ATL::_ATL_REGMAP_ENTRY regMapEntries[2]; \
         memset(&regMapEntries[1], 0, sizeof(ATL::_ATL_REGMAP_ENTRY)); \
         regMapEntries[0].szKey = L"OLEMISC"; \
         TCHAR szOleMisc[32]; \
         ATL::Checked::itot_s(_GetMiscStatus(), szOleMisc, _countof(szOleMisc), 10); \
         USES_CONVERSION_EX; \
         regMapEntries[0].szData = T2OLE_EX(szOleMisc, _ATL_SAFE_ALLOCA_DEF_THRESHOLD); \
         if (regMapEntries[0].szData == NULL) \
            return E_OUTOFMEMORY; \
         __if_exists(_Module) \
         { \
            return _Module.UpdateRegistryFromResource(x, bRegister, regMapEntries); \
         } \
         __if_not_exists(_Module) \
         { \
            return ATL::_pAtlModule->UpdateRegistryFromResource(x, bRegister, regMapEntries); \
         } \
      } \
         __if_exists(_Module) \
         { \
            return _Module.UpdateRegistryFromResource(x, bRegister); \
         } \
                return ATL::_pAtlModule->UpdateRegistryFromResource(x, bRegister); \
    }

#define BEGIN_CONNECTION_POINT_MAP(x)\
      typedef x _atl_conn_classtype;\
   static const ATL::_ATL_CONNMAP_ENTRY* GetConnMap(int* pnEntries) {\
   static const ATL::_ATL_CONNMAP_ENTRY _entries[] = {

#define BEGIN_PROP_MAP(theClass) \
      typedef ATL::_ATL_PROP_NOTIFY_EVENT_CLASS __ATL_PROP_NOTIFY_EVENT_CLASS; \
   typedef theClass _PropMapClass; \
   static const ATL::ATL_PROPMAP_ENTRY* GetPropertyMap()\
   {\
      static const ATL::ATL_PROPMAP_ENTRY pPropMap[] = \
      {

#define END_CONNECTION_POINT_MAP() \
   __if_exists(GetAttrConnMap) \
   { \
      {(DWORD_PTR) -2}, \
      {(DWORD_PTR) GetAttrConnMap }, \
   } \
   {(DWORD_PTR)-1} }; \
   if (pnEntries) \
   { \
      __if_exists(GetAttrConnMap) \
      { \
         GetAttrConnMap(pnEntries); \
         *pnEntries += sizeof(_entries)/sizeof(ATL::_ATL_CONNMAP_ENTRY) - 3; \
      } \
      *pnEntries = sizeof(_entries)/sizeof(ATL::_ATL_CONNMAP_ENTRY) - 1; \
   } \
   return _entries;}
#endif  // PRL_003

// UTF-8 preamble in .tlh files, QAC++ treats it as a token
#define ﻿ _prl_ignore token
#define _prl_ignore _ignore

// intrinsic function from intrin.h
extern "C" void __debugbreak(void);

// use of incomplete enum type to declare enumerator
#define GDIP_WMF_RECORD_TO_EMFPLUS(n) ((n) | GDIP_WMF_RECORD_BASE)

#if _MSC_VER >= 1913
#define _EMIT_CLRCALL(FUNC, OPT1, OPT2, OPT3)
#define _EMIT_FASTCALL(FUNC, OPT1, OPT2, OPT3)
#define _EMIT_STDCALL(FUNC, OPT1, OPT2, OPT3)
#define _EMIT_THISCALL(FUNC, OPT1, OPT2, OPT3)
#define _EMIT_VECTORCALL(FUNC, OPT1, OPT2, OPT3)
#else
#define _EMIT_CLRCALL(FUNC, OPT1, OPT2)
#define _EMIT_FASTCALL(FUNC, OPT1, OPT2)
#define _EMIT_STDCALL(FUNC, OPT1, OPT2)
#define _EMIT_THISCALL(FUNC, OPT1, OPT2)
#define _EMIT_VECTORCALL(FUNC, OPT1, OPT2)
#endif


// type traits
#define __is_constructible(X, ...) (::__qacpp_helpers::is_constructible<X, ## __VA_ARGS__>::value)
#define __is_trivially_constructible(X, ...) (__is_constructible(X, ## __VA_ARGS__) && __qacpp_is_trivially_constructible(X, ## __VA_ARGS__))
#define __is_destructible(X) (::__qacpp_helpers::is_destructible<X>::value)
#define __is_trivially_assignable(X,Y) __qacpp_is_trivially_assignable(X, Y)
#define __is_assignable(X,Y) (::__qacpp_helpers::is_assignable<X, Y>::value)
#define __is_nothrow_constructible(x,...) true
#define __is_nothrow_assignable(x,y) true
#define __is_nothrow_destructible(x) true
#define __is_trivially_destructible(T) (::__qacpp_helpers::is_trivially_destructible<T>::value)
#define __has_trivial_destructor(T) (::__qacpp_helpers::is_trivially_destructible<T>::value)
#define __has_unique_object_representations(x) true

#define _DEPRECATE_TR1_NAMESPACE


namespace __qacpp_helpers
{
  struct __yes_type { char c[1]; };
  struct __no_type { char c[2]; };

  template <class T, T v> struct integral_constant
  {
    static const T value = v;
    typedef T value_type;
    typedef integral_constant<T,v> type;
    operator value_type() { return value; }
  };

  typedef integral_constant<bool, true> true_type;
  typedef integral_constant<bool, false> false_type;

  template <class T> struct is_lvalue_reference : false_type { };
  template <class T> struct is_lvalue_reference<T &> : true_type { };

  template <class T> struct is_rvalue_reference : false_type { };
  template <class T> struct is_rvalue_reference<T &&> : false_type { };

  template <class T> struct is_reference : integral_constant<bool, is_lvalue_reference<T>::value || is_rvalue_reference<T>::value> { };

  template <class __type>
  struct add_rvalue_reference
  {
    typedef __type && type;
  };

  template<typename T>
  typename add_rvalue_reference<T>::type declval() noexcept;

  template<typename T>
  struct remove_all_extents
  {
    typedef T type;
  };

  template<typename T, PRQA_SIZE_T s>
  struct remove_all_extents<T[s]>
  {
    typedef typename remove_all_extents<T>::type type;
  };

  template<typename T>
  struct remove_all_extents<T[]>
  {
    typedef typename remove_all_extents<T>::type type;
  };

  template <class T> struct remove_cv { typedef T type; };
  template <class T> struct remove_cv<T const> { typedef T type; };
  template <class T> struct remove_cv<T volatile> { typedef T type; };
  template <class T> struct remove_cv<T const volatile> { typedef T type; };

  struct __is_destructible_impl
  {
    template<typename T, typename = decltype(declval<T&>().~T())>
    static __yes_type test(int);
    template<typename>
    static __no_type test(...);
  };

  template <class T> struct is_destructible
    : public integral_constant<bool, is_reference<T>::value
                               || sizeof(__is_destructible_impl::test<typename remove_all_extents<T>::type>(0)) == sizeof(__yes_type)>
  { };

  template <class T> struct is_trivially_destructible
    : public integral_constant<bool, is_destructible<T>::value
                               && (!__qacpp_is_class(typename remove_all_extents<T>::type)
                                   || __qacpp_has_trivial_destructor(typename remove_all_extents<T>::type))>
  { };

  struct __is_default_constructible_impl
  {
    template<typename _Tp, typename = decltype(_Tp())>
    static __yes_type test(int);

    template<typename>
    static __no_type test(...);
  };

  template <class T> struct is_default_constructible : public integral_constant<bool, sizeof(__is_default_constructible_impl::test<T>(0)) == sizeof(__yes_type)> { };
  template <class T, PRQA_SIZE_T N> struct is_default_constructible<T[N]> : public is_default_constructible<T> { };
  template <class T> struct is_default_constructible<T[]> : public is_default_constructible<T> { };
  template <class T> struct is_default_constructible<T&> : public integral_constant<bool, false> { };
  template <class T> struct is_default_constructible<T&&> : public integral_constant<bool, false> { };
  template <> struct is_default_constructible<void> : public integral_constant<bool, false> { };
  template <> struct is_default_constructible<void const> : public integral_constant<bool, false> { };
  template <> struct is_default_constructible<void volatile> : public integral_constant<bool, false> { };
  template <> struct is_default_constructible<void const volatile> : public integral_constant<bool, false> { };


  struct __is_constructible_impl
  {
    template<typename T, typename ...TheArgs, typename = decltype(T(declval<TheArgs>()...))>
    static __yes_type test(int);
    template<typename, typename...>
    static __no_type test(...);

    template<typename T, typename Arg, typename = decltype(::new T(declval<Arg>()))>
    static __yes_type test1(int);
    template<typename, typename>
    static __no_type test1(...);

    template <typename T>
    static __yes_type ref_test(T);
    template <typename T>
    static __no_type ref_test(...);
  };

  template <class T, class ...Args> struct is_constructible : public integral_constant<bool, sizeof(__is_constructible_impl::test<T, Args...>(0)) == sizeof(__yes_type)> { };
  template <class T, class Arg> struct is_constructible<T, Arg> : public integral_constant<bool, is_destructible<T>::value && sizeof(__is_constructible_impl::test1<T, Arg>(0)) == sizeof(__yes_type)> { };
  template <class Ref, class Arg> struct is_constructible<Ref&, Arg> : public integral_constant<bool, sizeof(__is_constructible_impl::ref_test<Ref&>(declval<Arg>())) == sizeof(__yes_type)> { };
  template <class Ref, class Arg> struct is_constructible<Ref&&, Arg> : public integral_constant<bool, sizeof(__is_constructible_impl::ref_test<Ref&&>(declval<Arg>())) == sizeof(__yes_type)> { };

  template <> struct is_constructible<void> : public false_type{};
  template <> struct is_constructible<void const> : public false_type{};
  template <> struct is_constructible<void const volatile> : public false_type{};
  template <> struct is_constructible<void volatile> : public false_type{};

  template <class T> struct is_constructible<T> : public is_default_constructible<T>{};


  struct __is_assignable_impl
  {
    template<typename _T1, typename _T2,
             typename = decltype(declval<_T1>() = declval<_T2	>())>
    static __yes_type test(int);

    template<typename, typename>
    static __no_type test(...);
  };

  template<typename _T1, typename _T2>
  struct is_assignable : public integral_constant<bool, sizeof(__is_assignable_impl::test<_T1, _T2>(0)) == sizeof(__yes_type)> { };
}


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

template<typename _Tp>
_Tp* __builtin_addressof(_Tp&) noexcept;

#define __COUNTER__ __PRQA_COUNTER__

// builtins used by limits header
#define __builtin_huge_val() HUGE_VAL
#define __builtin_huge_valf() HUGE_VALF
#define __builtin_nan nan
#define __builtin_nanf nanf
#define __builtin_nans nan
#define __builtin_nansf nanf

// builtins used by iosfwd header
#define __builtin_wmemchr std::wmemchr
#define __builtin_wmemcmp std::wmemcmp
#define __builtin_wcslen std::wcslen
#define __builtin_memcmp std::memcmp
#define __builtin_strlen std::strlen
#define __builtin_char_memchr(_T1,_T2,_T3) static_cast<const char *>(std::memchr(_T1,_T2,_T3))

#define _ALLOW_KEYWORD_MACROS

#define offsetof __qacpp_offsetof

#define __STDCPP_DEFAULT_NEW_ALIGNMENT__ sizeof(double)

inline constexpr char operator ""i8 (unsigned long long val)
{
  return val;
}

inline constexpr unsigned char operator ""ui8 (unsigned long long val)
{
  return val;
}

inline constexpr short operator ""i16 (unsigned long long val)
{
  return val;
}

inline constexpr unsigned short operator ""ui16 (unsigned long long val)
{
  return val;
}

inline constexpr int operator ""i32 (unsigned long long val)
{
  return val;
}

inline constexpr unsigned int operator ""ui32 (unsigned long long val)
{
  return val;
}
