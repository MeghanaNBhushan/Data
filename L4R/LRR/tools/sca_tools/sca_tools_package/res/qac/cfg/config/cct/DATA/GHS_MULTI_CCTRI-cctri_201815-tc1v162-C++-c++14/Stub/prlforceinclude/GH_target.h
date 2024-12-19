#ifndef GH_TARGET_CPP_FI_H
#define GH_TARGET_CPP_FI_H

#if __cplusplus > 199711L
#define _HAS_NOEXCEPT 1
#endif

/* intrinsics */
void __DI(void);
void __EI(void);
int __builtin_va_alist;
int __builtin_va_arg_incr(...);
int __va_aargnum(...);
int __va_ansiarg;
int __va_dargnum(...);
int __va_iargnum(...);
int __va_intreg;
int *__va_stkarg;

unsigned int __CLZ32(unsigned int);
unsigned int __GETSR(void);
int __MULSH(int, int);
unsigned int __MULUH(unsigned int, unsigned int);
void __PUTSR(unsigned int);
void __SETSR(unsigned int);

#define __noinline
#define __linkonce
#define __bytereversed
#define __bigendian
#define __littleendian
#define __packed
#define __nearcall
#define __farcall
#if defined(__V800__)
#define __callt
#endif

// TR1 functions 
#define __has_nothrow_assign(x)                   __qacpp_has_nothrow_assign(x)
#define __has_nothrow_constructor(x)              __qacpp_has_nothrow_constructor(x)
#define __has_nothrow_copy(x)                     __qacpp_has_nothrow_copy(x)
#define __has_trivial_assign(x)                   __qacpp_has_trivial_assign(x)
#define __has_trivial_constructor(x)              __qacpp_has_trivial_constructor(x)
#define __has_trivial_copy(x)                     __qacpp_has_trivial_copy(x)
#define __has_trivial_destructor(x)               __qacpp_has_trivial_destructor(x)
#define __has_virtual_destructor(x)               __qacpp_has_virtual_destructor(x)
#define __is_aggregate(x)                         __qacpp_is_aggregate(x)
#define __is_abstract(x)                          __qacpp_is_abstract(x)
#define __is_base_of(x,y)                         __qacpp_is_base_of(x,y)
#define __is_class(x)                             __qacpp_is_class(x)
#define __is_convertible_to(x,y)                  __qacpp_is_convertible(x,y)
#define __is_empty(x)                             __qacpp_is_empty(x)
#define __is_enum(x)                              __qacpp_is_enum(x)
#define __is_pod(x)                               __qacpp_is_pod(x)
#define __is_polymorphic(x)                       __qacpp_is_polymorphic(x)
#define __is_union(x)                             __qacpp_is_union(x)
#define __is_standard_layout(x)                   __qacpp_is_standard_layout(x)

#define __has_assign(x)                           false
#define __has_copy(x)                             false
#define __has_finalizer(x)                        false
#define __has_user_destructor(x)                  false
#define __is_delegate(x)                          false
#define __is_interface_class(x)                   false
#define __is_ref_array(x)                         false
#define __is_ref_class(x)                         false
#define __is_sealed(x)                            false
#define __is_simple_value_class(x)                false
#define __is_value_class(x)                       false
#define __must_be_array(x)                        false

#if (__QACPP_MAJOR__ < 40)
#define __underlying_type(x)                      __qacpp_underlying_type(x)
#else
#define __underlying_type(x)                      int
#endif
#define __has_unique_object_representations(x)    __is_trivially_copyable(x)
#define _Pragma(x)

#if (__QACPP_MAJOR__ < 42)
#define __is_literal_type(x)                      false
#else
#define __is_literal_type(x)                      __qacpp_is_literal(x)
#endif
#define __is_literal(x)                           __is_literal_type(x)

#if (__QACPP_MAJOR__ < 42)
#define __is_trivial(x)                           (__has_trivial_constructor(x) && __has_trivial_copy(x) && __has_trivial_destructor(x))
#define __is_trivially_copyable(x)                (__has_trivial_copy(x) && __has_trivial_destructor(x))
#define __is_trivially_constructible(x,y)         false
#define __is_trivially_assignable(x,y)            false
#else
#define __is_trivial(x)                           __qacpp_is_trivial(x)
#define __is_trivially_copyable(x)                __qacpp_is_trivially_copyable(x)
#define __is_trivially_constructible(x,y)         __qacpp_is_trivially_constructible(x, y)
#define __is_trivially_assignable(x,y)            __qacpp_is_trivially_assignable(x, y)
#endif

#if (__QACPP_MAJOR__ < 42)
#define __is_final(x)                             false
#else
#define __is_final(x)                             __qacpp_is_final(x)
#endif
#if (__QACPP_MAJOR__ < 40)
#define __underlying_type(x)                      int
#else
#define __underlying_type(x)                      __qacpp_underlying_type(x)
#endif
#if (__QACPP_MAJOR__ < 42)
#define static_assert                             _ignore_semi
#endif

// Below added for operation with comp_201814/scxx C++11/14

// Taken from PRQA_Generic_C++ utility
  template <class T> struct add_rvalue_reference { typedef T &&type; };

  template <class T>
  using add_rvalue_reference_t = typename add_rvalue_reference<T>::type;

  template <class T>
  add_rvalue_reference_t<T> declval() noexcept;

// Types not implemented by qacpp
template <class T> struct is_copy_assignable;
template <class T> struct is_move_assignable;
template <class T> struct is_trivially_default_constructible;
template <class T> struct is_trivially_destructible;
template <class T, class ... Args> struct is_nothrow_constructible;
template <class T> struct is_nothrow_default_constructible;
template <class T> struct is_nothrow_copy_constructible;
template <class T> struct is_nothrow_move_constructible;
template <class T, class U> struct is_nothrow_assignable;
template <class T> struct is_nothrow_copy_assignable;
template <class T> struct is_nothrow_move_assignable;
template <class T> struct is_nothrow_destructible;

template <class T> struct is_function;

// Types defined in scxx/type_traits but not enabled by preprocessing
template< class... >
using void_t = void;

template< class T >
struct decay;
template< class T >
using decay_t = typename decay<T>::type;

        // TEMPLATE CLASS make_unsigned
template<class _Ty>
        struct make_unsigned;
template<class _Ty>
        using make_unsigned_t = typename make_unsigned<_Ty>::type;

template <class T> struct remove_const;
template<class _Ty>
        using remove_const_t = typename remove_const<_Ty>::type;

        // TEMPLATE CLASS remove_pointer
template<class _Ty>
        struct remove_pointer;
template<class _Ty>
        using remove_pointer_t = typename remove_pointer<_Ty>::type;

#if __cplusplus >= 201703L
// C++17 updates

// To work around parse errors in scxx/random. Requires furhter investigation.
#define _RANDOM_

// builtin function used
int __builtin_wmemcmp(const wchar_t *, const wchar_t *, PRQA_SIZE_T);
PRQA_SIZE_T __builtin_wcslen(const wchar_t *);
const wchar_t *__builtin_wmemchr(const wchar_t *, wchar_t, PRQA_SIZE_T);
int __builtin_memcmp(const void * __M1, const void * __M2, PRQA_SIZE_T __LEN);
PRQA_SIZE_T __builtin_strlen(const char * __STR);
const void *__builtin_char_memchr(const void * __MEM, int __CH, PRQA_SIZE_T __n );
#endif

#if defined(__CORE_V850E3V5__) && defined(__RH850_FXU_TYPES__)
typedef long long __ev128_f32__;
#endif

#if defined(__CORE_V850E3V5__) && defined(__RH850_SIMD_TYPES__)
typedef long long __ev64_u16__;
typedef long long __ev64_s16__;
typedef long long __ev64_u32__;
typedef long long __ev64_s32__;
typedef long long __ev64_u64__;
typedef long long __ev64_s64__;
typedef long long __ev64_opaque__;
typedef long long __ev128_opaque__;
#endif

#if (__QACPP_MAJOR__ < 44)
// C '1x
#define _Pragma                                   _ignore_paren
#endif

// target specific settings
#if defined(__ALTIVEC__)
#define __vector
#endif
 
#else
#error "Multiple include"
#endif  /* ifndef GH_TARGET_CPP_FI_H */

