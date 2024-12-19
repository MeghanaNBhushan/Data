#ifndef PRLGCC_INCLUDED_ARM_NEON
#define PRLGCC_INCLUDED_ARM_NEON

/* For arm_neon.h */
#ifdef __ARM_NEON__
typedef __qacpp_integral_type<class __qacpp__simd64_int8_t, int> __simd64_int8_t; 
typedef __qacpp_integral_type<class __qacpp__simd64_int16_t, int> __simd64_int16_t; 
typedef __qacpp_integral_type<class __qacpp__simd64_int32_t, int> __simd64_int32_t;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_qi, int> __builtin_neon_qi;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_hi, int> __builtin_neon_hi;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_si, int> __builtin_neon_si;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_di, int> __builtin_neon_di;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_ci, int> __builtin_neon_ci;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_ei, int> __builtin_neon_ei;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_oi, int> __builtin_neon_oi;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_ti, int> __builtin_neon_ti;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_xi, int> __builtin_neon_xi;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_sf, float> __builtin_neon_sf;
typedef __qacpp_integral_type<class __qacpp__simd64_float16_t, float> __simd64_float16_t;
typedef __qacpp_integral_type<class __qacpp__simd64_float32_t, float> __simd64_float32_t;
typedef __qacpp_integral_type<class __qacpp__simd64_poly8_t, int> __simd64_poly8_t;
typedef __qacpp_integral_type<class __qacpp__simd64_poly16_t, int> __simd64_poly16_t;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_poly64, int> __builtin_neon_poly64;
typedef __qacpp_integral_type<class __qacpp__simd64_uint8_t, unsigned int >__simd64_uint8_t; 
typedef __qacpp_integral_type<class __qacpp__simd64_uint16_t, unsigned int> __simd64_uint16_t; 
typedef __qacpp_integral_type<class __qacpp__simd64_uint32_t, unsigned int> __simd64_uint32_t;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_uqi, int> __builtin_neon_uqi;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_uhi, int> __builtin_neon_uhi;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_usi, int> __builtin_neon_usi;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_udi, int> __builtin_neon_udi;
typedef __qacpp_integral_type<class __qacpp__simd128_int8_t, long> __simd128_int8_t;
typedef __qacpp_integral_type<class __qacpp__simd128_int16_t, long> __simd128_int16_t;
typedef __qacpp_integral_type<class __qacpp__simd128_int32_t, long> __simd128_int32_t;
typedef __qacpp_integral_type<class __qacpp__simd128_int64_t, long> __simd128_int64_t;
typedef __qacpp_integral_type<class __qacpp__simd128_float32_t, float> __simd128_float32_t;
typedef __qacpp_integral_type<class __qacpp__simd128_poly8_t, int> __simd128_poly8_t;
typedef __qacpp_integral_type<class __qacpp__simd128_poly16_t, int> __simd128_poly16_t;
typedef __qacpp_integral_type<class __qacpp__simd128_uint8_t, long> __simd128_uint8_t;
typedef __qacpp_integral_type<class __qacpp__simd128_uint16_t, long> __simd128_uint16_t;
typedef __qacpp_integral_type<class __qacpp__simd128_uint32_t, long> __simd128_uint32_t;
typedef __qacpp_integral_type<class __qacpp__simd128_uint64_t, long> __simd128_uint64_t;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_poly8, int> __builtin_neon_poly8;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_poly16, int> __builtin_neon_poly16;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_poly32, int> __builtin_neon_poly32;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_poly64, int> __builtin_neon_poly64;
typedef __qacpp_integral_type<class __qacpp__builtin_neon_poly128, int> __builtin_neon_poly128;
#endif

#ifdef __ARM_NEON
typedef float __fp16;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int8_t, signed char> _f[8];
} __Int8x8_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int16_t, short> _f[4];
} __Int16x4_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int32_t, int> _f[2];
} __Int32x2_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int64_t, long> _f[1];
} __Int64x1_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Float16_t, float> _f[4];
} __Float16x4_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Float16_t, int> _f[8];
} __Float16x8_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Float32_t, float> _f[2];
} __Float32x2_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Poly8_t, int> _f[8];
} __Poly8x8_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Poly16_t, int> _f[4];
} __Poly16x4_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Poly64_t, int> _f[1];
} __Poly64x1_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Uint8_t, unsigned char> _f[8];
} __Uint8x8_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Uint16_t, unsigned short> _f[4];
} __Uint16x4_t;
typedef struct {
 __qacpp_integral_type<class __qacpp__Uint32_t, unsigned int> _f[2];
} __Uint32x2_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Float64_t, double> _f[1];
} __Float64x1_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Uint64_t, unsigned long> _f[1];
} __Uint64x1_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int8_t, signed char> _f[16];
} __Int8x16_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int16_t, short> _f[8];
} __Int16x8_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int32_t, int> _f[4];
} __Int32x4_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Int64_t, long> _f[2];
} __Int64x2_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Float32_t, float> _f[4];
} __Float32x4_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Float64_t, double> _f[2];
} __Float64x2_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Poly8_t, int> _f[16];
} __Poly8x16_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Poly16_t, int> _f[8];
} __Poly16x8_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Poly64_t, int> _f[2];
} __Poly64x2_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Uint8_t, unsigned char> _f[16];
} __Uint8x16_t;
typedef struct {
__qacpp_integral_type<class __qacpp__Uint16_t, unsigned short> _f[8];
} __Uint16x8_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Uint32_t, unsigned int> _f[4];
} __Uint32x4_t;
typedef struct {
  __qacpp_integral_type<class __qacpp__Uint64_t, unsigned long> _f[2];
} __Uint64x2_t;
typedef __qacpp_integral_type<class __qacpp__Poly8_t, int> __Poly8_t;
typedef __qacpp_integral_type<class __qacpp__Poly16_t, int> __Poly16_t;
typedef __qacpp_integral_type<class __qacpp__Poly64_t, int> __Poly64_t;
typedef __qacpp_integral_type<class __qacpp__Poly128_t, int> __Poly128_t;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_qi, int> __builtin_aarch64_simd_qi;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_hi, int> __builtin_aarch64_simd_hi;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_si, int> __builtin_aarch64_simd_si;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_di, int> __builtin_aarch64_simd_di;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_sf, int> __builtin_aarch64_simd_sf;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_df, int> __builtin_aarch64_simd_df;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_ci, int> __builtin_aarch64_simd_ci;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_oi, int> __builtin_aarch64_simd_oi;
typedef __qacpp_integral_type<class __qacpp__builtin_aarch64_simd_xi, int> __builtin_aarch64_simd_xi;
#endif

#endif
