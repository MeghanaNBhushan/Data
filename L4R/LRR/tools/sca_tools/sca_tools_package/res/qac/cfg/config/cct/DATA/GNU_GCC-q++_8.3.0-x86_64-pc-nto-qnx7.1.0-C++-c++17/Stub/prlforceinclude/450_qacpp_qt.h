// qacpp_qt.h
//

#ifndef PRLGCC_INCLUDED_QACPP_QT
#define PRLGCC_INCLUDED_QACPP_QT

#if defined (PRL_GCC_07)

//
// If the build of QT is being analysed by QA C++, the stub for
// qconfig.h will not be included by qglobal.h (it's contitionally
// included on the value of QT_BUILD_MOC).  Forcing the flag to be set
// when building QT.
#if defined (QT_BUILD_MOC)
#  define Q_CC_INTEL 1
#endif

#endif // PRL_GCC_07


#endif // PRLGCC_INCLUDED_QACPP_QT
