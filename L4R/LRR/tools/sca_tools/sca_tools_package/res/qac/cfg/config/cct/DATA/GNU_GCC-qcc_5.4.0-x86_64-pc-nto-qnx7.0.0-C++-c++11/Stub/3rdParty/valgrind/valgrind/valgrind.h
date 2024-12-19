// valgrind.h
//

#ifndef PRLGCC_INCLUDED_VALGRIND
#define PRLGCC_INCLUDED_VALGRIND

#if defined PRL_GCC_07

#  define NVALGRIND

#endif


#include_next "valgrind/valgrind.h"


#if defined PRL_GCC_07

#  if defined VALGRIND_DO_CLIENT_REQUEST_EXPR

#    undef VALGRIND_DO_CLIENT_REQUEST_EXPR
#    define VALGRIND_DO_CLIENT_REQUEST_EXPR(                          \
            _zzq_default, _zzq_request,                               \
            _zzq_arg1, _zzq_arg2, _zzq_arg3, _zzq_arg4, _zzq_arg5)    \
          (_zzq_default)

#  endif // VALGRIND_DO_CLIENT_REQUEST_EXPR


#  if (__VALGRIND_MAJOR__ < 3) || ((__VALGRIND_MAJOR__ == 3) && (__VALGRIND_MINOR__ < 8))

#    if defined VALGRIND_NON_SIMD_CALL0
#      undef VALGRIND_NON_SIMD_CALL0
#    endif // VALGRIND_NON_SIMD_CALL0
#    define VALGRIND_NON_SIMD_CALL0(_qyy_fn)

#    if defined VALGRIND_NON_SIMD_CALL1
#      undef VALGRIND_NON_SIMD_CALL1
#    endif // VALGRIND_NON_SIMD_CALL1
#    define VALGRIND_NON_SIMD_CALL1(_qyy_fn, _qyy_arg1)

#    if defined VALGRIND_NON_SIMD_CALL2
#      undef VALGRIND_NON_SIMD_CALL2
#    endif // VALGRIND_NON_SIMD_CALL2
#    define VALGRIND_NON_SIMD_CALL2(_qyy_fn, _qyy_arg1, _qyy_arg2)

#    if defined VALGRIND_NON_SIMD_CALL3
#      undef VALGRIND_NON_SIMD_CALL3
#    endif // VALGRIND_NON_SIMD_CALL3
#    define VALGRIND_NON_SIMD_CALL3(_qyy_fn, _qyy_arg1, _qyy_arg2, _qyy_arg3)

#    if defined VALGRIND_COUNT_ERRORS
#      undef VALGRIND_COUNT_ERRORS
#    endif // VALGRIND_COUNT_ERRORS
#    define VALGRIND_COUNT_ERRORS

#    if defined VALGRIND_MALLOCLIKE_BLOCK
#      undef VALGRIND_MALLOCLIKE_BLOCK
#    endif // VALGRIND_MALLOCLIKE_BLOCK
#    define VALGRIND_MALLOCLIKE_BLOCK(addr, sizeB, rzB, is_zeroed)

#    if defined VALGRIND_RESIZEINPLACE_BLOCK
#      undef VALGRIND_RESIZEINPLACE_BLOCK
#    endif // VALGRIND_RESIZEINPLACE_BLOCK
#    define VALGRIND_RESIZEINPLACE_BLOCK(addr, oldSizeB, newSizeB, rzB)

#    if defined VALGRIND_FREELIKE_BLOCK
#      undef VALGRIND_FREELIKE_BLOCK
#    endif // VALGRIND_FREELIKE_BLOCK
#    define VALGRIND_FREELIKE_BLOCK(addr, rzB)

#    if defined VALGRIND_CREATE_MEMPOOL
#      undef VALGRIND_CREATE_MEMPOOL
#    endif // VALGRIND_CREATE_MEMPOOL
#    define VALGRIND_CREATE_MEMPOOL(pool, rzB, is_zeroed)

#    if defined VALGRIND_DESTROY_MEMPOOL
#      undef VALGRIND_DESTROY_MEMPOOL
#    endif // VALGRIND_DESTROY_MEMPOOL
#    define VALGRIND_DESTROY_MEMPOOL(pool)

#    if defined VALGRIND_MEMPOOL_ALLOC
#      undef VALGRIND_MEMPOOL_ALLOC
#    endif // VALGRIND_MEMPOOL_ALLOC
#    define VALGRIND_MEMPOOL_ALLOC(pool, addr, size)

#    if defined VALGRIND_MEMPOOL_FREE
#      undef VALGRIND_MEMPOOL_FREE
#    endif // VALGRIND_MEMPOOL_FREE
#    define VALGRIND_MEMPOOL_FREE(pool, addr)

#    if defined VALGRIND_MEMPOOL_TRIM
#      undef VALGRIND_MEMPOOL_TRIM
#    endif // VALGRIND_MEMPOOL_TRIM
#    define VALGRIND_MEMPOOL_TRIM(pool, addr, size)

#    if defined VALGRIND_MOVE_MEMPOOL
#      undef VALGRIND_MOVE_MEMPOOL
#    endif // VALGRIND_MOVE_MEMPOOL
#    define VALGRIND_MOVE_MEMPOOL(poolA, poolB)

#    if defined VALGRIND_MEMPOOL_CHANGE
#      undef VALGRIND_MEMPOOL_CHANGE
#    endif // VALGRIND_MEMPOOL_CHANGE
#    define VALGRIND_MEMPOOL_CHANGE(pool, addrA, addrB, size)

#    if defined VALGRIND_MEMPOOL_EXISTS
#      undef VALGRIND_MEMPOOL_EXISTS
#    endif // VALGRIND_MEMPOOL_EXISTS
bool __qacpp_valgrind_mempool_exists[];
#    define VALGRIND_MEMPOOL_EXISTS(pool) __qacpp_valgrind_mempool_exists[__LINE__]

#    if defined VALGRIND_STACK_REGISTER
#      undef VALGRIND_STACK_REGISTER
#    endif // VALGRIND_STACK_REGISTER
#    define VALGRIND_STACK_REGISTER(start, end)

#    if defined VALGRIND_STACK_DEREGISTER
#      undef VALGRIND_STACK_DEREGISTER
#    endif // VALGRIND_STACK_DEREGISTER
#    define VALGRIND_STACK_DEREGISTER(id)

#    if defined VALGRIND_STACK_CHANGE
#      undef VALGRIND_STACK_CHANGE
#    endif // VALGRIND_STACK_CHANGE
#    define VALGRIND_STACK_CHANGE(id, start, end)

#    if defined VALGRIND_LOAD_PDB_DEBUGINFO
#      undef VALGRIND_LOAD_PDB_DEBUGINFO
#    endif // VALGRIND_LOAD_PDB_DEBUGINFO
#    define VALGRIND_LOAD_PDB_DEBUGINFO(fd, ptr, total_size, delta)

#    if defined VALGRIND_MAP_IP_TO_SRCLOC
#      undef VALGRIND_MAP_IP_TO_SRCLOC
#    endif // VALGRIND_MAP_IP_TO_SRCLOC
#    define VALGRIND_MAP_IP_TO_SRCLOC(addr, buf64)

#    if defined VALGRIND_DISABLE_ERROR_REPORTING
#      undef VALGRIND_DISABLE_ERROR_REPORTING
#    endif // VALGRIND_DISABLE_ERROR_REPORTING
#    define VALGRIND_DISABLE_ERROR_REPORTING

#    if defined VALGRIND_ENABLE_ERROR_REPORTING
#      undef VALGRIND_ENABLE_ERROR_REPORTING
#    endif // VALGRIND_ENABLE_ERROR_REPORTING
#    define VALGRIND_ENABLE_ERROR_REPORTING

#    if defined VALGRIND_MONITOR_COMMAND
#      undef VALGRIND_MONITOR_COMMAND
#    endif // VALGRIND_MONITOR_COMMAND
#    define VALGRIND_MONITOR_COMMAND

#  endif // (__VALGRIND_MAJOR__ <= 3) || (__VALGRIND_MINOR__ < 8)

#endif // PRL_GCC_07


#endif
