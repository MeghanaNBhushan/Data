#ifndef GH_ARM_FI_H
#define GH_ARM_FI_H

/* Compilers may use another function within the assert macro to exit the 
 * program. QAC thus does not see an "exit" function and assumes the 
 * function returns, which it does not.
 * The below pragma tells QAC the compiler supplied function does not
 * return.
 */

#pragma PRQA_NO_RETURN _assert_
#pragma PRQA_NO_RETURN _assert

/* Depending on the code that the compiler maker uses within the assert macro,
 * QAC may issue warnings. It is also possible that when the NDEBUG macro is used
 * to suppress the assertion code, QAC may issue a "no side-effects" warning.
 * To eliminate these, we turn off all warnings for the assert macro.
 */
#pragma PRQA_MACRO_MESSAGES_OFF "assert"


/* Any other items that may be required in a "force-include" file should be placed below. */

/* intrinsics */
void __DI(void);
void __EI(void);
int __builtin_va_alist;
int __builtin_va_arg_incr();
int __va_aargnum();
int __va_ansiarg;
int __va_dargnum();
int __va_iargnum();
int __va_intreg;
int *__va_stkarg;

#define __noinline
#define __linkonce
#define __bytereversed
#define __bigendian
#define __littleendian
#define __packed
#define __nearcall
#define __farcall
#if defined(__V800__)
#define __callt
#endif

#if defined(__CORE_V850E3V5__) && defined(__RH850_FXU_TYPES__)
typedef long long __ev128_f32__;
#endif

#if defined(__CORE_V850E3V5__) && defined(__RH850_SIMD_TYPES__)
typedef long long __ev64_u16__;
typedef long long __ev64_s16__;
typedef long long __ev64_u32__;
typedef long long __ev64_s32__;
typedef long long __ev64_u64__;
typedef long long __ev64_s64__;
typedef long long __ev64_opaque__;
typedef long long __ev128_opaque__;
#endif

#if (__QAC_MAJOR__ < 96)
/* C99 */
#define _Pragma _ignore_paren
#endif

#else
#error "Multiple include"
#endif  /* ifndef GH_ARM_FI_H */

