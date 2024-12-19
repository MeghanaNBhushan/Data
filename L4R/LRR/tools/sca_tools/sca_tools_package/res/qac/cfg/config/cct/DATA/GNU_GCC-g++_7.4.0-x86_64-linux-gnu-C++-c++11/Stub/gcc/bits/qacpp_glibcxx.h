// qacpp_glibcxx.h
//
// Official releases of GNU GCC specify the library version using a
// combination of approaches.see the following for more information:
//   https://gcc.gnu.org/onlinedocs/libstdc++/manual/abi.html#abi.versioning
//   
// Where the version has not been found from the library path, this
// file maps the __GLIBCXX__ datestamps to X.Y.Z format for versions
// that are supported by QAC++.
//
// If the datestamp specified by __GLIBCXX__ is wrong or is not listed
// then please contact support at:
//   http://www.programmingresearch.com/services/contact-support
//
// Mapping to a new version is simply a matter of copying an existing
// entry and changing the values as needed:
//
//   #elif  __GLIBCXX__ == <value of __GLIBCXX__ as defined in c++config.h>
//
//   #define __PRL_GLIBCXX__            < major version of library >
//   #define __PRL_GLIBCXX_MINOR__      < minor version of library >
//   #define __PRL_GLIBCXX_PATCHLEVEL__ < patchlevel of library >
//
// See "HANDLING UNSUPPORTED LIBRARIES" below for information on how
// to determine these values.

#ifndef INCLUDED_QACPP_GLIBCXX
#define INCLUDED_QACPP_GLIBCXX

#if defined ( __PRL_GLIBCXX__ )

//
// The final technique for detecting the appropriate library version
// as specified by API Policy and Guidelines is to use the physical
// directory the headers are stored under:
//   include/c++/x.y.z
//
// This is the primary mechanism used to determine the correct
// version.  Should this approach fail, a determination is made based
// on the value of the __GLIBCXX__ setting.
// 

#else


#  if __GLIBCXX__ == 20181206


#    define __PRL_GLIBCXX__            7
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif __GLIBCXX__ == 20180917


#    define __PRL_GLIBCXX__            8
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20180726


#    define __PRL_GLIBCXX__            8
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20180720


#    define __PRL_GLIBCXX__            7
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20180502


#    define __PRL_GLIBCXX__            8
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20180424


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20180415


#    define __PRL_GLIBCXX__            7
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20180414


#    define __PRL_GLIBCXX__            8
#    define __PRL_GLIBCXX_MINOR__      0
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20180125


#    define __PRL_GLIBCXX__            7
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20171010

#    if   defined (_GLIBCXX_NOEXCEPT_IF)
#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0
#    endif

#    if ! defined (_GLIBCXX_NOEXCEPT_IF)
#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      5
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0
#    endif


#  elif  __GLIBCXX__ == 20171003


#    define __PRL_GLIBCXX__            7
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170814


#    define __PRL_GLIBCXX__            7
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170724


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170704


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170618


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170519


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20170516


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170502


#    define __PRL_GLIBCXX__            7
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170406


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20170304


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20161221


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20161005


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20160929


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20160916


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20160822


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20160726


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20160609


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20160603


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20160427


#    define __PRL_GLIBCXX__            6
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20160413

#    if   defined (_GLIBCXX14_CONSTEXPR)
#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1
#    endif

#    if ! defined (_GLIBCXX14_CONSTEXPR)
#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3
#    endif


#  elif  __GLIBCXX__ == 20151204


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20151015


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20151010


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20150716


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20150626


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20150623

#    if   defined (__GNUC_RH_RELEASE__)
#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2
#    endif

#    if ! defined (__GNUC_RH_RELEASE__)
#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 5
#    endif


#  elif  __GLIBCXX__ == 20150426


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20150422


#    define __PRL_GLIBCXX__            5
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20150327


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20141220


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20141219


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20141030


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20140911


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20140716


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20140612


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      7
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20140522


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20140422


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      9
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20140404


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20140222


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      7
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20140120


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20131016


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20130531


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20130412


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      6
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20130411


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      7
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20130322


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      8
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20120920


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      7
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20120702


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      5
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20120614


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      7
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20120322


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      7
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20120313

#    if   defined (__GNUC_RH_RELEASE__)
#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4
#endif

#    if ! defined (__GNUC_RH_RELEASE__)
#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 7
#endif


#  elif  __GLIBCXX__ == 20120305


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20120301


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      6
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20111026


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      6
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20110731


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20110627

#    if ! defined (_GLIBCXX_PACKAGE_URL)
#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 6
#endif

#    if   defined (_GLIBCXX_PACKAGE_URL)
#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      6
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1
#endif


#  elif  __GLIBCXX__ == 20110428


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      5
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20110416


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 6



#  elif  __GLIBCXX__ == 20110325


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      6
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20110214


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20101216


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      5
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20101001


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 5



#  elif  __GLIBCXX__ == 20100731


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      5
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20100726


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20100522


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 5



#  elif  __GLIBCXX__ == 20100429


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20100414


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      5
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20100121


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20091015


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20090804


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20090722


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20090421


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      4
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20090124


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20080827


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20080704


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20080606


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20080519


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 4



#  elif  __GLIBCXX__ == 20080306


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      3
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20080201


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 3



#  elif  __GLIBCXX__ == 20071124


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20071007


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20070719


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20070626


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20070514


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      2
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0



#  elif  __GLIBCXX__ == 20070214


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 2



#  elif  __GLIBCXX__ == 20070105


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20060524


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 1



#  elif  __GLIBCXX__ == 20060228


#    define __PRL_GLIBCXX__            4
#    define __PRL_GLIBCXX_MINOR__      1
#    define __PRL_GLIBCXX_PATCHLEVEL__ 0




#  elif defined (__PRL_GNUC__) && defined (__PRL_GNUC_MINOR__) && defined (__PRL_GNUC_PATCHLEVEL__) && !defined (__PRL_clang__)

//
// Fall back to detected GCC version (if not using clang)
//

#    define __PRL_GLIBCXX__            __PRL_GNUC__
#    define __PRL_GLIBCXX_MINOR__      __PRL_GNUC_MINOR__
#    define __PRL_GLIBCXX_PATCHLEVEL__ __PRL_GNUC_PATCHLEVEL__

#  endif

#endif

#if ! defined ( __PRL_GLIBCXX__ )

#  error "This version of the libstdc++ headers, defined by __GLIBCCXX__, is not supported or has been modified in this distribution.  Please contact support at http://www.programmingresearch.com/services/contact-support."

//
// HANDLING UNSUPPORTED LIBRARIES:
// 
// The above #error is triggered when:
//
//   1: The header set does not follow the 'include/c++/x.y.z' version
//      convention, and
//      
//   2: An existing supported version has a different value for the
//      __GLIBCXX__ macro shipped by the distribution or 3rd party
//      compiler vendor.
//
// Where __GLIBCXX__ has been changed, then the appropriate entry for
// the version shipped with the distribution can be added to the
// table.
//
// To determine the value of __GLIBCXX__, create a file with the
// following content:
//   #include <vector>
//   const unsigned int ValueOfGlibCxxIs = __GLIBCXX__;
//   
// And run the command as follows:
//   <compile command> -E <filename.cpp>
//
// The last few lines of the output will include:
//   const unsigned int ValueOfGlibCxxIs = 
//   # 2 "<stdin>" 3
//                                         20160603
//
// This value is the guard value that can be added to the table above
// to corresponding to the header version.
// 

#elif ( __PRL_GLIBCXX__ > 4 )  && (__QACPP_MAJOR__ < 40)

#  error "This version of the libstdc++ headers(" __GLIBC_CXX__ ") requires QA C++ version 4.0 or later.   Please contact support at http://www.programmingresearch.com/services/contact-support."

#elif ( __PRL_GLIBCXX__ > 5 )  && (__QACPP_MAJOR__ < 42)

#  error "This version of the libstdc++ headers(" __GLIBC_CXX__ ") requires QA C++ version 4.2 or later.   Please contact support at http://www.programmingresearch.com/services/contact-support."

#endif

#endif
