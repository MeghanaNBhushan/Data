// qacpp_builtin.h
//

#ifndef PRLGCC_INCLUDED_QACPP_BUILTIN
#define PRLGCC_INCLUDED_QACPP_BUILTIN

#include "300_qacpp_complex.h"

typedef void *                                    __builtin_va_list;
#define                                           __builtin_va_start(ap, parmN) ((void)((ap)= reinterpret_cast<void*>(&(parmN))))
#define                                           __builtin_va_arg(ap, type)	(*(type*)(ap))
#define                                           __builtin_va_end(ap)		((void)((ap)=0))
#define                                           __builtin_va_copy(d,s)

double                                            __builtin_acos(double);
float                                             __builtin_acosf(float);
double                                            __builtin_acosh(double);
float                                             __builtin_acoshf(float);
long double                                       __builtin_acoshl(long double);
long double                                       __builtin_acosl(long double);
double                                            __builtin_asin(double);
float                                             __builtin_asinf(float);
double                                            __builtin_asinh(double);
float                                             __builtin_asinhf(float);
long double                                       __builtin_asinhl(long double);
long double                                       __builtin_asinl(long double);
double                                            __builtin_atan(double);
double                                            __builtin_atan2(double,double);
float                                             __builtin_atan2f(float,float);
long double                                       __builtin_atan2l(long double, long double);
float                                             __builtin_atanf(float);
double                                            __builtin_atanh(double);
float                                             __builtin_atanhf(float);
long double                                       __builtin_atanhl(long double);
long double                                       __builtin_atanl(long double);
double                                            __builtin_cbrt(double);
float                                             __builtin_cbrtf(float);
long double                                       __builtin_cbrtl(long double);
double                                            __builtin_ceil(double);
float                                             __builtin_ceilf(float);
long double                                       __builtin_ceill(long double);
double                                            __builtin_copysign(double,double);
float                                             __builtin_copysignf(float,float);
long double                                       __builtin_copysignl(long double, long double);
double                                            __builtin_cos(double);
float                                             __builtin_cosf(float);
double                                            __builtin_cosh(double);
float                                             __builtin_coshf(float);
long double                                       __builtin_coshl(long double);
long double                                       __builtin_cosl(long double);
double                                            __builtin_drem(double,double);
float                                             __builtin_dremf(float,float);
long double                                       __builtin_dreml(long double, long double);
double                                            __builtin_erf(double);
double                                            __builtin_erfc(double);
float                                             __builtin_erfcf(float);
long double                                       __builtin_erfcl(long double);
float                                             __builtin_erff(float);
long double                                       __builtin_erfl(long double);
void                                              __builtin__exit(int);
void                                              __builtin__Exit(int);
double                                            __builtin_exp(double);
double                                            __builtin_exp10(double);
float                                             __builtin_exp10f(float);
long double                                       __builtin_exp10l(long double);
double                                            __builtin_exp2(double);
float                                             __builtin_exp2f(float);
long double                                       __builtin_exp2l(long double);
float                                             __builtin_expf(float);
long double                                       __builtin_expl(long double);
double                                            __builtin_expm1(double);
float                                             __builtin_expm1f(float);
long double                                       __builtin_expm1l(long double);
double                                            __builtin_fabs(double);
float                                             __builtin_fabsf(float);
long double                                       __builtin_fabsl(long double);
double                                            __builtin_fdim(double,double);
float                                             __builtin_fdimf(float,float);
long double                                       __builtin_fdiml(long double, long double);
double                                            __builtin_floor(double);
float                                             __builtin_floorf(float);
long double                                       __builtin_floorl(long double);
double                                            __builtin_fma(double,double,double);
float                                             __builtin_fmaf(float,float,float);
long double                                       __builtin_fmal(long double, long double, long double);
double                                            __builtin_fmax(double,double);
float                                             __builtin_fmaxf(float,float);
long double                                       __builtin_fmaxl(long double, long double);
double                                            __builtin_fmin(double,double);
float                                             __builtin_fminf(float,float);
long double                                       __builtin_fminl(long double, long double);
double                                            __builtin_fmod(double,double);
float                                             __builtin_fmodf(float,float);
long double                                       __builtin_fmodl(long double, long double);
double                                            __builtin_frexp(double,int*);
float                                             __builtin_frexpf(float,int*);
long double                                       __builtin_frexpl(long double, int*);
double                                            __builtin_gamma(double);
float                                             __builtin_gammaf(float);
long double                                       __builtin_gammal(long double);
double                                            __builtin_hypot(double,double);
float                                             __builtin_hypotf(float,float);
long double                                       __builtin_hypotl(long double, long double);
int                                               __builtin_ilogb(double);
int                                               __builtin_ilogbf(float);
int                                               __builtin_ilogbl(long double);
int                                               __builtin_isfinite(double);
double                                            __builtin_j0(double);
float                                             __builtin_j0f(float);
long double                                       __builtin_j0l(long double);
double                                            __builtin_j1(double);
float                                             __builtin_j1f(float);
long double                                       __builtin_j1l(long double);
double                                            __builtin_jn(int,double);
float                                             __builtin_jnf(int,float);
long double                                       __builtin_jnl(int, long double);
double                                            __builtin_ldexp(double,int);
float                                             __builtin_ldexpf(float,int);
long double                                       __builtin_ldexpl(long double, int);
double                                            __builtin_lgamma(double);
float                                             __builtin_lgammaf(float);
long double                                       __builtin_lgammal(long double);
long long int                                     __builtin_llrint(double);
long long int                                     __builtin_llrintf(float);
long long int                                     __builtin_llrintl(long double);
long long int                                     __builtin_llround(double);
long long int                                     __builtin_llroundf(float);
long long int                                     __builtin_llroundl(long double);
double                                            __builtin_log(double);
double                                            __builtin_log10(double);
float                                             __builtin_log10f(float);
long double                                       __builtin_log10l(long double);
double                                            __builtin_log1p(double);
float                                             __builtin_log1pf(float);
long double                                       __builtin_log1pl(long double);
double                                            __builtin_log2(double);
float                                             __builtin_log2f(float);
long double                                       __builtin_log2l(long double);
double                                            __builtin_logb(double);
float                                             __builtin_logbf(float);
long double                                       __builtin_logbl(long double);
float                                             __builtin_logf(float);
long double                                       __builtin_logl(long double);
__complex__ double                                __builtin_clog(__complex__ double);
__complex__ float                                 __builtin_clogf(__complex__ float);
__complex__ long double                           __builtin_clogl(__complex__ long double);
long int                                          __builtin_lrint(double);
long int                                          __builtin_lrintf(float);
long int                                          __builtin_lrintl(long double);
long int                                          __builtin_lround(double);
long int                                          __builtin_lroundf(float);
long int                                          __builtin_lroundl(long double);
double                                            __builtin_modf(double,double*);
float                                             __builtin_modff(float,float*);
long double                                       __builtin_modfl(long double, long double*);
double                                            __builtin_nearbyint(double);
float                                             __builtin_nearbyintf(float);
long double                                       __builtin_nearbyintl(long double);
double                                            __builtin_nextafter(double,double);
float                                             __builtin_nextafterf(float,float);
long double                                       __builtin_nextafterl(long double, long double);
double                                            __builtin_nexttoward(double, long double);
float                                             __builtin_nexttowardf(float, long double);
long double                                       __builtin_nexttowardl(long double, long double);
double                                            __builtin_pow(double,double);
double                                            __builtin_pow10(double);
float                                             __builtin_pow10f(float);
long double                                       __builtin_pow10l(long double);
float                                             __builtin_powf(float,float);
long double                                       __builtin_powl(long double, long double);
double                                            __builtin_remainder(double,double);
float                                             __builtin_remainderf(float,float);
long double                                       __builtin_remainderl(long double, long double);
double                                            __builtin_remquo(double,double,int*);
float                                             __builtin_remquof(float,float,int*);
long double                                       __builtin_remquol(long double, long double, int*);
double                                            __builtin_rint(double);
float                                             __builtin_rintf(float);
long double                                       __builtin_rintl(long double);
double                                            __builtin_round(double);
float                                             __builtin_roundf(float);
long double                                       __builtin_roundl(long double);
double                                            __builtin_scalb(double,double);
float                                             __builtin_scalbf(float,float);
long double                                       __builtin_scalbl(long double, long double);
double                                            __builtin_scalbln(double, long int);
float                                             __builtin_scalblnf(float, long int);
long double                                       __builtin_scalblnl(long double, long int);
double                                            __builtin_scalbn(double,int);
float                                             __builtin_scalbnf(float,int);
long double                                       __builtin_scalbnl(long double, int);
int                                               __builtin_signbit (double);
int                                               __builtin_signbitf (float);
int                                               __builtin_signbitl (long double);
double                                            __builtin_significand(double);
float                                             __builtin_significandf(float);
long double                                       __builtin_significandl(long double);
double                                            __builtin_sin(double);
void                                              __builtin_sincos(double,double*,double*);
void                                              __builtin_sincosf(float,float*,float*);
void                                              __builtin_sincosl(long double, long double*, long double*);
float                                             __builtin_sinf(float);
double                                            __builtin_sinh(double);
float                                             __builtin_sinhf(float);
long double                                       __builtin_sinhl(long double);
long double                                       __builtin_sinl(long double);
double                                            __builtin_sqrt(double);
float                                             __builtin_sqrtf(float);
long double                                       __builtin_sqrtl(long double);
double                                            __builtin_tan(double);
float                                             __builtin_tanf(float);
double                                            __builtin_tanh(double);
float                                             __builtin_tanhf(float);
long double                                       __builtin_tanhl(long double);
long double                                       __builtin_tanl(long double);
double                                            __builtin_tgamma(double);
float                                             __builtin_tgammaf(float);
long double                                       __builtin_tgammal(long double);
double                                            __builtin_trunc(double);
float                                             __builtin_truncf(float);
long double                                       __builtin_truncl(long double);
double                                            __builtin_y0(double);
float                                             __builtin_y0f(float);
long double                                       __builtin_y0l(long double);
double                                            __builtin_y1(double);
float                                             __builtin_y1f(float);
long double                                       __builtin_y1l(long double);
double                                            __builtin_yn(int,double);
float                                             __builtin_ynf(int,float);
long double                                       __builtin_ynl(int, long double);
double                                            __builtin_cabs(__complex__ double);
float                                             __builtin_cabsf(__complex__ float);
long double                                       __builtin_cabsl(__complex__ long double);
__complex__ double                                __builtin_cacos(__complex__ double);
__complex__ float                                 __builtin_cacosf(__complex__ float);
__complex__ double                                __builtin_cacosh(__complex__ double);
__complex__ float                                 __builtin_cacoshf(__complex__ float);
__complex__ long double                           __builtin_cacoshl(__complex__ long double);
__complex__ long double                           __builtin_cacosl(__complex__ long double);
double                                            __builtin_carg(__complex__ double);
float                                             __builtin_cargf(__complex__ float);
long double                                       __builtin_cargl(__complex__ long double);
__complex__ double                                __builtin_casin(__complex__ double);
__complex__ float                                 __builtin_casinf(__complex__ float);
__complex__ double                                __builtin_casinh(__complex__ double);
__complex__ float                                 __builtin_casinhf(__complex__ float);
__complex__ long double                           __builtin_casinhl(__complex__ long double);
__complex__ long double                           __builtin_casinl(__complex__ long double);
__complex__ double                                __builtin_catan(__complex__ double);
__complex__ float                                 __builtin_catanf(__complex__ float);
__complex__ double                                __builtin_catanh(__complex__ double);
__complex__ float                                 __builtin_catanhf(__complex__ float);
__complex__ long double                           __builtin_catanhl(__complex__ long double);
__complex__ long double                           __builtin_catanl(__complex__ long double);
__complex__ double                                __builtin_ccos(__complex__ double);
__complex__ float                                 __builtin_ccosf(__complex__ float);
__complex__ double                                __builtin_ccosh(__complex__ double);
__complex__ float                                 __builtin_ccoshf(__complex__ float);
__complex__ long double                           __builtin_ccoshl(__complex__ long double);
__complex__ long double                           __builtin_ccosl(__complex__ long double);
__complex__ double                                __builtin_cexp(__complex__ double);
__complex__ float                                 __builtin_cexpf(__complex__ float);
__complex__ long double                           __builtin_cexpl(__complex__ long double);
double                                            __builtin_cimag(__complex__ double);
float                                             __builtin_cimagf(__complex__ float);
long double                                       __builtin_cimagl(__complex__ long double);
__complex__ double                                __builtin_conj(__complex__ double);
__complex__ float                                 __builtin_conjf(__complex__ float);
__complex__ long double                           __builtin_conjl(__complex__ long double);
__complex__ double                                __builtin_cpow(__complex__ double, __complex__ double);
__complex__ float                                 __builtin_cpowf(__complex__ float, __complex__ float);
__complex__ long double                           __builtin_cpowl(__complex__ long double, __complex__ long double);
__complex__ double                                __builtin_cproj(__complex__ double);
__complex__ float                                 __builtin_cprojf(__complex__ float);
__complex__ long double                           __builtin_cprojl(__complex__ long double);
double                                            __builtin_creal(__complex__ double);
float                                             __builtin_crealf(__complex__ float);
long double                                       __builtin_creall(__complex__ long double);
__complex__ double                                __builtin_csin(__complex__ double);
__complex__ float                                 __builtin_csinf(__complex__ float);
__complex__ double                                __builtin_csinh(__complex__ double);
__complex__ float                                 __builtin_csinhf(__complex__ float);
__complex__ long double                           __builtin_csinhl(__complex__ long double);
__complex__ long double                           __builtin_csinl(__complex__ long double);
__complex__ double                                __builtin_csqrt(__complex__ double);
__complex__ float                                 __builtin_csqrtf(__complex__ float);
__complex__ long double                           __builtin_csqrtl(__complex__ long double);
__complex__ double                                __builtin_ctan(__complex__ double);
__complex__ float                                 __builtin_ctanf(__complex__ float);
__complex__ double                                __builtin_ctanh(__complex__ double);
__complex__ float                                 __builtin_ctanhf(__complex__ float);
__complex__ long double                           __builtin_ctanhl(__complex__ long double);
__complex__ long double                           __builtin_ctanl(__complex__ long double);
int                                               __builtin_bcmp(const void*, const void*, PRQA_SIZE_T);
void                                              __builtin_bcopy(const void*, void*, PRQA_SIZE_T);
void                                              __builtin_bzero(void*, PRQA_SIZE_T);
template <typename INT> INT                       __builtin_bswap16(INT);
template <typename INT> INT                       __builtin_bswap32(INT);
template <typename INT> INT                       __builtin_bswap64(INT);
char*                                             __builtin_index(const char*, int);
template <typename INT> int                       __builtin_isinf(INT);
template <typename INT> int                       __builtin_isnan(INT);
template <typename INT> int                       __builtin_isnormal(INT);
int                                               __builtin_memcmp(const void*,const void*, PRQA_SIZE_T);
void*                                             __builtin_memcpy(void*, const void*, PRQA_SIZE_T);
void*                                             __builtin_memmove(void*, const void*, PRQA_SIZE_T);
void*                                             __builtin_mempcpy(void*, const void*, PRQA_SIZE_T);
void*                                             __builtin_memset(void*, int, PRQA_SIZE_T);
void*                                             __builtin_memchr(const void*,int, PRQA_SIZE_T);
char*                                             __builtin_rindex(const char*,int);
char*                                             __builtin_stpcpy(char*, const char*);
char*                                             __builtin_strcat(char*, const char*);
char*                                             __builtin_strchr(const char*,int);
int                                               __builtin_strcmp(const char*,const char*);
char*                                             __builtin_strcpy(char*, const char*);
PRQA_SIZE_T                                       __builtin_strcspn(const char*,const char*);
char*                                             __builtin_strdup(const char*);
PRQA_SIZE_T                                       __builtin_strlen(const char*);
char*                                             __builtin_strncat(char*, const char*, PRQA_SIZE_T);
int                                               __builtin_strncmp(const char*,const char*, PRQA_SIZE_T);
char*                                             __builtin_strncpy(char*, const char*, PRQA_SIZE_T);
char*                                             __builtin_strpbrk(const char*,const char*);
char*                                             __builtin_strrchr(const char*,int);
PRQA_SIZE_T                                       __builtin_strspn(const char*,const char*);
char*                                             __builtin_strstr(const char*,const char*);
int                                               __builtin_fprintf(void*, const char*, ...);
int                                               __builtin_fprintf_unlocked(void*, const char*, ...);
int                                               __builtin_fputc(int, void*);
int                                               __builtin_fputc_unlocked(int, void*);
int                                               __builtin_fputs(const char*, void*);
int                                               __builtin_fputs_unlocked(const char*, void*);
int                                               __builtin_fscanf(void*, const char*, ...);
PRQA_SIZE_T                                       __builtin_fwrite(const void*, PRQA_SIZE_T, PRQA_SIZE_T, void*);
PRQA_SIZE_T                                       __builtin_fwrite_unlocked(const void*, PRQA_SIZE_T, PRQA_SIZE_T, void*);
int                                               __builtin_printf(const char*, ...);
int                                               __builtin_printf_unlocked(const char*, ...);
int                                               __builtin_putchar(int);
int                                               __builtin_putchar_unlocked(int);
int                                               __builtin_puts(const char*);
int                                               __builtin_puts_unlocked(const char*);
int                                               __builtin_scanf(const char*, ...);
int                                               __builtin_snprintf(char*, PRQA_SIZE_T, const char*, ...);
int                                               __builtin_sprintf(char*, const char*, ...);
int                                               __builtin_sscanf(const char*,const char*, ...);
template <typename __va_list_tag> int             __builtin_vfprintf(void*, const char*, __va_list_tag*);
template <typename __va_list_tag> int             __builtin_vfscanf(void*, const char*, __va_list_tag*);
template <typename __va_list_tag> int             __builtin_vprintf(const char*, __va_list_tag*);
template <typename __va_list_tag> int             __builtin_vscanf(const char*, __va_list_tag*);
template <typename __va_list_tag> int             __builtin_vsnprintf(char*, PRQA_SIZE_T, const char *, __va_list_tag*);
int                                               __builtin_vsprintf(char*,const char*,__builtin_va_list);
template <typename __va_list_tag> int             __builtin_vsscanf(const char*, const char*, __va_list_tag*);
void                                              __builtin_abort();
int                                               __builtin_abs(int);
template<typename T> T *                          __builtin_addressof(T &);
void*                                             __builtin_aggregate_incoming_address(...);
void*                                             __builtin_alloca(PRQA_SIZE_T);
void*                                             __builtin_apply(void (*)(...), void*, PRQA_SIZE_T);
void*                                             __builtin_apply_args(...);
int                                               __builtin_args_info(const int);
void*                                             __builtin_assume_aligned(const void *, PRQA_SIZE_T, ...);
void*                                             __builtin_calloc(PRQA_SIZE_T, PRQA_SIZE_T);
int                                               __builtin_classify_type(...);
template <typename INT> int                       __builtin_constant_p(INT);
char*                                             __builtin_dcgettext(const char*,const char*,int);
char*                                             __builtin_dgettext(const char*,const char*);
void*                                             __builtin_dwarf_cfa();
unsigned int                                      __builtin_dwarf_sp_column();
void                                              __builtin___builtin_eh_return(int,const char*);
int                                               __builtin_eh_return_data_regno(const int);
void                                              __builtin_exit(int);
void*                                             __builtin_extract_return_addr(void*);
void*                                             __builtin_frame_address(const unsigned int);
void*                                             __builtin_frob_return_addr(void*);
char*                                             __builtin_gettext(const char*);
template <typename LONG_INT> LONG_INT             __builtin_imaxabs(LONG_INT);
void                                              __builtin_init_dwarf_reg_size_table(void*);
int                                               __builtin_isgreater(...);
int                                               __builtin_isgreaterequal(...);
int                                               __builtin_isless(...);
int                                               __builtin_islessequal(...);
int                                               __builtin_islessgreater(...);
int                                               __builtin_isunordered(...);
long int                                          __builtin_labs(long int);
long long int                                     __builtin_llabs(long long int);
void                                              __builtin_longjmp(void*, const int);
void*                                             __builtin_malloc(PRQA_SIZE_T);
void*                                             __builtin_next_arg(...);
void                                              __builtin_prefetch(const void*, ...);
void                                              __builtin_return(void*);
void*                                             __builtin_return_address(const unsigned int);
void*                                             __builtin_saveregs(...);
int                                               __builtin_setjmp(void*);

// Using PTRDIFF_T as this should be ssize_t which practise has the
// same type.  Also - it is very unlikely that this will matter since
// these functions are only used by QA C/C++
PRQA_PTRDIFF_T                                    __builtin_strfmon(char*, PRQA_SIZE_T, const char*, ...);
PRQA_SIZE_T                                       __builtin_strftime(char*, PRQA_SIZE_T, const char*, const void*);

void                                              __builtin_unwind_init();
template <typename INT1, typename INT2> INT1      __sync_fetch_and_add(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_fetch_and_sub(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_fetch_and_or(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_fetch_and_and(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_fetch_and_xor(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_fetch_and_nand(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_add_and_fetch(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_sub_and_fetch(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_or_and_fetch(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_and_and_fetch(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_xor_and_fetch(INT1*, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_nand_and_fetch(INT1*, INT2, ...);
template <typename INT1, typename INT2> bool      __sync_bool_compare_and_swap(INT1*, INT2, INT2, ...);
template <typename INT1, typename INT2> INT1      __sync_val_compare_and_swap(INT1*, INT2, INT2, ...);
void                                              __sync_synchronize(...);
template <typename INT1, typename INT2> INT1      __sync_lock_test_and_set(INT1*, INT2, ...);
template <typename INT> INT                       __sync_lock_release (INT*, ...);

size_t __builtin_object_size (const void * ptr, int type);

int __builtin___sprintf_chk (char *s, int flag, size_t os, const char *fmt, ...);
int __builtin___snprintf_chk (char *s, size_t maxlen, int flag, size_t os,
                              const char *fmt, ...);
int __builtin___vsprintf_chk (char *s, int flag, size_t os, const char *fmt,
                              __builtin_va_list ap);
int __builtin___vsnprintf_chk (char *s, size_t maxlen, int flag, size_t os,
                               const char *fmt, __builtin_va_list ap);

void* __builtin___memcpy_chk(void*, const void*, PRQA_SIZE_T, PRQA_SIZE_T);
void* __builtin___memmove_chk(void*, const void*, PRQA_SIZE_T, PRQA_SIZE_T);
char* __builtin___strcpy_chk(char*, const char*, PRQA_SIZE_T);
char* __builtin___strcat_chk(char*, const char*, PRQA_SIZE_T);
char* __builtin___strncat_chk(char*, const char*, PRQA_SIZE_T, PRQA_SIZE_T);
void* __builtin___memset_chk(void*, int, PRQA_SIZE_T, PRQA_SIZE_T);
char* __builtin___strncpy_chk(char*, const char*, PRQA_SIZE_T, PRQA_SIZE_T);
char* __builtin___stpcpy_chk(char*, const char*, PRQA_SIZE_T);
char* __builtin___stpncpy_chk(char*, const char*, PRQA_SIZE_T, PRQA_SIZE_T);

#endif
