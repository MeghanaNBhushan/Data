// sched.h
//

#ifndef PRLGCC_INCLUDED_BITS_SCHED
#define PRLGCC_INCLUDED_BITS_SCHED

#include_next <bits/sched.h>

#if defined (PRL_GCC_07)

#  if defined(__CPU_SET_S)
#    undef __CPU_SET_S
#    define __CPU_SET_S(cpu, setsize, cpusetp)                         \
  ( (cpu < 8 * (setsize))                                              \
      ? (((__cpu_mask *) ((cpusetp)->__bits))[__CPUELT (cpu)]          \
          |= __CPUMASK (cpu))                                          \
      : 0 )
#endif

#  if defined(__CPU_CLR_S)
#    undef __CPU_CLR_S
#    define __CPU_CLR_S(cpu, setsize, cpusetp)                         \
  ( (cpu < 8 * (setsize))                                              \
      ? (((__cpu_mask *) ((cpusetp)->__bits))[__CPUELT (cpu)]          \
          &= ~__CPUMASK (cpu))                                         \
      : 0 )
#endif


#  if defined(__CPU_ISSET_S)
#    undef __CPU_ISSET_S
#    define __CPU_ISSET_S(cpu, setsize, cpusetp)                       \
  ((cpu < 8 * (setsize))                                               \
      ? ((((const __cpu_mask *) ((cpusetp)->__bits))[__CPUELT (cpu)]   \
              & __CPUMASK (cpu))) != 0                                 \
      : 0 )
#endif

namespace __qacpp_sched
{
  cpu_set_t * __qacpp_cpu_op_s(size_t setsize, cpu_set_t *, cpu_set_t *, cpu_set_t *);
}
#  if defined (__CPU_OP_S)
#    undef __CPU_OP_S
#    define __CPU_OP_S(setsize, destset, srcset1, srcset2, op)         \
  __qacpp_sched::__qacpp_cpu_op_s(setsize, destset, srcset1, srcset2)
#  endif

#endif // defined (PRL_GCC_07)

#endif // PRLGCC_INCLUDED_BITS_SCHED
