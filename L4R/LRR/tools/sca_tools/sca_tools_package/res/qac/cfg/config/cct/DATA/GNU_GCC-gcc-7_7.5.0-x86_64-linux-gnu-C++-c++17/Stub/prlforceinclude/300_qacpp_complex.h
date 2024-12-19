// qacpp_complex.h
//

#ifndef PRLGCC_INCLUDED_QACPP_COMPLEX
#define PRLGCC_INCLUDED_QACPP_COMPLEX

//
// For versions of QA C++ from 3.2 onwards, the code-regex option can
// be used to replace __complex__ completely in the source.

template <typename T>
class __qacpp_complex__
{
public:
  __qacpp_complex__();
  __qacpp_complex__(T);
  __qacpp_complex__(T, T);
  __qacpp_complex__(__qacpp_complex__ const & rhs);
  template <typename RHS> __qacpp_complex__(__qacpp_complex__<RHS> const & rhs);
  template <typename RHS> __qacpp_complex__ & operator=(RHS const &);
  template <typename RHS> __qacpp_complex__ & operator-=(RHS const &);
  template <typename RHS> __qacpp_complex__ & operator+=(RHS const &);
  template <typename RHS> __qacpp_complex__ & operator*=(RHS const &);
  template <typename RHS> __qacpp_complex__ & operator/=(RHS const &);
  operator T & ();
  operator T const & () const;
};

__qacpp_complex__<float> operator""fi(const char * s);
__qacpp_complex__<double> operator""i(const char * s);
__qacpp_complex__<long double> operator""Li(const char * s);
__qacpp_complex__<long double> operator""li(const char * s);


#endif
