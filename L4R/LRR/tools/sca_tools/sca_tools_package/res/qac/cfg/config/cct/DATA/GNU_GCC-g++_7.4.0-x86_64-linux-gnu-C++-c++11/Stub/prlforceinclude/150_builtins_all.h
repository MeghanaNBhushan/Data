#ifndef _BUILTINS_ALL_H
#define _BUILTINS_ALL_H

#ifndef __attribute__
#define __attribute__                             _ignore_paren
#endif

#if ((__GNUC__ > 4) || ((__GNUC__ == 4) && (__GNUC_MINOR__ > 2)))
typedef char                 __qac_v8qi__ __attribute__ ((vector_size(8)));
#else
typedef signed char          __qac_v8qi__ __attribute__ ((vector_size(8)));
#endif
typedef short                __qac_v4hi__ __attribute__ ((vector_size(8)));
typedef short                __qac_v2hi__ __attribute__ ((vector_size(4)));
typedef int                  __qac_di__   __attribute__ ((vector_size(8)));
typedef int                  __qac_v2si__ __attribute__ ((vector_size(8)));
typedef int                  __qac_v4si__ __attribute__ ((vector_size(16)));
#if ((__GNUC__ > 4) || ((__GNUC__ == 4) && (__GNUC_MINOR__ > 3)))
typedef long long            __qac_v4HI__ __attribute__ ((vector_size(1*sizeof(long long))));
#else
typedef unsigned long long   __qac_v4HI__;
#endif
typedef float                __qac_v4sf__ __attribute__ ((vector_size(sizeof(float)*4)));
#if ((__GNUC__ > 4) || ((__GNUC__ == 4) && (__GNUC_MINOR__ > 3)))
typedef float                __qac_cmpret_v4sf__ __attribute__ ((vector_size(sizeof(float)*4)));
#else
typedef int                  __qac_cmpret_v4sf__ __attribute__ ((vector_size(16)));
#endif

/* Post-MMX types */
typedef int                 __qac_v16si__ __attribute__ ((vector_size(64)));
typedef long long           __qac_v8di__  __attribute__ ((vector_size(64)));
typedef double              __qac_v8df__  __attribute__ ((vector_size(64)));
typedef float               __qac_v16sf__ __attribute__ ((vector_size(64)));
typedef short               __qac_hi__;
typedef char                __qac_qi__;
typedef double              __qac_v2df__ __attribute__ ((vector_size(2*sizeof(double))));
typedef float               __qac_v8sf__ __attribute__ ((vector_size(8*sizeof(float))));
typedef char                __qac_v16qi__ __attribute__ ((vector_size(16)));
typedef double              __qac_v4df__ __attribute__ ((vector_size(4*sizeof(double))));
typedef int                 __qac_round_;
typedef int                 __qac_v8si__ __attribute__ ((vector_size(8*sizeof(int))));
typedef short               __qac_v8hi__ __attribute__ ((vector_size(8*sizeof(short))));
typedef short               __qac_v16hi__ __attribute__ ((vector_size(16*sizeof(short))));
typedef long long           __qac_v2di__ __attribute__ ((vector_size(2*sizeof(long long))));
typedef long long           __qac_v4di__ __attribute__ ((vector_size(4*sizeof(long long))));
typedef float               __qac_v2sf__ __attribute__ ((vector_size(2*sizeof(float))));
typedef int                 __qac_si__;
typedef long long           __qac_v1di__;
typedef char                __qac_v32qi__ __attribute__ ((vector_size(32)));
typedef short               __qac_v32hi__ __attribute__ ((vector_size(32*sizeof(short))));

typedef int *               __qac_ptest_;
typedef int                 __qac_status__;
typedef long double         __qac_float128__;

__qac_float128__ __builtin_fabsq (__qac_float128__);
__qac_float128__ __builtin_copysignq (__qac_float128__, __qac_float128__);

void __builtin_ia32_pause (void);

__qac_float128__ __builtin_infq (void);

__qac_float128__ __builtin_huge_valq (void);

void __builtin_cpu_init (void);

int __builtin_cpu_is (const char *cpuname);

#ifdef __MMX__
/* -mmmx */

// ... available with -mmmx
__qac_di__ __builtin_ia32_pand (__qac_di__, __qac_di__);
__qac_di__ __builtin_ia32_pandn (__qac_di__, __qac_di__);
__qac_di__ __builtin_ia32_por (__qac_di__, __qac_di__);
__qac_di__ __builtin_ia32_pxor (__qac_di__, __qac_di__);
__qac_v2si__ __builtin_ia32_paddd (__qac_v2si__, __qac_v2si__);
__qac_v2si__ __builtin_ia32_pcmpeqd (__qac_v2si__, __qac_v2si__);
__qac_v2si__ __builtin_ia32_pcmpgtd (__qac_v2si__, __qac_v2si__);
__qac_v2si__ __builtin_ia32_psubd (__qac_v2si__, __qac_v2si__);
__qac_v2si__ __builtin_ia32_punpckhdq (__qac_v2si__, __qac_v2si__);
__qac_v2si__ __builtin_ia32_punpckldq (__qac_v2si__, __qac_v2si__);
__qac_v4hi__ __builtin_ia32_packssdw (__qac_v2si__, __qac_v2si__);
__qac_v4hi__ __builtin_ia32_paddsw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_paddusw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_paddw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pcmpeqw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pcmpgtw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pmulhw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pmullw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_psubsw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_psubusw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_psubw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_punpckhwd (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_punpcklwd (__qac_v4hi__, __qac_v4hi__);
__qac_v8qi__ __builtin_ia32_packsswb (__qac_v4hi__, __qac_v4hi__);
__qac_v8qi__ __builtin_ia32_packuswb (__qac_v4hi__, __qac_v4hi__);
__qac_v8qi__ __builtin_ia32_paddb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_paddsb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_paddusb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_pcmpeqb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_pcmpgtb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_psubb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_psubsb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_psubusb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_punpckhbw (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_punpcklbw (__qac_v8qi__, __qac_v8qi__);

__qac_v4hi__ __builtin_ia32_psllw (__qac_v4hi__, __qac_v4hi__);
__qac_v2si__ __builtin_ia32_pslld (__qac_v2si__, __qac_v2si__);
__qac_v1di__ __builtin_ia32_psllq (__qac_v1di__, __qac_v1di__);
__qac_v4hi__ __builtin_ia32_psrlw (__qac_v4hi__, __qac_v4hi__);
__qac_v2si__ __builtin_ia32_psrld (__qac_v2si__, __qac_v2si__);
__qac_v1di__ __builtin_ia32_psrlq (__qac_v1di__, __qac_v1di__);
__qac_v4hi__ __builtin_ia32_psraw (__qac_v4hi__, __qac_v4hi__);
__qac_v2si__ __builtin_ia32_psrad (__qac_v2si__, __qac_v2si__);
__qac_v4hi__ __builtin_ia32_psllwi (__qac_v4hi__, int);
__qac_v2si__ __builtin_ia32_pslldi (__qac_v2si__, int);
__qac_v1di__ __builtin_ia32_psllqi (__qac_v1di__, int);
__qac_v4hi__ __builtin_ia32_psrlwi (__qac_v4hi__, int);
__qac_v2si__ __builtin_ia32_psrldi (__qac_v2si__, int);
__qac_v1di__ __builtin_ia32_psrlqi (__qac_v1di__, int);
__qac_v4hi__ __builtin_ia32_psrawi (__qac_v4hi__, int);
__qac_v2si__ __builtin_ia32_psradi (__qac_v2si__, int);
#endif

#ifdef __SSE__
/* -msse */

__qac_v1di__ __builtin_ia32_psadbw (__qac_v8qi__, __qac_v8qi__);
__qac_v4hi__ __builtin_ia32_pavgw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pinsrw(__qac_v4hi__, int, int);
__qac_v4hi__ __builtin_ia32_pmaxsw(__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pminsw(__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pmulhuw(__qac_v4hi__, __qac_v4hi__);
__qac_v8qi__ __builtin_ia32_pavgb(__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_pmaxub(__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_pminub(__qac_v8qi__, __qac_v8qi__);
int __builtin_ia32_pextrw(__qac_v4hi__, int);
int __builtin_ia32_pmovmskb(__qac_v8qi__);
void __builtin_ia32_maskmovq(__qac_v8qi__, __qac_v8qi__, char *);
void __builtin_ia32_movntq(unsigned long long *, unsigned long long);
void __builtin_ia32_sfence(void);

/* -msse */

__qac_cmpret_v4sf__ __builtin_ia32_cmpeqps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpeqss(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpgeps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpgtps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpleps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpless(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpltps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpltss(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpneqps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpneqss(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpngeps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpngtps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpnleps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpnless(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpnltps(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpnlts(__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpnltss (__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpordps (__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpordss (__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpunordps (__qac_v4sf__, __qac_v4sf__);
__qac_cmpret_v4sf__ __builtin_ia32_cmpunordss (__qac_v4sf__, __qac_v4sf__);
__qac_v2si__ __builtin_ia32_cvtps2pi (__qac_v4sf__);
__qac_v2si__ __builtin_ia32_cvttps2pi (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_addps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_addss (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_andnps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_andps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_cvtpi2ps (__qac_v4sf__, __qac_v2si__);
__qac_v4sf__ __builtin_ia32_cvtsi2ss (__qac_v4sf__, int);
__qac_v4sf__ __builtin_ia32_divps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_divss (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_maxps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_maxss (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_minps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_minss (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_movhlps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_movlhps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_movss (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_mulps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_mulss (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_orps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_rcpps (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_rcpss (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_rsqrtps (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_rsqrtss (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_shufps (__qac_v4sf__, __qac_v4sf__, const int);
__qac_v4sf__ __builtin_ia32_sqrtps (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_sqrtss (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_subps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_subss (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_unpckhps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_unpcklps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_xorps (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_comieq (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_comige (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_comigt (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_comile (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_comilt (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_comineq (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_cvtss2si (__qac_v4sf__);
int __builtin_ia32_cvttss2si (__qac_v4sf__);
int __builtin_ia32_movmskps (__qac_v4sf__);
int __builtin_ia32_ucomieq (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_ucomige (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_ucomigt (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_ucomile (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_ucomilt (__qac_v4sf__, __qac_v4sf__);
int __builtin_ia32_ucomineq (__qac_v4sf__, __qac_v4sf__);
void __builtin_ia32_movntps (float *, __qac_v4sf__);

/* -mmsse */

__qac_v4sf__ __builtin_ia32_loadups (const float *);
void __builtin_ia32_storeups (float *, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_loadss (float *);
__qac_v4sf__ __builtin_ia32_loadhps (__qac_v4sf__, const __qac_v2sf__ *);
__qac_v4sf__ __builtin_ia32_loadlps (__qac_v4sf__, const __qac_v2sf__ *);
void __builtin_ia32_storehps (__qac_v2sf__ *, __qac_v4sf__);
void __builtin_ia32_storelps (__qac_v2sf__ *, __qac_v4sf__);
#endif

#ifdef __SSE2__
/* -msse2 */

int __builtin_ia32_comisdeq (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_comisdlt (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_comisdle (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_comisdgt (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_comisdge (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_comisdneq (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_ucomisdeq (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_ucomisdlt (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_ucomisdle (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_ucomisdgt (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_ucomisdge (__qac_v2df__, __qac_v2df__);
int __builtin_ia32_ucomisdneq (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpeqpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpltpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmplepd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpgtpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpgepd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpunordpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpneqpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpnltpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpnlepd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpngtpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpngepd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpordpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpeqsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpltsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmplesd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpunordsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpneqsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpnltsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpnlesd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cmpordsd (__qac_v2df__, __qac_v2df__);
__qac_v2di__ __builtin_ia32_paddq (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_psubq (__qac_v2di__, __qac_v2di__);
__qac_v2df__ __builtin_ia32_addpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_subpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_mulpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_divpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_addsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_subsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_mulsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_divsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_minpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_maxpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_minsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_maxsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_andpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_andnpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_orpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_xorpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_movsd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_unpckhpd (__qac_v2df__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_unpcklpd (__qac_v2df__, __qac_v2df__);
__qac_v16qi__ __builtin_ia32_paddb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_paddw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_paddd128 (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_paddq128 (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_psubb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_psubw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_psubd128 (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_psubq128 (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_pmullw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_pmulhw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v2di__ __builtin_ia32_pand128 (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_pandn128 (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_por128 (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_pxor128 (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_pavgb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pavgw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_pcmpeqb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pcmpeqw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_pcmpeqd128 (__qac_v4si__, __qac_v4si__);
__qac_v16qi__ __builtin_ia32_pcmpgtb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pcmpgtw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_pcmpgtd128 (__qac_v4si__, __qac_v4si__);
__qac_v16qi__ __builtin_ia32_pmaxub128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pmaxsw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_pminub128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pminsw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_punpckhbw128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_punpckhwd128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_punpckhdq128 (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_punpckhqdq128 (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_punpcklbw128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_punpcklwd128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_punpckldq128 (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_punpcklqdq128 (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_packsswb128 (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_packssdw128 (__qac_v4si__, __qac_v4si__);
__qac_v16qi__ __builtin_ia32_packuswb128 (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_pmulhuw128 (__qac_v8hi__, __qac_v8hi__);
void __builtin_ia32_maskmovdqu (__qac_v16qi__, __qac_v16qi__, char *);
__qac_v2df__ __builtin_ia32_loadupd (const double *);
void __builtin_ia32_storeupd (double *, __qac_v2df__);
__qac_v2df__ __builtin_ia32_loadhpd (__qac_v2df__, double const *);
__qac_v2df__ __builtin_ia32_loadlpd (__qac_v2df__, double const *);
int __builtin_ia32_movmskpd (__qac_v2df__);
int __builtin_ia32_pmovmskb128 (__qac_v16qi__);
void __builtin_ia32_movnti (int *, int);
void __builtin_ia32_movnti64 (long long int *, long long int);
void __builtin_ia32_movntpd (double *, __qac_v2df__);
void __builtin_ia32_movntdq (__qac_v2di__ *, __qac_v2di__);
__qac_v4si__ __builtin_ia32_pshufd (__qac_v4si__, int);
__qac_v8hi__ __builtin_ia32_pshuflw (__qac_v8hi__, int);
__qac_v8hi__ __builtin_ia32_pshufhw (__qac_v8hi__, int);
__qac_v2di__ __builtin_ia32_psadbw128 (__qac_v16qi__, __qac_v16qi__);
__qac_v2df__ __builtin_ia32_sqrtpd (__qac_v2df__);
__qac_v2df__ __builtin_ia32_sqrtsd (__qac_v2df__);
__qac_v2df__ __builtin_ia32_shufpd (__qac_v2df__, __qac_v2df__, int);
__qac_v2df__ __builtin_ia32_cvtdq2pd (__qac_v4si__);
__qac_v4sf__ __builtin_ia32_cvtdq2ps (__qac_v4si__);
__qac_v4si__ __builtin_ia32_cvtpd2dq (__qac_v2df__);
__qac_v2si__ __builtin_ia32_cvtpd2pi (__qac_v2df__);
__qac_v4sf__ __builtin_ia32_cvtpd2ps (__qac_v2df__);
__qac_v4si__ __builtin_ia32_cvttpd2dq (__qac_v2df__);
__qac_v2si__ __builtin_ia32_cvttpd2pi (__qac_v2df__);
__qac_v2df__ __builtin_ia32_cvtpi2pd (__qac_v2si__);
int __builtin_ia32_cvtsd2si (__qac_v2df__);
int __builtin_ia32_cvttsd2si (__qac_v2df__);
long long __builtin_ia32_cvtsd2si64 (__qac_v2df__);
long long __builtin_ia32_cvttsd2si64 (__qac_v2df__);
__qac_v4si__ __builtin_ia32_cvtps2dq (__qac_v4sf__);
__qac_v2df__ __builtin_ia32_cvtps2pd (__qac_v4sf__);
__qac_v4si__ __builtin_ia32_cvttps2dq (__qac_v4sf__);
__qac_v2df__ __builtin_ia32_cvtsi2sd (__qac_v2df__, int);
__qac_v2df__ __builtin_ia32_cvtsi642sd (__qac_v2df__, long long);
__qac_v4sf__ __builtin_ia32_cvtsd2ss (__qac_v4sf__, __qac_v2df__);
__qac_v2df__ __builtin_ia32_cvtss2sd (__qac_v2df__, __qac_v4sf__);
void __builtin_ia32_clflush (const void *);
void __builtin_ia32_lfence (void);
void __builtin_ia32_mfence (void);
__qac_v16qi__ __builtin_ia32_loaddqu (const char *);
void __builtin_ia32_storedqu (char *, __qac_v16qi__);
__qac_v1di__ __builtin_ia32_pmuludq (__qac_v2si__, __qac_v2si__);
__qac_v2di__ __builtin_ia32_pmuludq128 (__qac_v4si__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_psllw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_pslld128 (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_psllq128 (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_psrlw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_psrld128 (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_psrlq128 (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_psraw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_psrad128 (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_pslldqi128 (__qac_v2di__, int);
__qac_v8hi__ __builtin_ia32_psllwi128 (__qac_v8hi__, int);
__qac_v4si__ __builtin_ia32_pslldi128 (__qac_v4si__, int);
__qac_v2di__ __builtin_ia32_psllqi128 (__qac_v2di__, int);
__qac_v2di__ __builtin_ia32_psrldqi128 (__qac_v2di__, int);
__qac_v8hi__ __builtin_ia32_psrlwi128 (__qac_v8hi__, int);
__qac_v4si__ __builtin_ia32_psrldi128 (__qac_v4si__, int);
__qac_v2di__ __builtin_ia32_psrlqi128 (__qac_v2di__, int);
__qac_v8hi__ __builtin_ia32_psrawi128 (__qac_v8hi__, int);
__qac_v4si__ __builtin_ia32_psradi128 (__qac_v4si__, int);
__qac_v4si__ __builtin_ia32_pmaddwd128 (__qac_v8hi__, __qac_v8hi__);
__qac_v2di__ __builtin_ia32_movq128 (__qac_v2di__);

#endif

#ifdef __SSE3__
/* -msse3 */

__qac_v2df__ __builtin_ia32_addsubpd (__qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_addsubps (__qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_haddpd (__qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_haddps (__qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_hsubpd (__qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_hsubps (__qac_v4sf__, __qac_v4sf__);
__qac_v16qi__ __builtin_ia32_lddqu (char const *);
void __builtin_ia32_monitor (void *, unsigned int, unsigned int);
__qac_v4sf__ __builtin_ia32_movshdup (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_movsldup (__qac_v4sf__);
void __builtin_ia32_mwait (unsigned int, unsigned int);

/* -msse3 */

__qac_v2si__ __builtin_ia32_phaddd (__qac_v2si__, __qac_v2si__);
__qac_v4hi__ __builtin_ia32_phaddw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_phaddsw (__qac_v4hi__, __qac_v4hi__);
__qac_v2si__ __builtin_ia32_phsubd (__qac_v2si__, __qac_v2si__);
__qac_v4hi__ __builtin_ia32_phsubw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_phsubsw (__qac_v4hi__, __qac_v4hi__);
__qac_v4hi__ __builtin_ia32_pmaddubsw (__qac_v8qi__, __qac_v8qi__);
__qac_v4hi__ __builtin_ia32_pmulhrsw (__qac_v4hi__, __qac_v4hi__);
__qac_v8qi__ __builtin_ia32_pshufb (__qac_v8qi__, __qac_v8qi__);
__qac_v8qi__ __builtin_ia32_psignb (__qac_v8qi__, __qac_v8qi__);
__qac_v2si__ __builtin_ia32_psignd (__qac_v2si__, __qac_v2si__);
__qac_v4hi__ __builtin_ia32_psignw (__qac_v4hi__, __qac_v4hi__);
__qac_v1di__ __builtin_ia32_palignr (__qac_v1di__, __qac_v1di__, int);
__qac_v8qi__ __builtin_ia32_pabsb (__qac_v8qi__);
__qac_v2si__ __builtin_ia32_pabsd (__qac_v2si__);
__qac_v4hi__ __builtin_ia32_pabsw (__qac_v4hi__);

/* -msse3 */

__qac_v4si__ __builtin_ia32_phaddd128 (__qac_v4si__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_phaddw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_phaddsw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_phsubd128 (__qac_v4si__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_phsubw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_phsubsw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_pmaddubsw128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pmulhrsw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_pshufb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v16qi__ __builtin_ia32_psignb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_psignd128 (__qac_v4si__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_psignw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v2di__ __builtin_ia32_palignr128 (__qac_v2di__, __qac_v2di__, int);
__qac_v16qi__ __builtin_ia32_pabsb128 (__qac_v16qi__);
__qac_v4si__ __builtin_ia32_pabsd128 (__qac_v4si__);
__qac_v8hi__ __builtin_ia32_pabsw128 (__qac_v8hi__);
#endif

#ifdef __SSE4_1__
/* -msse4.1 */

__qac_v2df__ __builtin_ia32_blendpd (__qac_v2df__, __qac_v2df__, const int);
__qac_v4sf__ __builtin_ia32_blendps (__qac_v4sf__, __qac_v4sf__, const int);
__qac_v2df__ __builtin_ia32_blendvpd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_blendvps (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_dppd (__qac_v2df__, __qac_v2df__, const int);
__qac_v4sf__ __builtin_ia32_dpps (__qac_v4sf__, __qac_v4sf__, const int);
__qac_v4sf__ __builtin_ia32_insertps128 (__qac_v4sf__, __qac_v4sf__, const int);
__qac_v2di__ __builtin_ia32_movntdqa (__qac_v2di__ *);
__qac_v16qi__ __builtin_ia32_mpsadbw128 (__qac_v16qi__, __qac_v16qi__, const int);
__qac_v8hi__ __builtin_ia32_packusdw128 (__qac_v4si__, __qac_v4si__);
__qac_v16qi__ __builtin_ia32_pblendvb128 (__qac_v16qi__, __qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pblendw128 (__qac_v8hi__, __qac_v8hi__, const int);
__qac_v2di__ __builtin_ia32_pcmpeqq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_phminposuw128 (__qac_v8hi__);
__qac_v16qi__ __builtin_ia32_pmaxsb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_pmaxsd128 (__qac_v4si__, __qac_v4si__);
__qac_v4si__ __builtin_ia32_pmaxud128 (__qac_v4si__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_pmaxuw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_pminsb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_pminsd128 (__qac_v4si__, __qac_v4si__);
__qac_v4si__ __builtin_ia32_pminud128 (__qac_v4si__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_pminuw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_pmovsxbd128 (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_pmovsxbq128 (__qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pmovsxbw128 (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_pmovsxdq128 (__qac_v4si__);
__qac_v4si__ __builtin_ia32_pmovsxwd128 (__qac_v8hi__);
__qac_v2di__ __builtin_ia32_pmovsxwq128 (__qac_v8hi__);
__qac_v4si__ __builtin_ia32_pmovzxbd128 (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_pmovzxbq128 (__qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pmovzxbw128 (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_pmovzxdq128 (__qac_v4si__);
__qac_v4si__ __builtin_ia32_pmovzxwd128 (__qac_v8hi__);
__qac_v2di__ __builtin_ia32_pmovzxwq128 (__qac_v8hi__);
__qac_v2di__ __builtin_ia32_pmuldq128 (__qac_v4si__, __qac_v4si__);
__qac_v4si__ __builtin_ia32_pmulld128 (__qac_v4si__, __qac_v4si__);
int __builtin_ia32_ptestc128 (__qac_v2di__, __qac_v2di__);
int __builtin_ia32_ptestnzc128 (__qac_v2di__, __qac_v2di__);
int __builtin_ia32_ptestz128 (__qac_v2di__, __qac_v2di__);
__qac_v2df__ __builtin_ia32_roundpd (__qac_v2df__, const int);
__qac_v4sf__ __builtin_ia32_roundps (__qac_v4sf__, const int);
__qac_v2df__ __builtin_ia32_roundsd (__qac_v2df__, __qac_v2df__, const int);
__qac_v4sf__ __builtin_ia32_roundss (__qac_v4sf__, __qac_v4sf__, const int);

/* -msse4.1 */

__qac_v4sf__ __builtin_ia32_vec_set___qac_v4sf__ (__qac_v4sf__, float, const int);
int __builtin_ia32_vec_ext___qac_v16qi__ (__qac_v16qi__, const int);
__qac_v16qi__ __builtin_ia32_vec_set___qac_v16qi__ (__qac_v16qi__, int, const int);
__qac_v4si__ __builtin_ia32_vec_set___qac_v4si__ (__qac_v4si__, int, const int);
__qac_v2di__ __builtin_ia32_vec_set___qac_v2di__ (__qac_v2di__, long long, const int);

/* -msse4.1 */

float __builtin_ia32_vec_ext___qac_v4sf__ (__qac_v4sf__, const int);
int __builtin_ia32_vec_ext___qac_v4si__ (__qac_v4si__, const int);
long long __builtin_ia32_vec_ext___qac_v2di__ (__qac_v2di__, const int);
#endif

#ifdef __SSE4_2__
/* -msse4.2 */

__qac_v16qi__ __builtin_ia32_pcmpestrm128 (__qac_v16qi__, int, __qac_v16qi__, int, const int);
int __builtin_ia32_pcmpestri128 (__qac_v16qi__, int, __qac_v16qi__, int, const int);
int __builtin_ia32_pcmpestria128 (__qac_v16qi__, int, __qac_v16qi__, int, const int);
int __builtin_ia32_pcmpestric128 (__qac_v16qi__, int, __qac_v16qi__, int, const int);
int __builtin_ia32_pcmpestrio128 (__qac_v16qi__, int, __qac_v16qi__, int, const int);
int __builtin_ia32_pcmpestris128 (__qac_v16qi__, int, __qac_v16qi__, int, const int);
int __builtin_ia32_pcmpestriz128 (__qac_v16qi__, int, __qac_v16qi__, int, const int);
__qac_v16qi__ __builtin_ia32_pcmpistrm128 (__qac_v16qi__, __qac_v16qi__, const int);
int __builtin_ia32_pcmpistri128 (__qac_v16qi__, __qac_v16qi__, const int);
int __builtin_ia32_pcmpistria128 (__qac_v16qi__, __qac_v16qi__, const int);
int __builtin_ia32_pcmpistric128 (__qac_v16qi__, __qac_v16qi__, const int);
int __builtin_ia32_pcmpistrio128 (__qac_v16qi__, __qac_v16qi__, const int);
int __builtin_ia32_pcmpistris128 (__qac_v16qi__, __qac_v16qi__, const int);
int __builtin_ia32_pcmpistriz128 (__qac_v16qi__, __qac_v16qi__, const int);
__qac_v2di__ __builtin_ia32_pcmpgtq (__qac_v2di__, __qac_v2di__);

/* -msse4.2 */

unsigned int __builtin_ia32_crc32qi (unsigned int, unsigned char);
unsigned int __builtin_ia32_crc32hi (unsigned int, unsigned short);
unsigned int __builtin_ia32_crc32si (unsigned int, unsigned int);
unsigned long long __builtin_ia32_crc32di (unsigned long long, unsigned long long);

/* -msse4.2 */

int __builtin_popcount (unsigned int);
int __builtin_popcountl (unsigned long);
int __builtin_popcountll (unsigned long long);
#endif

#ifdef __AVX__
/* -mavx */

__qac_v4df__ __builtin_ia32_addpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_addps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_addsubpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_addsubps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_andnpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_andnps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_andpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_andps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_blendpd256 (__qac_v4df__,__qac_v4df__,int);
__qac_v8sf__ __builtin_ia32_blendps256 (__qac_v8sf__,__qac_v8sf__,int);
__qac_v4df__ __builtin_ia32_blendvpd256 (__qac_v4df__,__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_blendvps256 (__qac_v8sf__,__qac_v8sf__,__qac_v8sf__);
__qac_v2df__ __builtin_ia32_cmppd (__qac_v2df__,__qac_v2df__,int);
__qac_v4df__ __builtin_ia32_cmppd256 (__qac_v4df__,__qac_v4df__,int);
__qac_v4sf__ __builtin_ia32_cmpps (__qac_v4sf__,__qac_v4sf__,int);
__qac_v8sf__ __builtin_ia32_cmpps256 (__qac_v8sf__,__qac_v8sf__,int);
__qac_v2df__ __builtin_ia32_cmpsd (__qac_v2df__,__qac_v2df__,int);
__qac_v4sf__ __builtin_ia32_cmpss (__qac_v4sf__,__qac_v4sf__,int);
__qac_v4df__ __builtin_ia32_cvtdq2pd256 (__qac_v4si__);
__qac_v8sf__ __builtin_ia32_cvtdq2ps256 (__qac_v8si__);
__qac_v4si__ __builtin_ia32_cvtpd2dq256 (__qac_v4df__);
__qac_v4sf__ __builtin_ia32_cvtpd2ps256 (__qac_v4df__);
__qac_v8si__ __builtin_ia32_cvtps2dq256 (__qac_v8sf__);
__qac_v4df__ __builtin_ia32_cvtps2pd256 (__qac_v4sf__);
__qac_v4si__ __builtin_ia32_cvttpd2dq256 (__qac_v4df__);
__qac_v8si__ __builtin_ia32_cvttps2dq256 (__qac_v8sf__);
__qac_v4df__ __builtin_ia32_divpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_divps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v8sf__ __builtin_ia32_dpps256 (__qac_v8sf__,__qac_v8sf__,int);
__qac_v4df__ __builtin_ia32_haddpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_haddps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_hsubpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_hsubps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v32qi__ __builtin_ia32_lddqu256 (const char*);
__qac_v32qi__ __builtin_ia32_loaddqu256 (const char*);
__qac_v4df__ __builtin_ia32_loadupd256 (const double*);
__qac_v8sf__ __builtin_ia32_loadups256 (const float*);
__qac_v2df__ __builtin_ia32_maskloadpd (const __qac_v2df__*,__qac_v2df__);
__qac_v4df__ __builtin_ia32_maskloadpd256 (const __qac_v4df__*,__qac_v4df__);
__qac_v4sf__ __builtin_ia32_maskloadps (const __qac_v4sf__*,__qac_v4sf__);
__qac_v8sf__ __builtin_ia32_maskloadps256 (const __qac_v8sf__*,__qac_v8sf__);
void __builtin_ia32_maskstorepd (__qac_v2df__*,__qac_v2df__,__qac_v2df__);
void __builtin_ia32_maskstorepd256 (__qac_v4df__*,__qac_v4df__,__qac_v4df__);
void __builtin_ia32_maskstoreps (__qac_v4sf__*,__qac_v4sf__,__qac_v4sf__);
void __builtin_ia32_maskstoreps256 (__qac_v8sf__*,__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_maxpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_maxps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_minpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_minps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_movddup256 (__qac_v4df__);
int __builtin_ia32_movmskpd256 (__qac_v4df__);
int __builtin_ia32_movmskps256 (__qac_v8sf__);
__qac_v8sf__ __builtin_ia32_movshdup256 (__qac_v8sf__);
__qac_v8sf__ __builtin_ia32_movsldup256 (__qac_v8sf__);
__qac_v4df__ __builtin_ia32_mulpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_mulps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_orpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_orps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v2df__ __builtin_ia32_pd_pd256 (__qac_v4df__);
__qac_v4df__ __builtin_ia32_pd256_pd (__qac_v2df__);
__qac_v4sf__ __builtin_ia32_ps_ps256 (__qac_v8sf__);
__qac_v8sf__ __builtin_ia32_ps256_ps (__qac_v4sf__);
int __builtin_ia32_ptestc256 (__qac_v4di__,__qac_v4di__,__qac_ptest_);
int __builtin_ia32_ptestnzc256 (__qac_v4di__,__qac_v4di__,__qac_ptest_);
int __builtin_ia32_ptestz256 (__qac_v4di__,__qac_v4di__,__qac_ptest_);
__qac_v8sf__ __builtin_ia32_rcpps256 (__qac_v8sf__);
__qac_v4df__ __builtin_ia32_roundpd256 (__qac_v4df__,int);
__qac_v8sf__ __builtin_ia32_roundps256 (__qac_v8sf__,int);
__qac_v8sf__ __builtin_ia32_rsqrtps_nr256 (__qac_v8sf__);
__qac_v8sf__ __builtin_ia32_rsqrtps256 (__qac_v8sf__);
__qac_v4df__ __builtin_ia32_shufpd256 (__qac_v4df__,__qac_v4df__,int);
__qac_v8sf__ __builtin_ia32_shufps256 (__qac_v8sf__,__qac_v8sf__,int);
__qac_v4si__ __builtin_ia32_si_si256 (__qac_v8si__);
__qac_v8si__ __builtin_ia32_si256_si (__qac_v4si__);
__qac_v4df__ __builtin_ia32_sqrtpd256 (__qac_v4df__);
__qac_v8sf__ __builtin_ia32_sqrtps_nr256 (__qac_v8sf__);
__qac_v8sf__ __builtin_ia32_sqrtps256 (__qac_v8sf__);
void __builtin_ia32_storedqu256 (char*,__qac_v32qi__);
void __builtin_ia32_storeupd256 (double*,__qac_v4df__);
void __builtin_ia32_storeups256 (float*,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_subpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_subps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_unpckhpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_unpckhps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_unpcklpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_unpcklps256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4df__ __builtin_ia32_vbroadcastf128_pd256 (const __qac_v2df__*);
__qac_v8sf__ __builtin_ia32_vbroadcastf128_ps256 (const __qac_v4sf__*);
__qac_v4df__ __builtin_ia32_vbroadcastsd256 (const double*);
__qac_v4sf__ __builtin_ia32_vbroadcastss (const float*);
__qac_v8sf__ __builtin_ia32_vbroadcastss256 (const float*);
__qac_v2df__ __builtin_ia32_vextractf128_pd256 (__qac_v4df__,int);
__qac_v4sf__ __builtin_ia32_vextractf128_ps256 (__qac_v8sf__,int);
__qac_v4si__ __builtin_ia32_vextractf128_si256 (__qac_v8si__,int);
__qac_v4df__ __builtin_ia32_vinsertf128_pd256 (__qac_v4df__,__qac_v2df__,int);
__qac_v8sf__ __builtin_ia32_vinsertf128_ps256 (__qac_v8sf__,__qac_v4sf__,int);
__qac_v8si__ __builtin_ia32_vinsertf128_si256 (__qac_v8si__,__qac_v4si__,int);
__qac_v4df__ __builtin_ia32_vperm2f128_pd256 (__qac_v4df__,__qac_v4df__,int);
__qac_v8sf__ __builtin_ia32_vperm2f128_ps256 (__qac_v8sf__,__qac_v8sf__,int);
__qac_v8si__ __builtin_ia32_vperm2f128_si256 (__qac_v8si__,__qac_v8si__,int);
__qac_v2df__ __builtin_ia32_vpermil2pd (__qac_v2df__,__qac_v2df__,__qac_v2di__,int);
__qac_v4df__ __builtin_ia32_vpermil2pd256 (__qac_v4df__,__qac_v4df__,__qac_v4di__,int);
__qac_v4sf__ __builtin_ia32_vpermil2ps (__qac_v4sf__,__qac_v4sf__,__qac_v4si__,int);
__qac_v8sf__ __builtin_ia32_vpermil2ps256 (__qac_v8sf__,__qac_v8sf__,__qac_v8si__,int);
__qac_v2df__ __builtin_ia32_vpermilpd (__qac_v2df__,int);
__qac_v4df__ __builtin_ia32_vpermilpd256 (__qac_v4df__,int);
__qac_v4sf__ __builtin_ia32_vpermilps (__qac_v4sf__,int);
__qac_v8sf__ __builtin_ia32_vpermilps256 (__qac_v8sf__,int);
__qac_v2df__ __builtin_ia32_vpermilvarpd (__qac_v2df__,__qac_v2di__);
__qac_v4df__ __builtin_ia32_vpermilvarpd256 (__qac_v4df__,__qac_v4di__);
__qac_v4sf__ __builtin_ia32_vpermilvarps (__qac_v4sf__,__qac_v4si__);
__qac_v8sf__ __builtin_ia32_vpermilvarps256 (__qac_v8sf__,__qac_v8si__);
int __builtin_ia32_vtestcpd (__qac_v2df__,__qac_v2df__,__qac_ptest_);
int __builtin_ia32_vtestcpd256 (__qac_v4df__,__qac_v4df__,__qac_ptest_);
int __builtin_ia32_vtestcps (__qac_v4sf__,__qac_v4sf__,__qac_ptest_);
int __builtin_ia32_vtestcps256 (__qac_v8sf__,__qac_v8sf__,__qac_ptest_);
int __builtin_ia32_vtestnzcpd (__qac_v2df__,__qac_v2df__,__qac_ptest_);
int __builtin_ia32_vtestnzcpd256 (__qac_v4df__,__qac_v4df__,__qac_ptest_);
int __builtin_ia32_vtestnzcps (__qac_v4sf__,__qac_v4sf__,__qac_ptest_);
int __builtin_ia32_vtestnzcps256 (__qac_v8sf__,__qac_v8sf__,__qac_ptest_);
int __builtin_ia32_vtestzpd (__qac_v2df__,__qac_v2df__,__qac_ptest_);
int __builtin_ia32_vtestzpd256 (__qac_v4df__,__qac_v4df__,__qac_ptest_);
int __builtin_ia32_vtestzps (__qac_v4sf__,__qac_v4sf__,__qac_ptest_);
int __builtin_ia32_vtestzps256 (__qac_v8sf__,__qac_v8sf__,__qac_ptest_);
void __builtin_ia32_vzeroall (void);
void __builtin_ia32_vzeroupper (void);
__qac_v4df__ __builtin_ia32_xorpd256 (__qac_v4df__,__qac_v4df__);
__qac_v8sf__ __builtin_ia32_xorps256 (__qac_v8sf__,__qac_v8sf__);
#endif

#ifdef __AVX2__
/* -mavx2 */

__qac_v32qi__ __builtin_ia32_mpsadbw256 (__qac_v32qi__,__qac_v32qi__,int);
__qac_v32qi__ __builtin_ia32_pabsb256 (__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pabsw256 (__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pabsd256 (__qac_v8si__);
__qac_v16hi__ __builtin_ia32_packssdw256 (__qac_v8si__,__qac_v8si__);
__qac_v32qi__ __builtin_ia32_packsswb256 (__qac_v16hi__,__qac_v16hi__);
__qac_v16hi__ __builtin_ia32_packusdw256 (__qac_v8si__,__qac_v8si__);
__qac_v32qi__ __builtin_ia32_packuswb256 (__qac_v16hi__,__qac_v16hi__);
__qac_v32qi__ __builtin_ia32_paddb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_paddw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_paddd256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_paddq256 (__qac_v4di__,__qac_v4di__);
__qac_v32qi__ __builtin_ia32_paddsb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_paddsw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v32qi__ __builtin_ia32_paddusb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_paddusw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v4di__ __builtin_ia32_palignr256 (__qac_v4di__,__qac_v4di__,int);
__qac_v4di__ __builtin_ia32_andsi256 (__qac_v4di__,__qac_v4di__);
__qac_v4di__ __builtin_ia32_andnotsi256 (__qac_v4di__,__qac_v4di__);
__qac_v32qi__ __builtin_ia32_pavgb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pavgw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v32qi__ __builtin_ia32_pblendvb256 (__qac_v32qi__,__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pblendw256 (__qac_v16hi__,__qac_v16hi__,int);
__qac_v32qi__ __builtin_ia32_pcmpeqb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pcmpeqw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pcmpeqd256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_pcmpeqq256 (__qac_v4di__,__qac_v4di__);
__qac_v32qi__ __builtin_ia32_pcmpgtb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pcmpgtw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pcmpgtd256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_pcmpgtq256 (__qac_v4di__,__qac_v4di__);
__qac_v16hi__ __builtin_ia32_phaddw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_phaddd256 (__qac_v8si__,__qac_v8si__);
__qac_v16hi__ __builtin_ia32_phaddsw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v16hi__ __builtin_ia32_phsubw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_phsubd256 (__qac_v8si__,__qac_v8si__);
__qac_v16hi__ __builtin_ia32_phsubsw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v32qi__ __builtin_ia32_pmaddubsw256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pmaddwd256 (__qac_v16hi__,__qac_v16hi__);
__qac_v32qi__ __builtin_ia32_pmaxsb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pmaxsw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pmaxsd256 (__qac_v8si__,__qac_v8si__);
__qac_v32qi__ __builtin_ia32_pmaxub256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pmaxuw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pmaxud256 (__qac_v8si__,__qac_v8si__);
__qac_v32qi__ __builtin_ia32_pminsb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pminsw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pminsd256 (__qac_v8si__,__qac_v8si__);
__qac_v32qi__ __builtin_ia32_pminub256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pminuw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pminud256 (__qac_v8si__,__qac_v8si__);
int __builtin_ia32_pmovmskb256 (__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_pmovsxbw256 (__qac_v16qi__);
__qac_v8si__ __builtin_ia32_pmovsxbd256 (__qac_v16qi__);
__qac_v4di__ __builtin_ia32_pmovsxbq256 (__qac_v16qi__);
__qac_v8si__ __builtin_ia32_pmovsxwd256 (__qac_v8hi__);
__qac_v4di__ __builtin_ia32_pmovsxwq256 (__qac_v8hi__);
__qac_v4di__ __builtin_ia32_pmovsxdq256 (__qac_v4si__);
__qac_v16hi__ __builtin_ia32_pmovzxbw256 (__qac_v16qi__);
__qac_v8si__ __builtin_ia32_pmovzxbd256 (__qac_v16qi__);
__qac_v4di__ __builtin_ia32_pmovzxbq256 (__qac_v16qi__);
__qac_v8si__ __builtin_ia32_pmovzxwd256 (__qac_v8hi__);
__qac_v4di__ __builtin_ia32_pmovzxwq256 (__qac_v8hi__);
__qac_v4di__ __builtin_ia32_pmovzxdq256 (__qac_v4si__);
__qac_v4di__ __builtin_ia32_pmuldq256 (__qac_v8si__,__qac_v8si__);
__qac_v16hi__ __builtin_ia32_pmulhrsw256 (__qac_v16hi__, __qac_v16hi__);
__qac_v16hi__ __builtin_ia32_pmulhuw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v16hi__ __builtin_ia32_pmulhw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v16hi__ __builtin_ia32_pmullw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_pmulld256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_pmuludq256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_por256 (__qac_v4di__,__qac_v4di__);
__qac_v16hi__ __builtin_ia32_psadbw256 (__qac_v32qi__,__qac_v32qi__);
__qac_v32qi__ __builtin_ia32_pshufb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v8si__ __builtin_ia32_pshufd256 (__qac_v8si__,int);
__qac_v16hi__ __builtin_ia32_pshufhw256 (__qac_v16hi__,int);
__qac_v16hi__ __builtin_ia32_pshuflw256 (__qac_v16hi__,int);
__qac_v32qi__ __builtin_ia32_psignb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_psignw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_psignd256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_pslldqi256 (__qac_v4di__,int);
__qac_v16hi__ __builtin_ia32_psllwi256 (__qac_v16hi__,int);
__qac_v16hi__ __builtin_ia32_psllw256(__qac_v16hi__,__qac_v8hi__);
__qac_v8si__ __builtin_ia32_pslldi256 (__qac_v8si__,int);
__qac_v8si__ __builtin_ia32_pslld256(__qac_v8si__,__qac_v4si__);
__qac_v4di__ __builtin_ia32_psllqi256 (__qac_v4di__,int);
__qac_v4di__ __builtin_ia32_psllq256(__qac_v4di__,__qac_v2di__);
__qac_v16hi__ __builtin_ia32_psrawi256 (__qac_v16hi__,int);
__qac_v16hi__ __builtin_ia32_psraw256 (__qac_v16hi__,__qac_v8hi__);
__qac_v8si__ __builtin_ia32_psradi256 (__qac_v8si__,int);
__qac_v8si__ __builtin_ia32_psrad256 (__qac_v8si__,__qac_v4si__);
__qac_v4di__ __builtin_ia32_psrldqi256 (__qac_v4di__, int);
__qac_v16hi__ __builtin_ia32_psrlwi256 (__qac_v16hi__,int);
__qac_v16hi__ __builtin_ia32_psrlw256 (__qac_v16hi__,__qac_v8hi__);
__qac_v8si__ __builtin_ia32_psrldi256 (__qac_v8si__,int);
__qac_v8si__ __builtin_ia32_psrld256 (__qac_v8si__,__qac_v4si__);
__qac_v4di__ __builtin_ia32_psrlqi256 (__qac_v4di__,int);
__qac_v4di__ __builtin_ia32_psrlq256(__qac_v4di__,__qac_v2di__);
__qac_v32qi__ __builtin_ia32_psubb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v32hi__ __builtin_ia32_psubw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_psubd256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_psubq256 (__qac_v4di__,__qac_v4di__);
__qac_v32qi__ __builtin_ia32_psubsb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_psubsw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v32qi__ __builtin_ia32_psubusb256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_psubusw256 (__qac_v16hi__,__qac_v16hi__);
__qac_v32qi__ __builtin_ia32_punpckhbw256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_punpckhwd256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_punpckhdq256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_punpckhqdq256 (__qac_v4di__,__qac_v4di__);
__qac_v32qi__ __builtin_ia32_punpcklbw256 (__qac_v32qi__,__qac_v32qi__);
__qac_v16hi__ __builtin_ia32_punpcklwd256 (__qac_v16hi__,__qac_v16hi__);
__qac_v8si__ __builtin_ia32_punpckldq256 (__qac_v8si__,__qac_v8si__);
__qac_v4di__ __builtin_ia32_punpcklqdq256 (__qac_v4di__,__qac_v4di__);
__qac_v4di__ __builtin_ia32_pxor256 (__qac_v4di__,__qac_v4di__);
__qac_v4di__ __builtin_ia32_movntdqa256 (__qac_v4di__*);
__qac_v4sf__ __builtin_ia32_vbroadcastss_ps (__qac_v4sf__);
__qac_v8sf__ __builtin_ia32_vbroadcastss_ps256 (__qac_v4sf__);
__qac_v4df__ __builtin_ia32_vbroadcastsd_pd256 (__qac_v2df__);
__qac_v4di__ __builtin_ia32_vbroadcastsi256 (__qac_v2di__);
__qac_v4si__ __builtin_ia32_pblendd128 (__qac_v4si__,__qac_v4si__);
__qac_v8si__ __builtin_ia32_pblendd256 (__qac_v8si__,__qac_v8si__);
__qac_v32qi__ __builtin_ia32_pbroadcastb256 (__qac_v16qi__);
__qac_v16hi__ __builtin_ia32_pbroadcastw256 (__qac_v8hi__);
__qac_v8si__ __builtin_ia32_pbroadcastd256 (__qac_v4si__);
__qac_v4di__ __builtin_ia32_pbroadcastq256 (__qac_v2di__);
__qac_v16qi__ __builtin_ia32_pbroadcastb128 (__qac_v16qi__);
__qac_v8hi__ __builtin_ia32_pbroadcastw128 (__qac_v8hi__);
__qac_v4si__ __builtin_ia32_pbroadcastd128 (__qac_v4si__);
__qac_v2di__ __builtin_ia32_pbroadcastq128 (__qac_v2di__);
__qac_v8si__ __builtin_ia32_permvarsi256 (__qac_v8si__,__qac_v8si__);
__qac_v4df__ __builtin_ia32_permdf256 (__qac_v4df__,int);
__qac_v8sf__ __builtin_ia32_permvarsf256 (__qac_v8sf__,__qac_v8sf__);
__qac_v4di__ __builtin_ia32_permdi256 (__qac_v4di__,int);
__qac_v4di__ __builtin_ia32_permti256 (__qac_v4di__,__qac_v4di__,int);
__qac_v4di__ __builtin_ia32_extract128i256 (__qac_v4di__,int);
__qac_v4di__ __builtin_ia32_insert128i256 (__qac_v4di__,__qac_v2di__,int);
__qac_v8si__ __builtin_ia32_maskloadd256 (const __qac_v8si__*,__qac_v8si__);
__qac_v4di__ __builtin_ia32_maskloadq256 (const __qac_v4di__*,__qac_v4di__);
__qac_v4si__ __builtin_ia32_maskloadd (const __qac_v4si__*,__qac_v4si__);
__qac_v2di__ __builtin_ia32_maskloadq (const __qac_v2di__*,__qac_v2di__);
void __builtin_ia32_maskstored256 (__qac_v8si__*,__qac_v8si__,__qac_v8si__);
void __builtin_ia32_maskstoreq256 (__qac_v4di__*,__qac_v4di__,__qac_v4di__);
void __builtin_ia32_maskstored (__qac_v4si__*,__qac_v4si__,__qac_v4si__);
void __builtin_ia32_maskstoreq (__qac_v2di__*,__qac_v2di__,__qac_v2di__);
__qac_v8si__ __builtin_ia32_psllv8si (__qac_v8si__,__qac_v8si__);
__qac_v4si__ __builtin_ia32_psllv4si (__qac_v4si__,__qac_v4si__);
__qac_v4di__ __builtin_ia32_psllv4di (__qac_v4di__,__qac_v4di__);
__qac_v2di__ __builtin_ia32_psllv2di (__qac_v2di__,__qac_v2di__);
__qac_v8si__ __builtin_ia32_psrav8si (__qac_v8si__,__qac_v8si__);
__qac_v4si__ __builtin_ia32_psrav4si (__qac_v4si__,__qac_v4si__);
__qac_v8si__ __builtin_ia32_psrlv8si (__qac_v8si__,__qac_v8si__);
__qac_v4si__ __builtin_ia32_psrlv4si (__qac_v4si__,__qac_v4si__);
__qac_v4di__ __builtin_ia32_psrlv4di (__qac_v4di__,__qac_v4di__);
__qac_v2di__ __builtin_ia32_psrlv2di (__qac_v2di__,__qac_v2di__);
__qac_v2df__ __builtin_ia32_gathersiv2df (__qac_v2df__, const double*,__qac_v4si__,__qac_v2df__,int);
__qac_v4df__ __builtin_ia32_gathersiv4df (__qac_v4df__, const double*,__qac_v4si__,__qac_v4df__,int);
__qac_v2df__ __builtin_ia32_gatherdiv2df (__qac_v2df__, const double*,__qac_v2di__,__qac_v2df__,int);
__qac_v4df__ __builtin_ia32_gatherdiv4df (__qac_v4df__, const double*,__qac_v4di__,__qac_v4df__,int);
__qac_v4sf__ __builtin_ia32_gathersiv4sf (__qac_v4sf__, const float*,__qac_v4si__,__qac_v4sf__,int);
__qac_v8sf__ __builtin_ia32_gathersiv8sf (__qac_v8sf__, const float*,__qac_v8si__,__qac_v8sf__,int);
__qac_v4sf__ __builtin_ia32_gatherdiv4sf (__qac_v4sf__, const float*,__qac_v2di__,__qac_v4sf__,int);
__qac_v4sf__ __builtin_ia32_gatherdiv4sf256 (__qac_v4sf__, const float*,__qac_v4di__,__qac_v4sf__,int);
__qac_v2di__ __builtin_ia32_gathersiv2di (__qac_v2di__, const long long*,__qac_v4si__,__qac_v2di__,int);
__qac_v4di__ __builtin_ia32_gathersiv4di (__qac_v4di__, const long long*,__qac_v4si__,__qac_v4di__,int);
__qac_v2di__ __builtin_ia32_gatherdiv2di (__qac_v2di__, const long long*,__qac_v2di__,__qac_v2di__,int);
__qac_v4di__ __builtin_ia32_gatherdiv4di (__qac_v4di__, const long long*,__qac_v4di__,__qac_v4di__,int);
__qac_v4si__ __builtin_ia32_gathersiv4si (__qac_v4si__, const int*,__qac_v4si__,__qac_v4si__,int);
__qac_v8si__ __builtin_ia32_gathersiv8si (__qac_v8si__, const int*,__qac_v8si__,__qac_v8si__,int);
__qac_v4si__ __builtin_ia32_gatherdiv4si (__qac_v4si__, const int*,__qac_v2di__,__qac_v4si__,int);
__qac_v4si__ __builtin_ia32_gatherdiv4si256 (__qac_v4si__, const int*,__qac_v4di__,__qac_v4si__,int);
#endif

#ifdef __AES__
/* -maes */

__qac_v2di__ __builtin_ia32_aesenc128 (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_aesenclast128 (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_aesdec128 (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_aesdeclast128 (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_aeskeygenassist128 (__qac_v2di__, const int);
__qac_v2di__ __builtin_ia32_aesimc128 (__qac_v2di__);
#endif

#ifdef __PCLMUL__
/* -mpclmul */

__qac_v2di__ __builtin_ia32_pclmulqdq128 (__qac_v2di__, __qac_v2di__, const int);
#endif

#ifdef __FSGSBASE__
/* -mfsgsbase */

unsigned int __builtin_ia32_rdfsbase32 (void);
unsigned long long __builtin_ia32_rdfsbase64 (void);
unsigned int __builtin_ia32_rdgsbase32 (void);
unsigned long long __builtin_ia32_rdgsbase64 (void);
void _writefsbase_u32 (unsigned int);
void _writefsbase_u64 (unsigned long long);
void _writegsbase_u32 (unsigned int);
void _writegsbase_u64 (unsigned long long);
#endif

#ifdef __RDRND__
/* -mrdrnd */

unsigned int __builtin_ia32_rdrand16_step (unsigned short *);
unsigned int __builtin_ia32_rdrand32_step (unsigned int *);
unsigned int __builtin_ia32_rdrand64_step (unsigned long long *);
#endif


#ifdef __SSE4A__
/* -msse4a */

void __builtin_ia32_movntsd (double *, __qac_v2df__);
void __builtin_ia32_movntss (float *, __qac_v4sf__);
__qac_v2di__ __builtin_ia32_extrq  (__qac_v2di__, __qac_v16qi__);
__qac_v2di__ __builtin_ia32_extrqi (__qac_v2di__, const unsigned int, const unsigned int);
__qac_v2di__ __builtin_ia32_insertq (__qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_insertqi (__qac_v2di__, __qac_v2di__, const unsigned int, const unsigned int);
#endif

#ifdef __XOP__
/* -mxop */

__qac_v2df__ __builtin_ia32_vfrczpd (__qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfrczps (__qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfrczsd (__qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfrczss (__qac_v4sf__);
__qac_v4df__ __builtin_ia32_vfrczpd256 (__qac_v4df__);
__qac_v8sf__ __builtin_ia32_vfrczps256 (__qac_v8sf__);
__qac_v2di__ __builtin_ia32_vpcmov (__qac_v2di__, __qac_v2di__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_vpcmov___qac_v2di__ (__qac_v2di__, __qac_v2di__, __qac_v2di__);
__qac_v4si__ __builtin_ia32_vpcmov___qac_v4si__ (__qac_v4si__, __qac_v4si__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_vpcmov___qac_v8hi__ (__qac_v8hi__, __qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcmov___qac_v16qi__ (__qac_v16qi__, __qac_v16qi__, __qac_v16qi__);
__qac_v2df__ __builtin_ia32_vpcmov___qac_v2df__ (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vpcmov___qac_v4sf__ (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v4di__ __builtin_ia32_vpcmov___qac_v4di__256 (__qac_v4di__, __qac_v4di__, __qac_v4di__);
__qac_v8si__ __builtin_ia32_vpcmov___qac_v8si__256 (__qac_v8si__, __qac_v8si__, __qac_v8si__);
__qac_v16hi__ __builtin_ia32_vpcmov___qac_v16hi__256 (__qac_v16hi__, __qac_v16hi__, __qac_v16hi__);
__qac_v32qi__ __builtin_ia32_vpcmov___qac_v32qi__256 (__qac_v32qi__, __qac_v32qi__, __qac_v32qi__);
__qac_v4df__ __builtin_ia32_vpcmov___qac_v4df__256 (__qac_v4df__, __qac_v4df__, __qac_v4df__);
__qac_v8sf__ __builtin_ia32_vpcmov___qac_v8sf__256 (__qac_v8sf__, __qac_v8sf__, __qac_v8sf__);
__qac_v16qi__ __builtin_ia32_vpcomeqb (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_vpcomeqw (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_vpcomeqd (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomeqq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomequb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomequd (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomequq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomequw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomeqw (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcomfalseb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomfalsed (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomfalseq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomfalseub (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomfalseud (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomfalseuq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomfalseuw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomfalsew (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcomgeb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomged (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomgeq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomgeub (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomgeud (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomgeuq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomgeuw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomgew (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcomgtb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomgtd (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomgtq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomgtub (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomgtud (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomgtuq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomgtuw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomgtw (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcomleb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomled (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomleq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomleub (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomleud (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomleuq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomleuw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomlew (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcomltb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomltd (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomltq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomltub (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomltud (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomltuq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomltuw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomltw (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcomneb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomned (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomneq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomneub (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomneud (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomneuq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomneuw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomnew (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpcomtrueb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomtrued (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomtrueq (__qac_v2di__, __qac_v2di__);
__qac_v16qi__ __builtin_ia32_vpcomtrueub (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpcomtrueud (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpcomtrueuq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpcomtrueuw (__qac_v8hi__, __qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vpcomtruew (__qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_vphaddbd (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_vphaddbq (__qac_v16qi__);
__qac_v8hi__ __builtin_ia32_vphaddbw (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_vphadddq (__qac_v4si__);
__qac_v4si__ __builtin_ia32_vphaddubd (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_vphaddubq (__qac_v16qi__);
__qac_v8hi__ __builtin_ia32_vphaddubw (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_vphaddudq (__qac_v4si__);
__qac_v4si__ __builtin_ia32_vphadduwd (__qac_v8hi__);
__qac_v2di__ __builtin_ia32_vphadduwq (__qac_v8hi__);
__qac_v4si__ __builtin_ia32_vphaddwd (__qac_v8hi__);
__qac_v2di__ __builtin_ia32_vphaddwq (__qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vphsubbw (__qac_v16qi__);
__qac_v2di__ __builtin_ia32_vphsubdq (__qac_v4si__);
__qac_v4si__ __builtin_ia32_vphsubwd (__qac_v8hi__);
__qac_v4si__ __builtin_ia32_vpmacsdd (__qac_v4si__, __qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpmacsdqh (__qac_v4si__, __qac_v4si__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_vpmacsdql (__qac_v4si__, __qac_v4si__, __qac_v2di__);
__qac_v4si__ __builtin_ia32_vpmacssdd (__qac_v4si__, __qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpmacssdqh (__qac_v4si__, __qac_v4si__, __qac_v2di__);
__qac_v2di__ __builtin_ia32_vpmacssdql (__qac_v4si__, __qac_v4si__, __qac_v2di__);
__qac_v4si__ __builtin_ia32_vpmacsswd (__qac_v8hi__, __qac_v8hi__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_vpmacssww (__qac_v8hi__, __qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_vpmacswd (__qac_v8hi__, __qac_v8hi__, __qac_v4si__);
__qac_v8hi__ __builtin_ia32_vpmacsww (__qac_v8hi__, __qac_v8hi__, __qac_v8hi__);
__qac_v4si__ __builtin_ia32_vpmadcsswd (__qac_v8hi__, __qac_v8hi__, __qac_v4si__);
__qac_v4si__ __builtin_ia32_vpmadcswd (__qac_v8hi__, __qac_v8hi__, __qac_v4si__);
__qac_v16qi__ __builtin_ia32_vpperm (__qac_v16qi__, __qac_v16qi__, __qac_v16qi__);
__qac_v16qi__ __builtin_ia32_vprotb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vprotd (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vprotq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vprotw (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpshab (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpshad (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpshaq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpshaw (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_vpshlb (__qac_v16qi__, __qac_v16qi__);
__qac_v4si__ __builtin_ia32_vpshld (__qac_v4si__, __qac_v4si__);
__qac_v2di__ __builtin_ia32_vpshlq (__qac_v2di__, __qac_v2di__);
__qac_v8hi__ __builtin_ia32_vpshlw (__qac_v8hi__, __qac_v8hi__);
#endif

#ifdef __FMA4__
/* -mfma4 */

__qac_v2df__ __builtin_ia32_vfmaddpd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfmaddps (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfmaddsd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfmaddss (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfmsubpd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfmsubps (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfmsubsd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfmsubss (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfnmaddpd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfnmaddps (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfnmaddsd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfnmaddss (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfnmsubpd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfnmsubps (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfnmsubsd (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfnmsubss (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfmaddsubpd  (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfmaddsubps  (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v2df__ __builtin_ia32_vfmsubaddpd  (__qac_v2df__, __qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_vfmsubaddps  (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__);
__qac_v4df__ __builtin_ia32_vfmaddpd256 (__qac_v4df__, __qac_v4df__, __qac_v4df__);
__qac_v8sf__ __builtin_ia32_vfmaddps256 (__qac_v8sf__, __qac_v8sf__, __qac_v8sf__);
__qac_v4df__ __builtin_ia32_vfmsubpd256 (__qac_v4df__, __qac_v4df__, __qac_v4df__);
__qac_v8sf__ __builtin_ia32_vfmsubps256 (__qac_v8sf__, __qac_v8sf__, __qac_v8sf__);
__qac_v4df__ __builtin_ia32_vfnmaddpd256 (__qac_v4df__, __qac_v4df__, __qac_v4df__);
__qac_v8sf__ __builtin_ia32_vfnmaddps256 (__qac_v8sf__, __qac_v8sf__, __qac_v8sf__);
__qac_v4df__ __builtin_ia32_vfnmsubpd256 (__qac_v4df__, __qac_v4df__, __qac_v4df__);
__qac_v8sf__ __builtin_ia32_vfnmsubps256 (__qac_v8sf__, __qac_v8sf__, __qac_v8sf__);
__qac_v4df__ __builtin_ia32_vfmaddsubpd256 (__qac_v4df__, __qac_v4df__, __qac_v4df__);
__qac_v8sf__ __builtin_ia32_vfmaddsubps256 (__qac_v8sf__, __qac_v8sf__, __qac_v8sf__);
__qac_v4df__ __builtin_ia32_vfmsubaddpd256 (__qac_v4df__, __qac_v4df__, __qac_v4df__);
__qac_v8sf__ __builtin_ia32_vfmsubaddps256 (__qac_v8sf__, __qac_v8sf__, __qac_v8sf__);
#endif

#ifdef __LWP__
/* -mlwp */

void __builtin_ia32_llwpcb16 (void *);
void __builtin_ia32_llwpcb32 (void *);
void __builtin_ia32_llwpcb64 (void *);
/*
void * __builtin_ia32_llwpcb16 (void);
void * __builtin_ia32_llwpcb32 (void);
void * __builtin_ia32_llwpcb64 (void);
*/
void __builtin_ia32_lwpval16 (unsigned short, unsigned int, unsigned short);
void __builtin_ia32_lwpval32 (unsigned int, unsigned int, unsigned int);
void __builtin_ia32_lwpval64 (unsigned long long*, unsigned int, unsigned int);
unsigned char __builtin_ia32_lwpins16 (unsigned short, unsigned int, unsigned short);
unsigned char __builtin_ia32_lwpins32 (unsigned int, unsigned int, unsigned int);
unsigned char __builtin_ia32_lwpins64 (unsigned long long*, unsigned int, unsigned int);
#endif

#ifdef __BMI__
/* -mbmi */

unsigned int __builtin_ia32_bextr_u32(unsigned int, unsigned int);
unsigned long long __builtin_ia32_bextr_u64 (unsigned long long, unsigned long long);
#endif

#ifdef __BMI2__
/* -mbmi2 */

unsigned int _bzhi_u32 (unsigned int, unsigned int);
unsigned int _pdep_u32 (unsigned int, unsigned int);
unsigned int _pext_u32 (unsigned int, unsigned int);
unsigned long long _bzhi_u64 (unsigned long long, unsigned long long);
unsigned long long _pdep_u64 (unsigned long long, unsigned long long);
unsigned long long _pext_u64 (unsigned long long, unsigned long long);
#endif

#ifdef __LZCNT__
/* -mlzcnt */

unsigned short __builtin_ia32_lzcnt_16(unsigned short);
unsigned int __builtin_ia32_lzcnt_u32(unsigned int);
unsigned long long __builtin_ia32_lzcnt_u64 (unsigned long long);
#endif

#ifdef __FXSR__
/* -mfxsr */

void __builtin_ia32_fxsave (void *);
void __builtin_ia32_fxrstor (void *);
void __builtin_ia32_fxsave64 (void *);
void __builtin_ia32_fxrstor64 (void *);
#endif

#ifdef __XSAVE__
/* -mxsave */

void __builtin_ia32_xsave (void *, long long);
void __builtin_ia32_xrstor (void *, long long);
void __builtin_ia32_xsave64 (void *, long long);
void __builtin_ia32_xrstor64 (void *, long long);
#endif

#ifdef __XSAVEOPT__
/* -mxsaveopt */

void __builtin_ia32_xsaveopt (void *, long long);
void __builtin_ia32_xsaveopt64 (void *, long long);
#endif

#ifdef __TBM__
/* -mtbm */

unsigned int __builtin_ia32_bextri_u32 (unsigned int, const unsigned int);
unsigned long long __builtin_ia32_bextri_u64 (unsigned long long, const unsigned long long);
#endif

#ifdef __3dNOW__
/* -m3dnow */

void __builtin_ia32_femms (void);
__qac_v8qi__ __builtin_ia32_pavgusb (__qac_v8qi__, __qac_v8qi__);
__qac_v2si__ __builtin_ia32_pf2id (__qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfacc (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfadd (__qac_v2sf__, __qac_v2sf__);
__qac_v2si__ __builtin_ia32_pfcmpeq (__qac_v2sf__, __qac_v2sf__);
__qac_v2si__ __builtin_ia32_pfcmpge (__qac_v2sf__, __qac_v2sf__);
__qac_v2si__ __builtin_ia32_pfcmpgt (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfmax (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfmin (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfmul (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfrcp (__qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfrcpit1 (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfrcpit2 (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfrsqrt (__qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfsub (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfsubr (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pi2fd (__qac_v2si__);
__qac_v4hi__ __builtin_ia32_pmulhrw (__qac_v4hi__, __qac_v4hi__);

/* -m3dnow */

__qac_v2si__ __builtin_ia32_pf2iw (__qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfnacc (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pfpnacc (__qac_v2sf__, __qac_v2sf__);
__qac_v2sf__ __builtin_ia32_pi2fw (__qac_v2si__);
__qac_v2sf__ __builtin_ia32_pswapdsf (__qac_v2sf__);
__qac_v2si__ __builtin_ia32_pswapdsi (__qac_v2si__);
#endif

#ifdef __RTM__
/* -mrtm */

int __builtin_ia32_xbegin ();
void __builtin_ia32_xend ();
void __builtin_ia32_xabort (__qac_status__);
int __builtin_ia32_xtest ();
#endif
#ifdef __AVX__
/* AVX */
void __builtin_ia32_movntdq256 (__qac_v4di__*, __qac_v4di__);
void __builtin_ia32_movntpd256 (double*, __qac_v4df__);
void __builtin_ia32_movntps256 (float*, __qac_v8sf__);
void __builtin_ia32_compressstoresf512_mask (__qac_v16sf__*, __qac_v16sf__, short);
void __builtin_ia32_compressstoresi512_mask (__qac_v16si__*, __qac_v16si__, short);
void __builtin_ia32_compressstoredf512_mask (__qac_v8df__*, __qac_v8df__, signed char);
void __builtin_ia32_compressstoredi512_mask (__qac_v8di__*, __qac_v8di__, signed char);
__qac_v16sf__ __builtin_ia32_expandloadsf512_mask (const __qac_v16sf__*, __qac_v16sf__, short);
__qac_v16sf__ __builtin_ia32_expandloadsf512_maskz (const __qac_v16sf__*, __qac_v16sf__, short);
__qac_v16si__ __builtin_ia32_expandloadsi512_mask (const __qac_v16si__*, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_expandloadsi512_maskz (const __qac_v16si__*, __qac_v16si__, short);
__qac_v8df__ __builtin_ia32_expandloaddf512_mask (const __qac_v8df__*, __qac_v8df__, signed char);
__qac_v8df__ __builtin_ia32_expandloaddf512_maskz (const __qac_v8df__*, __qac_v8df__, signed char);
__qac_v8di__ __builtin_ia32_expandloaddi512_mask (const __qac_v8di__*, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_expandloaddi512_maskz (const __qac_v8di__*, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_loaddqusi512_mask (const __qac_v16si__*, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_loaddqudi512_mask (const __qac_v8di__*, __qac_v8di__, signed char);
__qac_v8df__ __builtin_ia32_loadupd512_mask (const __qac_v8df__*, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_loadups512_mask (const __qac_v16sf__*, __qac_v16sf__, short);
__qac_v16sf__ __builtin_ia32_loadaps512_mask (const __qac_v16sf__*, __qac_v16sf__, short);
__qac_v16si__ __builtin_ia32_movdqa32load512_mask (const __qac_v16si__*, __qac_v16si__, short);
__qac_v8df__ __builtin_ia32_loadapd512_mask (const __qac_v8df__*, __qac_v8df__, signed char);
__qac_v8di__ __builtin_ia32_movdqa64load512_mask (const __qac_v8di__*, __qac_v8di__, signed char);
void __builtin_ia32_movntps512 (float*, __qac_v16sf__);
void __builtin_ia32_movntpd512 (double*, __qac_v8df__);
void __builtin_ia32_movntdq512 (__qac_v8di__*, __qac_v8di__);
__qac_v8di__ __builtin_ia32_movntdqa512 (__qac_v8di__*);
void __builtin_ia32_storedqusi512_mask (__qac_v16si__*, __qac_v16si__, short);
void __builtin_ia32_storedqudi512_mask (__qac_v8di__*, __qac_v8di__, signed char);
void __builtin_ia32_storeupd512_mask (__qac_v8df__*, __qac_v8df__, signed char);
void __builtin_ia32_pmovusqd512mem_mask (__qac_v8si__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovsqd512mem_mask (__qac_v8si__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovqd512mem_mask (__qac_v8si__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovusqw512mem_mask (__qac_v8hi__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovsqw512mem_mask (__qac_v8hi__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovqw512mem_mask (__qac_v8hi__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovusdw512mem_mask (__qac_v16hi__*, __qac_v16si__, short);
void __builtin_ia32_pmovsdw512mem_mask (__qac_v16hi__*, __qac_v16si__, short);
void __builtin_ia32_pmovdw512mem_mask (__qac_v16hi__*, __qac_v16si__, short);
void __builtin_ia32_pmovqb512mem_mask (__qac_v16qi__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovusqb512mem_mask (__qac_v16qi__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovsqb512mem_mask (__qac_v16qi__*, __qac_v8di__, signed char);
void __builtin_ia32_pmovusdb512mem_mask (__qac_v16qi__*, __qac_v16si__, short);
void __builtin_ia32_pmovsdb512mem_mask (__qac_v16qi__*, __qac_v16si__, short);
void __builtin_ia32_pmovdb512mem_mask (__qac_v16qi__*, __qac_v16si__, short);
void __builtin_ia32_storeups512_mask (__qac_v16sf__*, __qac_v16sf__, short);
void __builtin_ia32_storeaps512_mask (__qac_v16sf__*, __qac_v16sf__, short);
void __builtin_ia32_movdqa32store512_mask (__qac_v16si__*, __qac_v16si__, short);
void __builtin_ia32_storeapd512_mask (__qac_v8df__*, __qac_v8df__, signed char);
void __builtin_ia32_movdqa64store512_mask (__qac_v8di__*, __qac_v8di__, signed char);
__qac_v4df__ __builtin_ia32_floorpd256 (__qac_v4df__, __qac_round_);
__qac_v4df__ __builtin_ia32_ceilpd256 (__qac_v4df__, __qac_round_);
__qac_v4df__ __builtin_ia32_truncpd256 (__qac_v4df__, __qac_round_);
__qac_v4df__ __builtin_ia32_rintpd256 (__qac_v4df__, __qac_round_);
__qac_v4df__ __builtin_ia32_roundpd_az256 (__qac_v4df__);
__qac_v8si__ __builtin_ia32_roundpd_az_vec_pack_sfix256 (__qac_v4df__, __qac_v4df__);
__qac_v8si__ __builtin_ia32_floorpd_vec_pack_sfix256 (__qac_v4df__, __qac_v4df__, __qac_round_);
__qac_v8si__ __builtin_ia32_ceilpd_vec_pack_sfix256 (__qac_v4df__, __qac_v4df__, __qac_round_);
__qac_v8sf__ __builtin_ia32_floorps256 (__qac_v8sf__, __qac_round_);
__qac_v8sf__ __builtin_ia32_ceilps256 (__qac_v8sf__, __qac_round_);
__qac_v8sf__ __builtin_ia32_truncps256 (__qac_v8sf__, __qac_round_);
__qac_v8sf__ __builtin_ia32_rintps256 (__qac_v8sf__, __qac_round_);
__qac_v8si__ __builtin_ia32_floorps_sfix256 (__qac_v8sf__, __qac_round_);
__qac_v8si__ __builtin_ia32_ceilps_sfix256 (__qac_v8sf__, __qac_round_);
__qac_v8sf__ __builtin_ia32_roundps_az256 (__qac_v8sf__);
__qac_v8si__ __builtin_ia32_roundps_az_sfix256 (__qac_v8sf__);
__qac_v8sf__ __builtin_ia32_copysignps256 (__qac_v8sf__, __qac_v8sf__);
__qac_v4df__ __builtin_ia32_copysignpd256 (__qac_v4df__, __qac_v4df__);
__qac_v8si__ __builtin_ia32_vec_pack_sfix256 (__qac_v4df__, __qac_v4df__);
__qac_v16si__ __builtin_ia32_alignd512_mask (__qac_v16si__, __qac_v16si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_alignq512_mask (__qac_v8di__, __qac_v8di__, int, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_blendmd_512_mask (__qac_v16si__, __qac_v16si__, short);
__qac_v8df__ __builtin_ia32_blendmpd_512_mask (__qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_blendmps_512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v8di__ __builtin_ia32_blendmq_512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16sf__ __builtin_ia32_broadcastf32x4_512 (__qac_v4sf__, __qac_v16sf__, short);
__qac_v8df__ __builtin_ia32_broadcastf64x4_512 (__qac_v4df__, __qac_v8df__, signed char);
__qac_v16si__ __builtin_ia32_broadcasti32x4_512 (__qac_v4si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_broadcasti64x4_512 (__qac_v4di__, __qac_v8di__, signed char);
__qac_v8df__ __builtin_ia32_broadcastsd512 (__qac_v2df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_broadcastss512 (__qac_v4sf__, __qac_v16sf__, short);
short __builtin_ia32_cmpd512_mask (__qac_v16si__, __qac_v16si__, int, short);
signed char __builtin_ia32_cmpq512_mask (__qac_v8di__, __qac_v8di__, int, signed char);
__qac_v8df__ __builtin_ia32_compressdf512_mask (__qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_compresssf512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v8df__ __builtin_ia32_cvtdq2pd512_mask (__qac_v8si__, __qac_v8df__, signed char);
__qac_v16hi__ __builtin_ia32_vcvtps2ph512_mask (__qac_v16sf__, int, __qac_v16hi__, short);
__qac_v8df__ __builtin_ia32_cvtudq2pd512_mask (__qac_v8si__, __qac_v8df__, signed char);
__qac_v2df__ __builtin_ia32_cvtusi2sd32 (__qac_v2df__, unsigned int);
__qac_v8df__ __builtin_ia32_expanddf512_mask (__qac_v8df__, __qac_v8df__, signed char);
__qac_v8df__ __builtin_ia32_expanddf512_maskz (__qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_expandsf512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v16sf__ __builtin_ia32_expandsf512_maskz (__qac_v16sf__, __qac_v16sf__, short);
__qac_v4sf__ __builtin_ia32_extractf32x4_mask (__qac_v16sf__, int, __qac_v4sf__, signed char);
__qac_v4df__ __builtin_ia32_extractf64x4_mask (__qac_v8df__, int, __qac_v4df__, signed char);
__qac_v4si__ __builtin_ia32_extracti32x4_mask (__qac_v16si__, int, __qac_v4si__, signed char);
__qac_v4di__ __builtin_ia32_extracti64x4_mask (__qac_v8di__, int, __qac_v4di__, signed char);
__qac_v16sf__ __builtin_ia32_insertf32x4_mask (__qac_v16sf__, __qac_v4sf__, int, __qac_v16sf__, short);
__qac_v8df__ __builtin_ia32_insertf64x4_mask (__qac_v8df__, __qac_v4df__, int, __qac_v8df__, signed char);
__qac_v16si__ __builtin_ia32_inserti32x4_mask (__qac_v16si__, __qac_v4si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_inserti64x4_mask (__qac_v8di__, __qac_v4di__, int, __qac_v8di__, signed char);
__qac_v8df__ __builtin_ia32_movapd512_mask (__qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_movaps512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v8df__ __builtin_ia32_movddup512_mask (__qac_v8df__, __qac_v8df__, signed char);
__qac_v16si__ __builtin_ia32_movdqa32_512_mask (__qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_movdqa64_512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16sf__ __builtin_ia32_movshdup512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v16sf__ __builtin_ia32_movsldup512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v16si__ __builtin_ia32_pabsd512_mask (__qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pabsq512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_paddd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_paddq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pandd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_pandnd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pandnq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_pandq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pbroadcastd512 (__qac_v4si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_pbroadcastd512_gpr_mask (int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_broadcastmb512 (signed char);
__qac_v16si__ __builtin_ia32_broadcastmw512 (short);
__qac_v8di__ __builtin_ia32_pbroadcastq512 (__qac_v2di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_pbroadcastq512_gpr_mask (__qac_di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_pbroadcastq512_mem_mask (__qac_di__, __qac_v8di__, signed char);
short __builtin_ia32_pcmpeqd512_mask (__qac_v16si__, __qac_v16si__, short);
signed char __builtin_ia32_pcmpeqq512_mask (__qac_v8di__, __qac_v8di__, signed char);
short __builtin_ia32_pcmpgtd512_mask (__qac_v16si__, __qac_v16si__, short);
signed char __builtin_ia32_pcmpgtq512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_compresssi512_mask (__qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_compressdi512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_expandsi512_mask (__qac_v16si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_expandsi512_maskz (__qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_expanddi512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_expanddi512_maskz (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pmaxsd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pmaxsq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pmaxud512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pmaxuq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pminsd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pminsq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pminud512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pminuq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16qi__ __builtin_ia32_pmovdb512_mask (__qac_v16si__, __qac_v16qi__, short);
__qac_v16hi__ __builtin_ia32_pmovdw512_mask (__qac_v16si__, __qac_v16hi__, short);
__qac_v16qi__ __builtin_ia32_pmovqb512_mask (__qac_v8di__, __qac_v16qi__, signed char);
__qac_v8si__ __builtin_ia32_pmovqd512_mask (__qac_v8di__, __qac_v8si__, signed char);
__qac_v8hi__ __builtin_ia32_pmovqw512_mask (__qac_v8di__, __qac_v8hi__, signed char);
__qac_v16qi__ __builtin_ia32_pmovsdb512_mask (__qac_v16si__, __qac_v16qi__, short);
__qac_v16hi__ __builtin_ia32_pmovsdw512_mask (__qac_v16si__, __qac_v16hi__, short);
__qac_v16qi__ __builtin_ia32_pmovsqb512_mask (__qac_v8di__, __qac_v16qi__, signed char);
__qac_v8si__ __builtin_ia32_pmovsqd512_mask (__qac_v8di__, __qac_v8si__, signed char);
__qac_v8hi__ __builtin_ia32_pmovsqw512_mask (__qac_v8di__, __qac_v8hi__, signed char);
__qac_v16si__ __builtin_ia32_pmovsxbd512_mask (__qac_v16qi__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pmovsxbq512_mask (__qac_v16qi__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_pmovsxdq512_mask (__qac_v8si__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pmovsxwd512_mask (__qac_v16hi__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pmovsxwq512_mask (__qac_v8hi__, __qac_v8di__, signed char);
__qac_v16qi__ __builtin_ia32_pmovusdb512_mask (__qac_v16si__, __qac_v16qi__, short);
__qac_v16hi__ __builtin_ia32_pmovusdw512_mask (__qac_v16si__, __qac_v16hi__, short);
__qac_v16qi__ __builtin_ia32_pmovusqb512_mask (__qac_v8di__, __qac_v16qi__, signed char);
__qac_v8si__ __builtin_ia32_pmovusqd512_mask (__qac_v8di__, __qac_v8si__, signed char);
__qac_v8hi__ __builtin_ia32_pmovusqw512_mask (__qac_v8di__, __qac_v8hi__, signed char);
__qac_v16si__ __builtin_ia32_pmovzxbd512_mask (__qac_v16qi__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pmovzxbq512_mask (__qac_v16qi__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_pmovzxdq512_mask (__qac_v8si__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pmovzxwd512_mask (__qac_v16hi__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pmovzxwq512_mask (__qac_v8hi__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_pmuldq512_mask (__qac_v16si__, __qac_v16si__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pmulld512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pmuludq512_mask (__qac_v16si__, __qac_v16si__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pord512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_porq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_prold512_mask (__qac_v16si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_prolq512_mask (__qac_v8di__, int, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_prolvd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_prolvq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_prord512_mask (__qac_v16si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_prorq512_mask (__qac_v8di__, int, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_prorvd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_prorvq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pshufd512_mask (__qac_v16si__, int, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_pslld512_mask (__qac_v16si__, __qac_v4si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_pslldi512_mask (__qac_v16si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_psllq512_mask (__qac_v8di__, __qac_v2di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_psllqi512_mask (__qac_v8di__, int, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_psllv16si_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_psllv8di_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_psrad512_mask (__qac_v16si__, __qac_v4si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_psradi512_mask (__qac_v16si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_psraq512_mask (__qac_v8di__, __qac_v2di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_psraqi512_mask (__qac_v8di__, int, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_psrav16si_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_psrav8di_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_psrld512_mask (__qac_v16si__, __qac_v4si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_psrldi512_mask (__qac_v16si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_psrlq512_mask (__qac_v8di__, __qac_v2di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_psrlqi512_mask (__qac_v8di__, int, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_psrlv16si_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_psrlv8di_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_psubd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_psubq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
short __builtin_ia32_ptestmd512 (__qac_v16si__, __qac_v16si__, short);
signed char __builtin_ia32_ptestmq512 (__qac_v8di__, __qac_v8di__, signed char);
short __builtin_ia32_ptestnmd512 (__qac_v16si__, __qac_v16si__, short);
signed char __builtin_ia32_ptestnmq512 (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_punpckhdq512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_punpckhqdq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_punpckldq512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_punpcklqdq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_pxord512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_pxorq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v8df__ __builtin_ia32_rcp14pd512_mask (__qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_rcp14ps512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v2df__ __builtin_ia32_rcp14sd (__qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_rcp14ss (__qac_v4sf__, __qac_v4sf__);
__qac_v8df__ __builtin_ia32_rsqrt14pd512_mask (__qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_rsqrt14ps512_mask (__qac_v16sf__, __qac_v16sf__, short);
__qac_v2df__ __builtin_ia32_rsqrt14sd (__qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_rsqrt14ss (__qac_v4sf__, __qac_v4sf__);
__qac_v8df__ __builtin_ia32_shufpd512_mask (__qac_v8df__, __qac_v8df__, int, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_shufps512_mask (__qac_v16sf__, __qac_v16sf__, int, __qac_v16sf__, short);
__qac_v16sf__ __builtin_ia32_shuf_f32x4_mask (__qac_v16sf__, __qac_v16sf__, int, __qac_v16sf__, short);
__qac_v8df__ __builtin_ia32_shuf_f64x2_mask (__qac_v8df__, __qac_v8df__, int, __qac_v8df__, signed char);
__qac_v16si__ __builtin_ia32_shuf_i32x4_mask (__qac_v16si__, __qac_v16si__, int, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_shuf_i64x2_mask (__qac_v8di__, __qac_v8di__, int, __qac_v8di__, signed char);
short __builtin_ia32_ucmpd512_mask (__qac_v16si__, __qac_v16si__, int, short);
signed char __builtin_ia32_ucmpq512_mask (__qac_v8di__, __qac_v8di__, int, signed char);
__qac_v8df__ __builtin_ia32_unpckhpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_unpckhps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short);
__qac_v8df__ __builtin_ia32_unpcklpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_unpcklps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short);
__qac_v16si__ __builtin_ia32_vplzcntd_512_mask (__qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_vplzcntq_512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_vpconflictsi_512_mask (__qac_v16si__, __qac_v16si__, short);
__qac_v8di__ __builtin_ia32_vpconflictdi_512_mask (__qac_v8di__, __qac_v8di__, signed char);
__qac_v8df__ __builtin_ia32_permdf512_mask (__qac_v8df__, int, __qac_v8df__, signed char);
__qac_v8di__ __builtin_ia32_permdi512_mask (__qac_v8di__, int, __qac_v8di__, signed char);
__qac_v16si__ __builtin_ia32_vpermi2vard512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8df__ __builtin_ia32_vpermi2varpd512_mask (__qac_v8df__, __qac_v8di__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_vpermi2varps512_mask (__qac_v16sf__, __qac_v16si__, __qac_v16sf__, short);
__qac_v8di__ __builtin_ia32_vpermi2varq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v8df__ __builtin_ia32_vpermilpd512_mask (__qac_v8df__, int, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_vpermilps512_mask (__qac_v16sf__, int, __qac_v16sf__, short);
__qac_v8df__ __builtin_ia32_vpermilvarpd512_mask (__qac_v8df__, __qac_v8di__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_vpermilvarps512_mask (__qac_v16sf__, __qac_v16si__, __qac_v16sf__, short);
__qac_v16si__ __builtin_ia32_vpermt2vard512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_vpermt2vard512_maskz (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v8df__ __builtin_ia32_vpermt2varpd512_mask (__qac_v8di__, __qac_v8df__, __qac_v8df__, signed char);
__qac_v8df__ __builtin_ia32_vpermt2varpd512_maskz (__qac_v8di__, __qac_v8df__, __qac_v8df__, signed char);
__qac_v16sf__ __builtin_ia32_vpermt2varps512_mask (__qac_v16si__, __qac_v16sf__, __qac_v16sf__, short);
__qac_v16sf__ __builtin_ia32_vpermt2varps512_maskz (__qac_v16si__, __qac_v16sf__, __qac_v16sf__, short);
__qac_v8di__ __builtin_ia32_vpermt2varq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v8di__ __builtin_ia32_vpermt2varq512_maskz (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v8df__ __builtin_ia32_permvardf512_mask (__qac_v8df__, __qac_v8di__, __qac_v8df__, signed char);
__qac_v8di__ __builtin_ia32_permvardi512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, signed char);
__qac_v16sf__ __builtin_ia32_permvarsf512_mask (__qac_v16sf__, __qac_v16si__, __qac_v16sf__, short);
__qac_v16si__ __builtin_ia32_permvarsi512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, short);
__qac_v16si__ __builtin_ia32_pternlogd512_mask (__qac_v16si__, __qac_v16si__, __qac_v16si__, int, short);
__qac_v16si__ __builtin_ia32_pternlogd512_maskz (__qac_v16si__, __qac_v16si__, __qac_v16si__, int, short);
__qac_v8di__ __builtin_ia32_pternlogq512_mask (__qac_v8di__, __qac_v8di__, __qac_v8di__, int, signed char);
__qac_v8di__ __builtin_ia32_pternlogq512_maskz (__qac_v8di__, __qac_v8di__, __qac_v8di__, int, signed char);
__qac_v16sf__ __builtin_ia32_copysignps512 (__qac_v16sf__, __qac_v16sf__);
__qac_v8df__ __builtin_ia32_copysignpd512 (__qac_v8df__, __qac_v8df__);
__qac_v8df__ __builtin_ia32_sqrtpd512 (__qac_v8df__);
__qac_v16sf__ __builtin_ia32_sqrtps512 (__qac_v16sf__);
__qac_v16sf__ __builtin_ia32_exp2ps (__qac_v16sf__);
__qac_v16si__ __builtin_ia32_roundpd_az_vec_pack_sfix512 (__qac_v8df__, __qac_v8df__);
__qac_v16si__ __builtin_ia32_floorpd_vec_pack_sfix512 (__qac_v8df__, __qac_v8df__, __qac_round_);
__qac_v16si__ __builtin_ia32_ceilpd_vec_pack_sfix512 (__qac_v8df__, __qac_v8df__, __qac_round_);
short __builtin_ia32_kandhi (short, short);
short __builtin_ia32_kandnhi (short, short);
short __builtin_ia32_knothi (short);
short __builtin_ia32_korhi (short, short);
short __builtin_ia32_kortestchi (short, short);
short __builtin_ia32_kortestzhi (short, short);
short __builtin_ia32_kunpckhi (short, short);
short __builtin_ia32_kxnorhi (short, short);
short __builtin_ia32_kxorhi (short, short);
short __builtin_ia32_kmov16 (short);
__qac_v8df__ __builtin_ia32_addpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_addps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_addsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_addss_round (__qac_v4sf__, __qac_v4sf__, int);
signed char __builtin_ia32_cmppd512_mask (__qac_v8df__, __qac_v8df__, int, signed char, int);
short __builtin_ia32_cmpps512_mask (__qac_v16sf__, __qac_v16sf__, int, short, int);
signed char __builtin_ia32_cmpsd_mask (__qac_v2df__, __qac_v2df__, int, signed char, int);
signed char __builtin_ia32_cmpss_mask (__qac_v4sf__, __qac_v4sf__, int, signed char, int);
int __builtin_ia32_vcomisd (__qac_v2df__, __qac_v2df__, int, int);
int __builtin_ia32_vcomiss (__qac_v4sf__, __qac_v4sf__, int, int);
__qac_v16sf__ __builtin_ia32_cvtdq2ps512_mask (__qac_v16si__, __qac_v16sf__, short, int);
__qac_v8si__ __builtin_ia32_cvtpd2dq512_mask (__qac_v8df__, __qac_v8si__, signed char, int);
__qac_v8sf__ __builtin_ia32_cvtpd2ps512_mask (__qac_v8df__, __qac_v8sf__, signed char, int);
__qac_v8si__ __builtin_ia32_cvtpd2udq512_mask (__qac_v8df__, __qac_v8si__, signed char, int);
__qac_v16sf__ __builtin_ia32_vcvtph2ps512_mask (__qac_v16hi__, __qac_v16sf__, short, int);
__qac_v16si__ __builtin_ia32_cvtps2dq512_mask (__qac_v16sf__, __qac_v16si__, short, int);
__qac_v8df__ __builtin_ia32_cvtps2pd512_mask (__qac_v8sf__, __qac_v8df__, signed char, int);
__qac_v16si__ __builtin_ia32_cvtps2udq512_mask (__qac_v16sf__, __qac_v16si__, short, int);
__qac_v4sf__ __builtin_ia32_cvtsd2ss_round (__qac_v4sf__, __qac_v2df__, int);
__qac_v2df__ __builtin_ia32_cvtsi2sd64 (__qac_v2df__, long long, int);
__qac_v4sf__ __builtin_ia32_cvtsi2ss32 (__qac_v4sf__, int, int);
__qac_v4sf__ __builtin_ia32_cvtsi2ss64 (__qac_v4sf__, long long, int);
__qac_v2df__ __builtin_ia32_cvtss2sd_round (__qac_v2df__, __qac_v4sf__, int);
__qac_v8si__ __builtin_ia32_cvttpd2dq512_mask (__qac_v8df__, __qac_v8si__, signed char, int);
__qac_v8si__ __builtin_ia32_cvttpd2udq512_mask (__qac_v8df__, __qac_v8si__, signed char, int);
__qac_v16si__ __builtin_ia32_cvttps2dq512_mask (__qac_v16sf__, __qac_v16si__, short, int);
__qac_v16si__ __builtin_ia32_cvttps2udq512_mask (__qac_v16sf__, __qac_v16si__, short, int);
__qac_v16sf__ __builtin_ia32_cvtudq2ps512_mask (__qac_v16si__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_cvtusi2sd64 (__qac_v2df__, unsigned long long, int);
__qac_v4sf__ __builtin_ia32_cvtusi2ss32 (__qac_v4sf__, unsigned int, int);
__qac_v4sf__ __builtin_ia32_cvtusi2ss64 (__qac_v4sf__, unsigned long long, int);
__qac_v8df__ __builtin_ia32_divpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_divps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_divsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_divss_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_fixupimmpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8di__, int, signed char, int);
__qac_v8df__ __builtin_ia32_fixupimmpd512_maskz (__qac_v8df__, __qac_v8df__, __qac_v8di__, int, signed char, int);
__qac_v16sf__ __builtin_ia32_fixupimmps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16si__, int, short, int);
__qac_v16sf__ __builtin_ia32_fixupimmps512_maskz (__qac_v16sf__, __qac_v16sf__, __qac_v16si__, int, short, int);
__qac_v2df__ __builtin_ia32_fixupimmsd_mask (__qac_v2df__, __qac_v2df__, __qac_v2di__, int, signed char, int);
__qac_v2df__ __builtin_ia32_fixupimmsd_maskz (__qac_v2df__, __qac_v2df__, __qac_v2di__, int, signed char, int);
__qac_v4sf__ __builtin_ia32_fixupimmss_mask (__qac_v4sf__, __qac_v4sf__, __qac_v4si__, int, signed char, int);
__qac_v4sf__ __builtin_ia32_fixupimmss_maskz (__qac_v4sf__, __qac_v4sf__, __qac_v4si__, int, signed char, int);
__qac_v8df__ __builtin_ia32_getexppd512_mask (__qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_getexpps512_mask (__qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_getexpsd128_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_getexpss128_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_getmantpd512_mask (__qac_v8df__, int, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_getmantps512_mask (__qac_v16sf__, int, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_getmantsd_round (__qac_v2df__, __qac_v2df__, int, int);
__qac_v4sf__ __builtin_ia32_getmantss_round (__qac_v4sf__, __qac_v4sf__, int, int);
__qac_v8df__ __builtin_ia32_maxpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_maxps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_maxsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_maxss_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_minpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_minps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_minsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_minss_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_mulpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_mulps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_mulsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_mulss_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_rndscalepd_mask (__qac_v8df__, int, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_rndscaleps_mask (__qac_v16sf__, int, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_rndscalesd_round (__qac_v2df__, __qac_v2df__, int, int);
__qac_v4sf__ __builtin_ia32_rndscaless_round (__qac_v4sf__, __qac_v4sf__, int, int);
__qac_v8df__ __builtin_ia32_scalefpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_scalefps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_scalefsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_scalefss_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_sqrtpd512_mask (__qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_sqrtps512_mask (__qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_sqrtsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_sqrtss_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_subpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_subps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_subsd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_subss_round (__qac_v4sf__, __qac_v4sf__, int);
int __builtin_ia32_vcvtsd2si32 (__qac_v2df__, int);
long long __builtin_ia32_vcvtsd2si64 (__qac_v2df__, int);
unsigned int __builtin_ia32_vcvtsd2usi32 (__qac_v2df__, int);
unsigned long long __builtin_ia32_vcvtsd2usi64 (__qac_v2df__, int);
int __builtin_ia32_vcvtss2si32 (__qac_v4sf__, int);
long long __builtin_ia32_vcvtss2si64 (__qac_v4sf__, int);
unsigned int __builtin_ia32_vcvtss2usi32 (__qac_v4sf__, int);
unsigned long long __builtin_ia32_vcvtss2usi64 (__qac_v4sf__, int);
int __builtin_ia32_vcvttsd2si32 (__qac_v2df__, int);
long long __builtin_ia32_vcvttsd2si64 (__qac_v2df__, int);
unsigned int __builtin_ia32_vcvttsd2usi32 (__qac_v2df__, int);
unsigned long long __builtin_ia32_vcvttsd2usi64 (__qac_v2df__, int);
int __builtin_ia32_vcvttss2si32 (__qac_v4sf__, int);
long long __builtin_ia32_vcvttss2si64 (__qac_v4sf__, int);
unsigned int __builtin_ia32_vcvttss2usi32 (__qac_v4sf__, int);
unsigned long long __builtin_ia32_vcvttss2usi64 (__qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_vfmaddpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v8df__ __builtin_ia32_vfmaddpd512_mask3 (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v8df__ __builtin_ia32_vfmaddpd512_maskz (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_vfmaddps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v16sf__ __builtin_ia32_vfmaddps512_mask3 (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v16sf__ __builtin_ia32_vfmaddps512_maskz (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_vfmaddsd3_round (__qac_v2df__, __qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_vfmaddss3_round (__qac_v4sf__, __qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_vfmaddsubpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v8df__ __builtin_ia32_vfmaddsubpd512_mask3 (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v8df__ __builtin_ia32_vfmaddsubpd512_maskz (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_vfmaddsubps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v16sf__ __builtin_ia32_vfmaddsubps512_mask3 (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v16sf__ __builtin_ia32_vfmaddsubps512_maskz (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v8df__ __builtin_ia32_vfmsubaddpd512_mask3 (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_vfmsubaddps512_mask3 (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v8df__ __builtin_ia32_vfmsubpd512_mask3 (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_vfmsubps512_mask3 (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v8df__ __builtin_ia32_vfnmaddpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_vfnmaddps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v8df__ __builtin_ia32_vfnmsubpd512_mask (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v8df__ __builtin_ia32_vfnmsubpd512_mask3 (__qac_v8df__, __qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_vfnmsubps512_mask (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v16sf__ __builtin_ia32_vfnmsubps512_mask3 (__qac_v16sf__, __qac_v16sf__, __qac_v16sf__, short, int);
__qac_v8df__ __builtin_ia32_exp2pd_mask (__qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_exp2ps_mask (__qac_v16sf__, __qac_v16sf__, short, int);
__qac_v8df__ __builtin_ia32_rcp28pd_mask (__qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_rcp28ps_mask (__qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_rcp28sd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_rcp28ss_round (__qac_v4sf__, __qac_v4sf__, int);
__qac_v8df__ __builtin_ia32_rsqrt28pd_mask (__qac_v8df__, __qac_v8df__, signed char, int);
__qac_v16sf__ __builtin_ia32_rsqrt28ps_mask (__qac_v16sf__, __qac_v16sf__, short, int);
__qac_v2df__ __builtin_ia32_rsqrt28sd_round (__qac_v2df__, __qac_v2df__, int);
__qac_v4sf__ __builtin_ia32_rsqrt28ss_round (__qac_v4sf__, __qac_v4sf__, int);
void __builtin__ITM_WM256 (__qac_v8sf__*, __qac_v8sf__);
void __builtin__ITM_WaRM256 (__qac_v8sf__*, __qac_v8sf__);
void __builtin__ITM_WaWM256 (__qac_v8sf__*, __qac_v8sf__);
__qac_v8sf__ __builtin__ITM_RM256 (const __qac_v8sf__*);
__qac_v8sf__ __builtin__ITM_RaRM256 (const __qac_v8sf__*);
__qac_v8sf__ __builtin__ITM_RaWM256 (const __qac_v8sf__*);
__qac_v8sf__ __builtin__ITM_RfWM256 (const __qac_v8sf__*);
void __builtin__ITM_LM256 (const void*);
#endif

#ifdef __MMX__
/* MMX */
void __builtin_ia32_emms (void);
__qac_v2si__ __builtin_ia32_pmaddwd (__qac_v4hi__, __qac_v4hi__);
void __builtin__ITM_WM64 (__qac_v2si__*, __qac_v2si__);
void __builtin__ITM_WaRM64 (__qac_v2si__*, __qac_v2si__);
void __builtin__ITM_WaWM64 (__qac_v2si__*, __qac_v2si__);
__qac_v2si__ __builtin__ITM_RM64 (const __qac_v2si__*);
__qac_v2si__ __builtin__ITM_RaRM64 (const __qac_v2si__*);
__qac_v2si__ __builtin__ITM_RaWM64 (const __qac_v2si__*);
__qac_v2si__ __builtin__ITM_RfWM64 (const __qac_v2si__*);
void __builtin__ITM_LM64 (const void*);
#endif

#ifdef __SSE2__
/* SSE2 */
__qac_v2df__ __builtin_ia32_copysignpd (__qac_v2df__, __qac_v2df__);
__qac_v4si__ __builtin_ia32_vec_pack_sfix (__qac_v2df__, __qac_v2df__);
__qac_v16qi__ __builtin_ia32_paddsb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_paddsw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_psubsb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_psubsw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_paddusb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_paddusw128 (__qac_v8hi__, __qac_v8hi__);
__qac_v16qi__ __builtin_ia32_psubusb128 (__qac_v16qi__, __qac_v16qi__);
__qac_v8hi__ __builtin_ia32_psubusw128 (__qac_v8hi__, __qac_v8hi__);
#endif

#ifdef __LWP__
/* LWP */
void __builtin_ia32_llwpcb (void*);
void* __builtin_ia32_slwpcb (void);
#endif

#ifdef __BMI2__
/* BMI2 */
unsigned int __builtin_ia32_bzhi_int (unsigned int, unsigned int);
unsigned long long __builtin_ia32_bzhi_di (unsigned long long, unsigned long long);
unsigned int __builtin_ia32_pdep_int (unsigned int, unsigned int);
unsigned long long __builtin_ia32_pdep_di (unsigned long long, unsigned long long);
unsigned int __builtin_ia32_pext_int (unsigned int, unsigned int);
unsigned long long __builtin_ia32_pext_di (unsigned long long, unsigned long long);
#endif

#ifdef __RDRND__
/* ROUND */
__qac_v2df__ __builtin_ia32_floorpd (__qac_v2df__, __qac_round_);
__qac_v2df__ __builtin_ia32_ceilpd (__qac_v2df__, __qac_round_);
__qac_v2df__ __builtin_ia32_truncpd (__qac_v2df__, __qac_round_);
__qac_v2df__ __builtin_ia32_rintpd (__qac_v2df__, __qac_round_);
__qac_v4si__ __builtin_ia32_floorpd_vec_pack_sfix (__qac_v2df__, __qac_v2df__, __qac_round_);
__qac_v4si__ __builtin_ia32_ceilpd_vec_pack_sfix (__qac_v2df__, __qac_v2df__, __qac_round_);
__qac_v2df__ __builtin_ia32_roundpd_az (__qac_v2df__);
__qac_v4si__ __builtin_ia32_roundpd_az_vec_pack_sfix (__qac_v2df__, __qac_v2df__);
__qac_v4sf__ __builtin_ia32_floorps (__qac_v4sf__, __qac_round_);
__qac_v4sf__ __builtin_ia32_ceilps (__qac_v4sf__, __qac_round_);
__qac_v4sf__ __builtin_ia32_truncps (__qac_v4sf__, __qac_round_);
__qac_v4sf__ __builtin_ia32_rintps (__qac_v4sf__, __qac_round_);
__qac_v4si__ __builtin_ia32_floorps_sfix (__qac_v4sf__, __qac_round_);
__qac_v4si__ __builtin_ia32_ceilps_sfix (__qac_v4sf__, __qac_round_);
__qac_v4sf__ __builtin_ia32_roundps_az (__qac_v4sf__);
__qac_v4si__ __builtin_ia32_roundps_az_sfix (__qac_v4sf__);
#endif

#ifdef __SSE__
/* SSE */
__qac_v4sf__ __builtin_ia32_sqrtps_nr (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_rsqrtps_nr (__qac_v4sf__);
long long __builtin_ia32_cvtss2si64 (__qac_v4sf__);
long long __builtin_ia32_cvttss2si64 (__qac_v4sf__);
__qac_v4sf__ __builtin_ia32_copysignps (__qac_v4sf__, __qac_v4sf__);
__qac_v4sf__ __builtin_ia32_cvtsi642ss (__qac_v4sf__, __qac_di__);
float __builtin_ia32_rsqrtf (float);
__qac_v4hi__ __builtin_ia32_pshufw (__qac_v4hi__,const int);
void __builtin__ITM_WM128 (__qac_v4sf__*, __qac_v4sf__);
void __builtin__ITM_WaRM128 (__qac_v4sf__*, __qac_v4sf__);
void __builtin__ITM_WaWM128 (__qac_v4sf__*, __qac_v4sf__);
__qac_v4sf__ __builtin__ITM_RM128 (const __qac_v4sf__*);
__qac_v4sf__ __builtin__ITM_RaRM128 (const __qac_v4sf__*);
__qac_v4sf__ __builtin__ITM_RaWM128 (const __qac_v4sf__*);
__qac_v4sf__ __builtin__ITM_RfWM128 (const __qac_v4sf__*);
void __builtin__ITM_LM128 (const void*);
#endif

unsigned long long __builtin_ia32_rdtsc (void);
unsigned long long __builtin_ia32_rdtscp (unsigned*);
int __builtin_ia32_bsrsi (int);
unsigned long long __builtin_ia32_rdpmc (int);
unsigned char __builtin_ia32_rolqi (unsigned char, int);
unsigned short __builtin_ia32_rolhi (unsigned short, int);
unsigned char __builtin_ia32_rorqi (unsigned char, int);
unsigned short __builtin_ia32_rorhi (unsigned short, int);

#ifdef __FSGSBASE__
/* FSGSBASE */
void __builtin_ia32_wrfsbase32 (unsigned);
void __builtin_ia32_wrfsbase64 (unsigned long long);
void __builtin_ia32_wrgsbase32 (unsigned);
void __builtin_ia32_wrgsbase64 (unsigned long long);
#endif

#ifdef __F16C__
/* F16C */
__qac_v4sf__ __builtin_ia32_vcvtph2ps (__qac_v8hi__);
__qac_v8sf__ __builtin_ia32_vcvtph2ps256 (__qac_v8hi__);
__qac_v8hi__ __builtin_ia32_vcvtps2ph (__qac_v4sf__, int);
__qac_v8hi__ __builtin_ia32_vcvtps2ph256 (__qac_v8sf__, int);
#endif

/* 64BIT */
long long __builtin_ia32_bsrdi (long long);

#ifdef __3dNOW__
/* 3DNOW */
__qac_v2sf__ __builtin_ia32_pfrsqit1 (__qac_v2sf__, __qac_v2sf__);
#endif

/* functions from https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html */

#define __builtin_choose_expr(const_exp, exp1, exp2) \
  ((const_exp) ? (exp1) : (exp2))

long __builtin_expect (long, long);
void __builtin_trap (void);
void __builtin_unreachable (void);
int __builtin_LINE ();
const char * __builtin_FUNCTION ();
const char * __builtin_FILE ();
void __builtin___clear_cache (char *, char *);
void __builtin_prefetch (const void *, ...);
double __builtin_huge_val (void);
float __builtin_huge_valf (void);
long double __builtin_huge_vall (void);
int __builtin_fpclassify (const int, const int, const int, const int, const int, ...);
double __builtin_inf (void);
float __builtin_inff (void);
long double __builtin_infl (void);
double __builtin_nan (const char *);
float __builtin_nanf (const char *);
long double __builtin_nanl (const char *);
double __builtin_nans (const char *);
float __builtin_nansf (const char *);
long double __builtin_nansl (const char *);
int __builtin_ffs (int);
int __builtin_popcount (unsigned int);
int __builtin_parity (unsigned int);
int __builtin_ffsl (long);
int __builtin_popcountl (unsigned long);
int __builtin_parityl (unsigned long);
int __builtin_ffsll (long long);
int __builtin_popcountll (unsigned long long);
int __builtin_parityll (unsigned long long);
double __builtin_powi (double, int);
float __builtin_powif (float, int);
long double __builtin_powil (long double, int);


#ifdef __BMI__
/* BMI */
/* unsigned short __builtin_ctzs (unsigned short); */
#define __builtin_ctzs(X) 0
#endif

#ifdef __LZCNT__
/* LZCNT */
/* unsigned short __builtin_clzs (unsigned short); */
#define __builtin_clzs(X) 0
#endif

/* int __builtin_clrsb (int);
 * int __builtin_clrsbl (long);
 * int __builtin_clrsbll (long long);
 */
#define __builtin_clrsb(X) 0
#define __builtin_clrsbl(X) 0
#define __builtin_clrsbll(X) 0

/* int __builtin_clz (unsigned int);
 * int __builtin_clzl (unsigned long);
 * int __builtin_clzll (unsigned long long);
 */
#ifndef __XC32__
#define __builtin_clz(X) 0
#endif
#define __builtin_clzl(X) 0
#define __builtin_clzll(X) 0

/* int __builtin_ctz (unsigned int);
 * int __builtin_ctzl (unsigned long);
 * int __builtin_ctzll (unsigned long long);
 */
#ifndef __XC32__
#define __builtin_ctz(X) 0
#endif
#define __builtin_ctzl(X) 0
#define __builtin_ctzll(X) 0

typedef __qac_float128__ __float80;
typedef __qac_float128__ __float128;

#ifdef __XC32__
/* Microchip xc32-g++ built-in functions */

/* Don't include xkeycheck.h because it doesn't like how we support _Complex */
#define _XKEYCHECK

/* Based on DS50001686J (2.10) DS50002799Aand (2.15) */

/* D.2 BUILT-IN FUNCTION DESCRIPTIONS */
#if __XC32_VERSION > 2100
unsigned int __builtin_bcc0(unsigned int rn, unsigned int sel,
  unsigned int clr);
unsigned int __builtin_bsc0(unsigned int rn, unsigned int sel,
  unsigned int set);
unsigned int __builtin_bcsc0(unsigned int rn, unsigned int sel,
  unsigned int clr, unsigned int set);
unsigned int __builtin_clz(unsigned int x);
unsigned int __builtin_ctz(unsigned int x);
void __builtin_mips_cache(unsigned int op, unsigned int addr);
unsigned int __builtin_mxc0(unsigned int rn, unsigned int sel,
  unsigned int val);
/* Undocumented but used in
xc32\v2.15\examples\cpp_examples\interrupts-1.X\source\interrupts-1.cpp */
unsigned int __builtin_mfc0(unsigned int, unsigned int);
unsigned int __builtin_mtc0(unsigned int rn, unsigned int sel,
  unsigned int val);
#endif
unsigned long __builtin_section_begin(const char *name);
unsigned long __builtin_section_end(const char *name);
unsigned long __builtin_section_size(const char *name);
unsigned int __builtin_get_isr_state(void);
void __builtin_set_isr_state(unsigned int state);
void __builtin_software_breakpoint(void);
/* 14.9 ENABLNG/DISABLING INTERRUPTS */
unsigned int __builtin_disable_interrupts(void);
void __builtin_enable_interrupts(void);

/* D.3 BUILT-IN DSP FUNCTIONS
typedef signed char v4i8 __attribute__ ((vector_size(4)));
typedef signed char v4q7 __attribute__ ((vector_size(4)));
typedef short v2i16 __attribute__ ((vector_size(4)));
typedef short v2q15 __attribute__ ((vector_size(4)));
*/
typedef union { signed char a[4]; } v4i8;
typedef union { signed char a[4]; } v4q7;
typedef union { short a[2]; } v2i16;
typedef union { short a[2]; } v2q15;

typedef int q31;
typedef int i32;
typedef unsigned int ui32;
typedef long long a64;

typedef unsigned char imm0_3;
typedef unsigned char imm0_7;
typedef unsigned char imm0_15;
typedef unsigned char imm0_31;
typedef unsigned char imm0_63;
typedef unsigned char imm0_255;
typedef short imm_n32_31;
typedef short imm_n512_511;

/* TABLE D-1: MAP DIRECTLY TO DSP INSTRUCTION */
v2q15 __builtin_mips_absq_s_ph (v2q15);
q31 __builtin_mips_absq_s_w (q31);
v2q15 __builtin_mips_addq_ph (v2q15, v2q15);
v2q15 __builtin_mips_addq_s_ph (v2q15, v2q15);
q31 __builtin_mips_addq_s_w (q31, q31);
i32 __builtin_mips_addsc (i32, i32);
v4i8 __builtin_mips_addu_qb (v4i8, v4i8);
v4i8 __builtin_mips_addu_s_qb (v4i8, v4i8);
i32 __builtin_mips_addwc (i32, i32);
i32 __builtin_mips_bitrev (i32);
i32 __builtin_mips_bposge32 (void);
void __builtin_mips_cmp_eq_ph (v2q15, v2q15);
void __builtin_mips_cmp_le_ph (v2q15, v2q15);
void __builtin_mips_cmp_lt_ph (v2q15, v2q15);
i32 __builtin_mips_cmpgu_eq_qb (v4i8, v4i8);
i32 __builtin_mips_cmpgu_le_qb (v4i8, v4i8);
i32 __builtin_mips_cmpgu_lt_qb (v4i8, v4i8);
void __builtin_mips_cmpu_eq_qb (v4i8, v4i8);
void __builtin_mips_cmpu_le_qb (v4i8, v4i8);
void __builtin_mips_cmpu_lt_qb (v4i8, v4i8);
a64 __builtin_mips_dpaq_s_w_ph (a64, v2q15, v2q15);
a64 __builtin_mips_dpaq_sa_l_w (a64, q31, q31);
a64 __builtin_mips_dpau_h_qbl (a64, v4i8, v4i8);
a64 __builtin_mips_dpau_h_qbr (a64, v4i8, v4i8);
a64 __builtin_mips_dpsq_s_w_ph (a64, v2q15, v2q15);
a64 __builtin_mips_dpsq_sa_l_w (a64, q31, q31);
a64 __builtin_mips_dpsu_h_qbl (a64, v4i8, v4i8);
a64 __builtin_mips_dpsu_h_qbr (a64, v4i8, v4i8);
i32 __builtin_mips_extp (a64, i32);
i32 __builtin_mips_extp (a64, imm0_31);
i32 __builtin_mips_extpdp (a64, i32);
i32 __builtin_mips_extpdp (a64, imm0_31);
i32 __builtin_mips_extr_r_w (a64, i32);
i32 __builtin_mips_extr_r_w (a64, imm0_31);
i32 __builtin_mips_extr_rs_w (a64, i32);
i32 __builtin_mips_extr_rs_w (a64, imm0_31);
i32 __builtin_mips_extr_s_h (a64, i32);
i32 __builtin_mips_extr_s_h (a64, imm0_31);
i32 __builtin_mips_extr_w (a64, i32);
i32 __builtin_mips_extr_w (a64, imm0_31);
i32 __builtin_mips_insv (i32, i32);
i32 __builtin_mips_lbux (void *, i32);
i32 __builtin_mips_lhx (void *, i32);
i32 __builtin_mips_lwx (void *, i32);
a64 __builtin_mips_maq_s_w_phl (a64, v2q15, v2q15);
a64 __builtin_mips_maq_s_w_phr (a64, v2q15, v2q15);
a64 __builtin_mips_maq_sa_w_phl (a64, v2q15, v2q15);
a64 __builtin_mips_maq_sa_w_phr (a64, v2q15, v2q15);
i32 __builtin_mips_modsub (i32, i32);
a64 __builtin_mips_mthlip (a64, i32);
q31 __builtin_mips_muleq_s_w_phl (v2q15, v2q15);
q31 __builtin_mips_muleq_s_w_phr (v2q15, v2q15);
v2q15 __builtin_mips_muleu_s_ph_qbl (v4i8, v2q15);
v2q15 __builtin_mips_muleu_s_ph_qbr (v4i8, v2q15);
v2q15 __builtin_mips_mulq_rs_ph (v2q15, v2q15);
a64 __builtin_mips_mulsaq_s_w_ph (a64, v2q15, v2q15);
v2q15 __builtin_mips_packrl_ph (v2q15, v2q15);
v2q15 __builtin_mips_pick_ph (v2q15, v2q15);
v4i8 __builtin_mips_pick_qb (v4i8, v4i8);
q31 __builtin_mips_preceq_w_phl (v2q15);
q31 __builtin_mips_preceq_w_phr (v2q15);
v2q15 __builtin_mips_precequ_ph_qbl (v4i8);
v2q15 __builtin_mips_precequ_ph_qbla (v4i8);
v2q15 __builtin_mips_precequ_ph_qbr (v4i8);
v2q15 __builtin_mips_precequ_ph_qbra (v4i8);
v2q15 __builtin_mips_preceu_ph_qbl (v4i8);
v2q15 __builtin_mips_preceu_ph_qbla (v4i8);
v2q15 __builtin_mips_preceu_ph_qbr (v4i8);
v2q15 __builtin_mips_preceu_ph_qbra (v4i8);
v2q15 __builtin_mips_precrq_ph_w (q31, q31);
v4i8 __builtin_mips_precrq_qb_ph (v2q15, v2q15);
v2q15 __builtin_mips_precrq_rs_ph_w (q31, q31);
v4i8 __builtin_mips_precrqu_s_qb_ph (v2q15, v2q15);
i32 __builtin_mips_raddu_w_qb (v4i8);
i32 __builtin_mips_rddsp (imm0_63);
v2q15 __builtin_mips_repl_ph (i32);
v2q15 __builtin_mips_repl_ph (imm_n512_511);
v4i8 __builtin_mips_repl_qb (i32);
v4i8 __builtin_mips_repl_qb (imm0_255);
a64 __builtin_mips_shilo (a64, i32);
a64 __builtin_mips_shilo (a64, imm_n32_31);
v2q15 __builtin_mips_shll_ph (v2q15, i32);
v2q15 __builtin_mips_shll_ph (v2q15, imm0_15);
v4i8 __builtin_mips_shll_qb (v4i8, i32);
v4i8 __builtin_mips_shll_qb (v4i8, imm0_7);
v2q15 __builtin_mips_shll_s_ph (v2q15, i32);
v2q15 __builtin_mips_shll_s_ph (v2q15, imm0_15);
q31 __builtin_mips_shll_s_w (q31, i32);
q31 __builtin_mips_shll_s_w (q31, imm0_31);
v2q15 __builtin_mips_shra_ph (v2q15, i32);
v2q15 __builtin_mips_shra_ph (v2q15, imm0_15);
v2q15 __builtin_mips_shra_r_ph (v2q15, i32);
v2q15 __builtin_mips_shra_r_ph (v2q15, imm0_15);
q31 __builtin_mips_shra_r_w (q31, i32);
q31 __builtin_mips_shra_r_w (q31, imm0_31);
v4i8 __builtin_mips_shrl_qb (v4i8, i32);
v4i8 __builtin_mips_shrl_qb (v4i8, imm0_7);
v2q15 __builtin_mips_subq_ph (v2q15, v2q15);
v2q15 __builtin_mips_subq_s_ph (v2q15, v2q15);
q31 __builtin_mips_subq_s_w (q31, q31);
v4i8 __builtin_mips_subu_qb (v4i8, v4i8);
v4i8 __builtin_mips_subu_s_qb (v4i8, v4i8);
void __builtin_mips_wrdsp (i32, imm0_63);

/* TABLE D-2: MAP DIRECTLY TO MIPS DSP INSTRUCTION */
v4q7 __builtin_mips_absq_s_qb (v4q7);
v2q15 __builtin_mips_addqh_ph (v2q15, v2q15);
v2q15 __builtin_mips_addqh_r_ph (v2q15, v2q15);
q31 __builtin_mips_addqh_r_w (q31, q31);
q31 __builtin_mips_addqh_w (q31, q31);
v2i16 __builtin_mips_addu_ph (v2i16, v2i16);
v2i16 __builtin_mips_addu_s_ph (v2i16, v2i16);
v4i8 __builtin_mips_adduh_qb (v4i8, v4i8);
v4i8 __builtin_mips_adduh_r_qb (v4i8, v4i8);
i32 __builtin_mips_append (i32, i32, imm0_31);
i32 __builtin_mips_balign (i32, i32, imm0_3);
i32 __builtin_mips_cmpgdu_eq_qb (v4i8, v4i8);
i32 __builtin_mips_cmpgdu_le_qb (v4i8, v4i8);
i32 __builtin_mips_cmpgdu_lt_qb (v4i8, v4i8);
a64 __builtin_mips_dpa_w_ph (a64, v2i16, v2i16);
a64 __builtin_mips_dpaqx_s_w_ph (a64, v2q15, v2q15);
a64 __builtin_mips_dpaqx_sa_w_ph (a64, v2q15, v2q15);
a64 __builtin_mips_dpax_w_ph (a64, v2i16, v2i16);
a64 __builtin_mips_dps_w_ph (a64, v2i16, v2i16);
a64 __builtin_mips_dpsqx_s_w_ph (a64, v2q15, v2q15);
a64 __builtin_mips_dpsqx_sa_w_ph (a64, v2q15, v2q15);
a64 __builtin_mips_dpsx_w_ph (a64, v2i16, v2i16);
a64 __builtin_mips_madd (a64, i32, i32);
a64 __builtin_mips_maddu (a64, ui32, ui32);
a64 __builtin_mips_msub (a64, i32, i32);
a64 __builtin_mips_msubu (a64, ui32, ui32);
v2i16 __builtin_mips_mul_ph (v2i16, v2i16);
v2i16 __builtin_mips_mul_s_ph (v2i16, v2i16);
q31 __builtin_mips_mulq_rs_w (q31, q31);
v2q15 __builtin_mips_mulq_s_ph (v2q15, v2q15);
q31 __builtin_mips_mulq_s_w (q31, q31);
a64 __builtin_mips_mulsa_w_ph (a64, v2i16, v2i16);
a64 __builtin_mips_mult (i32, i32);
a64 __builtin_mips_multu (ui32, ui32);
v4i8 __builtin_mips_precr_qb_ph (v2i16, v2i16);
v2i16 __builtin_mips_precr_sra_ph_w (i32, i32, imm0_31);
v2i16 __builtin_mips_precr_sra_r_ph_w (i32, i32, imm0_31);
i32 __builtin_mips_prepend (i32, i32, imm0_31);
v4i8 __builtin_mips_shra_qb (v4i8, i32);
v4i8 __builtin_mips_shra_qb (v4i8, imm0_7);
v4i8 __builtin_mips_shra_r_qb (v4i8, i32);
v4i8 __builtin_mips_shra_r_qb (v4i8, imm0_7);
v2i16 __builtin_mips_shrl_ph (v2i16, i32);
v2i16 __builtin_mips_shrl_ph (v2i16, imm0_15);
v2q15 __builtin_mips_subqh_ph (v2q15, v2q15);
v2q15 __builtin_mips_subqh_r_ph (v2q15, v2q15);
q31 __builtin_mips_subqh_r_w (q31, q31);
q31 __builtin_mips_subqh_w (q31, q31);
v2i16 __builtin_mips_subu_ph (v2i16, v2i16);
v2i16 __builtin_mips_subu_s_ph (v2i16, v2i16);
v4i8 __builtin_mips_subuh_qb (v4i8, v4i8);
v4i8 __builtin_mips_subuh_r_qb (v4i8, v4i8);
#endif /* __XC32 */

#endif

