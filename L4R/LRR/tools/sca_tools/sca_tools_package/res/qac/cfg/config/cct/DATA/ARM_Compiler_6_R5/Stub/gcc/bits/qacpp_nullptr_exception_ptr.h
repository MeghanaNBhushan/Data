// qacpp_nullptr_exception_ptr.h
//

#ifndef INCLUDED_QACPP_NULLPTR_EXCEPTION_PTR
#define INCLUDED_QACPP_NULLPTR_EXCEPTION_PTR


#if (__QACPP_MAJOR__ < 40) && (__PRL_GLIBCXX__ >= 5)

#if ! defined (PRLGCC_INCLUDED_QACPP_NULLPTR)
#  error "Configuration error, qacpp_nullptr.h should be force included before using this file"
#endif

namespace std 
{
  namespace __exception_ptr
  {
    class exception_ptr;
  }
}

namespace __qacpp_nullptr
{
  bool operator==(std::__exception_ptr::exception_ptr const & , __qacpp_nullptr_t::__qacpp_nullptr_convtype *);
  bool operator==(__qacpp_nullptr_t::__qacpp_nullptr_convtype *, std::__exception_ptr::exception_ptr const & );
  bool operator!=(std::__exception_ptr::exception_ptr const & , __qacpp_nullptr_t::__qacpp_nullptr_convtype *);
  bool operator!=(__qacpp_nullptr_t::__qacpp_nullptr_convtype *, std::__exception_ptr::exception_ptr const & );
}

#endif


#endif
