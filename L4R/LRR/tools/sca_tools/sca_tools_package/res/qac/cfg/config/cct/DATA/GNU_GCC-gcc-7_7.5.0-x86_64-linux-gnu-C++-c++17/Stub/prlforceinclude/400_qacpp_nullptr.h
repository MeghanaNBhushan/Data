// qacpp_nullptr.h
//

#ifndef PRLGCC_INCLUDED_QACPP_NULLPTR
#define PRLGCC_INCLUDED_QACPP_NULLPTR

#if (__QACPP_MAJOR__ < 40)

namespace __qacpp_nullptr
{
  class __qacpp_nullptr_t
  {
  public:
    struct __qacpp_nullptr_convtype;
  
  public:
    __qacpp_nullptr_t();
    __qacpp_nullptr_t(__qacpp_nullptr_convtype *);
    template<class T> inline operator T*() const { return 0; }
    template<class C, class T> inline operator T C ::* () const { return 0; }

  private:
    void operator&() const;
 
  } const nullptr;
  
  template<typename T> bool operator==(__qacpp_nullptr_t, T*);
  template<typename T> bool operator==(T*, __qacpp_nullptr_t);
  template<typename T> bool operator!=(__qacpp_nullptr_t, T*);
  template<typename T> bool operator!=(T*, __qacpp_nullptr_t);
}

using __qacpp_nullptr::nullptr;
using __qacpp_nullptr::operator==;
using __qacpp_nullptr::operator!=;

namespace std
{
  using __qacpp_nullptr::nullptr;
  using __qacpp_nullptr::operator==;
  using __qacpp_nullptr::operator!=;
}

#endif


#endif
