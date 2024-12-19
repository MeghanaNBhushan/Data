#ifndef PRLGCC_INCLUDED_ARM_NEON
#define PRLGCC_INCLUDED_ARM_NEON

/* For arm_neon.h */
#ifdef __ARM_NEON__
typedef int __simd64_int8_t; 
typedef int __simd64_int16_t; 
typedef int __simd64_int32_t;
typedef int __builtin_neon_qi;
typedef int __builtin_neon_hi;
typedef int __builtin_neon_si;
typedef int __builtin_neon_di;
typedef int __builtin_neon_ci;
typedef int __builtin_neon_ei;
typedef int __builtin_neon_oi;
typedef int __builtin_neon_ti;
typedef int __builtin_neon_xi;
typedef float __builtin_neon_sf;
typedef float __simd64_float16_t;
typedef float __simd64_float32_t;
typedef int __simd64_poly8_t;
typedef int __simd64_poly16_t;
typedef int __builtin_neon_poly64;
typedef unsigned int __simd64_uint8_t; 
typedef unsigned int __simd64_uint16_t; 
typedef unsigned int __simd64_uint32_t;
typedef int __builtin_neon_uqi;
typedef int __builtin_neon_uhi;
typedef int __builtin_neon_usi;
typedef int __builtin_neon_udi;
typedef long __simd128_int8_t;
typedef long __simd128_int16_t;
typedef long __simd128_int32_t;
typedef long __simd128_int64_t;
typedef float __simd128_float32_t;
typedef int __simd128_poly8_t;
typedef int __simd128_poly16_t;
typedef long __simd128_uint8_t;
typedef long __simd128_uint16_t;
typedef long __simd128_uint32_t;
typedef long __simd128_uint64_t;
typedef int __builtin_neon_poly8;
typedef int __builtin_neon_poly16;
typedef int __builtin_neon_poly32;
typedef int __builtin_neon_poly64;
typedef int __builtin_neon_poly128;
#endif

#ifdef __ARM_NEON
typedef int __Poly8_t;
typedef int __Poly16_t;
typedef int __Poly64_t;
typedef int __Poly128_t;
typedef float __fp16;
typedef struct { signed char _f[8]; } __Int8x8_t;
typedef struct { short _f[4]; } __Int16x4_t;
typedef struct { int _f[2]; } __Int32x2_t;
typedef struct { long _f[1]; } __Int64x1_t;
typedef struct { float _f[4]; } __Float16x4_t;
typedef struct { float _f[2]; } __Float32x2_t;
typedef struct { __Poly8_t _f[8]; } __Poly8x8_t;
typedef struct { __Poly16_t _f[4]; } __Poly16x4_t;
typedef struct { unsigned char _f[8]; } __Uint8x8_t;
typedef struct { unsigned short _f[4]; } __Uint16x4_t;
typedef struct { unsigned int _f[2]; } __Uint32x2_t;
typedef struct { double _f[1]; } __Float64x1_t;
typedef struct { unsigned long _f[1]; } __Uint64x1_t;
typedef struct { signed char _f[16]; } __Int8x16_t;
typedef struct { short _f[8]; } __Int16x8_t;
typedef struct { int _f[4]; } __Int32x4_t;
typedef struct { long _f[2]; } __Int64x2_t;
typedef struct { float _f[8]; } __Float16x8_t;
typedef struct { float _f[4]; } __Float32x4_t;
typedef struct { double _f[2]; } __Float64x2_t;
typedef struct { __Poly8_t _f[16]; } __Poly8x16_t;
typedef struct { __Poly16_t _f[8]; } __Poly16x8_t;
typedef struct { __Poly64_t _f[1]; } __Poly64x1_t;
typedef struct { __Poly64_t _f[2]; } __Poly64x2_t;
typedef struct { unsigned char _f[16]; } __Uint8x16_t;
typedef struct { unsigned short _f[8]; } __Uint16x8_t;
typedef struct { unsigned int _f[4]; } __Uint32x4_t;
typedef struct { unsigned long _f[2]; } __Uint64x2_t;
typedef int __builtin_aarch64_simd_qi;
typedef int __builtin_aarch64_simd_hi;
typedef int __builtin_aarch64_simd_si;
typedef int __builtin_aarch64_simd_di;
typedef float __builtin_aarch64_simd_hf;
typedef float __builtin_aarch64_simd_sf;
typedef float __builtin_aarch64_simd_df;
typedef int __builtin_aarch64_simd_ci;
typedef int __builtin_aarch64_simd_oi;
typedef int __builtin_aarch64_simd_xi;
#endif

#endif
