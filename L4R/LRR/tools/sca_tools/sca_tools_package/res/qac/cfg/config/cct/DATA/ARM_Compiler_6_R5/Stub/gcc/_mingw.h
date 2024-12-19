// _mingw.h
//

#ifndef PRLGCC_INCLUDED__MINGW
#define PRLGCC_INCLUDED__MINGW

#include_next <_mingw.h>

/*
** MinGW undefines __attribute__ in order to:
**    "avoid problems with outdated checks for GCC __attribute__ support".
*/
#if defined (__attribute__)
#undef __attribute__
#endif
#define __attribute__                             _ignore_paren

#endif
