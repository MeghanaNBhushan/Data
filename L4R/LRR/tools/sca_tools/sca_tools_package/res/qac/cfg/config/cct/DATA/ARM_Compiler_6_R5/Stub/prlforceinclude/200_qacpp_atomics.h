// qacpp_atomics.h
//

#ifndef PRLGCC_INCLUDED_QACPP_ATOMICS
#define PRLGCC_INCLUDED_QACPP_ATOMICS

#include "400_qacpp_nullptr.h"

/* Atomics */
typedef int _Atomic_word ;
template<typename INT> INT __atomic_load_n(INT *, int);
template<typename INT1, typename INT2> void __atomic_load(INT1 *, INT2 *, int);
template<typename INT1, typename INT2> void __atomic_store_n(INT1 *, INT2, int);
template<typename INT1, typename INT2> void __atomic_store(INT1 *, INT2 *, int);
template<typename INT1, typename INT2> INT1 __atomic_exchange_n(INT1 *, INT2, int);
template<typename INT1, typename INT2, typename INT3> void __atomic_exchange(INT1 *, INT2 *, INT3 *, int);
template<typename INT1, typename INT2, typename INT3> bool __atomic_compare_exchange_n(INT1 *, INT2 *, INT3, bool, int, int);
template<typename INT1, typename INT2, typename INT3> bool __atomic_compare_exchange(INT1 *, INT2 *, INT3 *, bool, int, int);

#define __atomic_load_4 __atomic_load_n
#define __atomic_load_8 __atomic_load_n
#define __atomic_store_4 __atomic_store_n
#define __atomic_store_8 __atomic_store_n


template<typename INT1, typename INT2> INT1 __atomic_add_fetch(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_sub_fetch(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_and_fetch(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_xor_fetch(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_or_fetch(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_nand_fetch(INT1 *, INT2, int);

template<typename INT1, typename INT2> INT1 __atomic_fetch_add(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_fetch_sub(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_fetch_and(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_fetch_xor(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_fetch_or(INT1 *, INT2, int);
template<typename INT1, typename INT2> INT1 __atomic_fetch_nand(INT1 *, INT2, int);

template<typename INT> bool __atomic_test_and_set(INT *, int);
template<typename INT> void __atomic_clear(INT *, int);
void __atomic_thread_fence(int);
void __atomic_signal_fence(int);
template<typename INT> bool __atomic_always_lock_free(PRQA_SIZE_T, INT const *);
/* According to
https://gcc.gnu.org/onlinedocs/gcc-5.2.0/gcc/_005f_005fatomic-Builtins.html
the following two declarations need to use void* for the pointer argument.
*/
bool __atomic_always_lock_free(PRQA_SIZE_T, void *p);
bool __atomic_is_lock_free(PRQA_SIZE_T, void *p);
template<typename INT> bool __atomic_is_lock_free(PRQA_SIZE_T, INT const *);

void __c11_atomic_thread_fence(int);
void __c11_atomic_signal_fence(int);
template<typename INT1, typename INT2>
INT2 __c11_atomic_exchange(INT1 *, INT2, int);
template<typename INT1, typename INT2>
void __c11_atomic_store(INT1 *, INT2, int);
template<typename INT1>
INT1 __c11_atomic_load(INT1 *, int);
template<typename INT1, typename INT2>
INT1 __c11_atomic_fetch_add(INT1 *, INT2, int);
template<typename INT1, typename INT2>
INT1 __c11_atomic_fetch_sub(INT1 *, INT2, int);
template<typename INT1, typename INT2, typename INT3>
bool __c11_atomic_compare_exchange_weak(INT1 *, INT2*, INT3, int, int);
template<typename INT1, typename INT2, typename INT3>
bool __c11_atomic_compare_exchange_strong(INT1 *, INT2*, INT3, int, int);
template<typename INT1, typename INT2>
INT1 __c11_atomic_fetch_or(INT1 *, INT2, int);
template<typename INT1, typename INT2>
INT1 __c11_atomic_fetch_and(INT1 *, INT2, int);

// #define _Atomic(T)              struct { T volatile __val; }
#define _Atomic(T) T

#endif
