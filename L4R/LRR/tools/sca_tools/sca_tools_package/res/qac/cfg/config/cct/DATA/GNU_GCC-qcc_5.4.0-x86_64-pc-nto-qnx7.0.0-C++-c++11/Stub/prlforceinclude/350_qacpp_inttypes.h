// qacpp_inttypes.h
//

#ifndef PRLGCC_INCLUDED_QACPP_INTTYPES
#define PRLGCC_INCLUDED_QACPP_INTTYPES


namespace QACPP_TypeSizeHelper
{
  template <typename Type> struct Def;

  // Dummy Placeholder type for when the size is not an exact match for a type setting
  template <> struct Def<void> {
    typedef signed int INT_TYPE;
    typedef unsigned int UINT_TYPE;
    static const unsigned int size = 0;
  };
  
  template <> struct Def<long long> {
    typedef signed long long INT_TYPE;
    typedef unsigned long long UINT_TYPE;
    static const unsigned long long size = sizeof(long long)*8;
    typedef Def<void> NEXT_TYPE;
  };

  template <> struct Def<long> {
    typedef signed long INT_TYPE;
    typedef unsigned long UINT_TYPE;
    static const unsigned long size = sizeof(long)*8;
    typedef Def<long long> NEXT_TYPE;
  };

  template <> struct Def<int> {
    typedef signed int INT_TYPE;
    typedef unsigned int UINT_TYPE;
    static const unsigned int size = sizeof(int)*8;
    typedef Def<long> NEXT_TYPE;
  };

  template <> struct Def<short> {
    typedef signed short INT_TYPE;
    typedef unsigned short UINT_TYPE;
    static const unsigned int size = sizeof(short)*8;
    typedef Def<int> NEXT_TYPE;
  };

  template <> struct Def<char> {
    typedef signed char INT_TYPE;
    typedef unsigned char UINT_TYPE;
    static const unsigned int size = sizeof(char)*8;
    typedef Def<short> NEXT_TYPE;
  };


  //
  // Search for the type that matches the number of bits specified.
  // Will use sizes for 'int' if one cannot be found.
  template <typename Def, unsigned int S, unsigned int N> struct Search {
    typedef typename Def::NEXT_TYPE NEXT_TYPE;
    typedef typename Search <NEXT_TYPE, NEXT_TYPE::size, N>::TYPE TYPE;
  };

  template <unsigned int S, unsigned int N> struct Search <Def<void>, S, N> {
    typedef Def<void> TYPE;
  };

  template <typename Def, unsigned int S> struct Search <Def, S, S> {
    typedef Def TYPE;
  };
}

# define __intN_t(N, MODE) \
  typedef QACPP_TypeSizeHelper::Search <QACPP_TypeSizeHelper::Def<char>            \
                                        , QACPP_TypeSizeHelper::Def<char>::size    \
                                        , N>::TYPE::INT_TYPE int##N##_t;

# define __u_intN_t(N, MODE) \
  typedef QACPP_TypeSizeHelper::Search <QACPP_TypeSizeHelper::Def<char>            \
                                        , QACPP_TypeSizeHelper::Def<char>::size    \
                                        , N>::TYPE::UINT_TYPE u_int##N##_t;


template < typename Kind, typename IntegralType, typename PromType >
struct __qacpp_integral_type_prom_type {
  typedef IntegralType type;
};

template < typename Kind, typename PromType >
struct __qacpp_integral_type {

  typedef __qacpp_integral_type<Kind, PromType> self;
  typedef typename __qacpp_integral_type_prom_type<Kind, self, PromType> :: type ArithOpResultType;

  __qacpp_integral_type ( ) ;
  template <typename T> __qacpp_integral_type ( T ) ;
     
  template <typename T> operator T ( ) const ;
  template <typename T> operator T& ( ) ;
     
  friend bool                operator <   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend bool                operator <=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend bool                operator >   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend bool                operator >=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend bool                operator ==  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend bool                operator !=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  
  friend ArithOpResultType            operator -   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend ArithOpResultType            operator +   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend ArithOpResultType            operator *   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend ArithOpResultType            operator /   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend ArithOpResultType            operator %   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  
  friend ArithOpResultType            operator &   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend ArithOpResultType            operator |   ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend ArithOpResultType            operator <<  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend ArithOpResultType            operator >>  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
     
  friend __qacpp_integral_type & operator -=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend __qacpp_integral_type & operator +=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend __qacpp_integral_type & operator *=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend __qacpp_integral_type & operator /=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend __qacpp_integral_type & operator %=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  
  friend __qacpp_integral_type & operator &=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend __qacpp_integral_type & operator |=  ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend __qacpp_integral_type & operator <<= ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;
  friend __qacpp_integral_type & operator >>= ( __qacpp_integral_type const &, __qacpp_integral_type const & ) ;

  ArithOpResultType                   operator ~   ( ) const ;
  ArithOpResultType                   operator -   ( ) const ;
  ArithOpResultType                   operator +   ( ) const ;
  bool                       operator !   ( ) const ;

  __qacpp_integral_type &        operator++() const ;
  __qacpp_integral_type          operator++(int) const ;
  __qacpp_integral_type &        operator--() const ;
  __qacpp_integral_type          operator--(int) const ;
     
} ;

#if (__QACPP_MAJOR__ < 41)

class __qacpp_char16_type;
class __qacpp_char32_type;

template < typename IntegralType, typename PromType >
struct __qacpp_integral_type_prom_type<__qacpp_char16_type, IntegralType, PromType> { typedef PromType type; };

template < typename IntegralType, typename PromType >
struct __qacpp_integral_type_prom_type<__qacpp_char32_type, IntegralType, PromType> { typedef PromType type; };

typedef __qacpp_integral_type < __qacpp_char16_type, int > char16_t ;
typedef __qacpp_integral_type < __qacpp_char32_type, int > char32_t ;

#endif

// PR-25924:  Very limited support for the 128 bit types. (see also -cre in ver-all.ext)
typedef __qacpp_integral_type < class __qacpp_int128_type, long long > __int128 ;
typedef __qacpp_integral_type < class __qacpp_uint128_type, unsigned long long > __qacpp_uint128 ;
typedef __int128 __int128_t;
typedef __qacpp_uint128 __uint128_t;

#endif
