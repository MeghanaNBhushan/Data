// qacpp_type_traits.h
//

#ifndef PRLGCC_INCLUDED_QACPP_TYPE_TRAITS
#define PRLGCC_INCLUDED_QACPP_TYPE_TRAITS

// type traits
#define __is_constructible(X, ...) (::__qacpp_helpers::is_constructible<X, ## __VA_ARGS__>::value)
#define __is_assignable(X,Y) (::__qacpp_helpers::is_assignable<X, Y>::value)

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

  template <class __type>
  struct add_rvalue_reference
  {
    typedef __type && type;
  };

  template<typename T>
  typename add_rvalue_reference<T>::type declval() noexcept;

  struct __is_destructible_impl
  {
    template<typename T, typename = decltype(declval<T&>().~T())>
    static __yes_type test(int);
    template<typename>
    static __no_type test(...);
  };

  template <class T> struct is_destructible : public integral_constant<bool, sizeof(__is_destructible_impl::test<T>(0)) == sizeof(__yes_type)> { };


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

#endif
