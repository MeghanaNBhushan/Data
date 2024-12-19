// qconfig.h
//

#ifndef PRLGCC_INCLUDED_QTCORE_QCONFIG
#define PRLGCC_INCLUDED_QTCORE_QCONFIG

#include_next<QtCore/qconfig.h>

#if defined (PRL_GCC_07)
// statement expressions not supported by QA C++ 
#  define Q_CC_INTEL 1
#endif

#endif
