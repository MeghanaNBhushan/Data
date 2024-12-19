#define ONE                                         0x1
#define TWO                                         ONE + ONE
#define THREE                                       (TWO + TWO) - ONE
#define ONE_ONE                                     0x11
#define ONE_TWO                                     ONE_ONE + 0x1
#define ONE_TWO_ONE                                 0x121
#define MAX                                         0xFFFFFFFF

#define MEM_VAS_DRAM_SIZE                           0x40000000 // 1GB
#define MEM_VAS_RTRAM_BASE                          0xEB200000
#define MEM_VAS_BOOTMGR_MAXSIZE                     (0x32000 - 0x2800) // 200kB
#define MEM_VAS_RPU_MAXSIZE                         0x900000 // 9 MB
#define MEM_VAS_APU_MAXSIZE                         (MEM_VAS_DRAM_SIZE - MEM_VAS_RPU_MAXSIZE)
#define MEM_VAS_HSMRPUEX_BASE                       0xEB23C000
#define MEM_VAS_HSMRPUEX_MAXSIZE                    0x2000
#define MEM_VAS_BOOTMGR_BASE                        (MEM_VAS_RTRAM_BASE + 0x2800) // add 10 KB because of IPL loading