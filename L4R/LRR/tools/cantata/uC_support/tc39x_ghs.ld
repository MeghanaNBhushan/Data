/*

#define BSS_FLAGS (CLEAR) (NOLOAD)
#define ROMSECTION(x) ROM_NOCOPY(x)
#define ROMSECTION(x) ROM(x)
*/
/* entry point */
OPTION("-e rba_SysPreInitCfgCore0")
OPTION("-u rba_SysPreInitCfgCore0")

DEFAULTS {
LCF_CSA0_SIZE = 32k;
LCF_USTACK0_SIZE = 32k;
LCF_ISTACK0_SIZE = 1k;

LCF_CSA1_SIZE = 8k;
LCF_USTACK1_SIZE = 2k;
LCF_ISTACK1_SIZE = 1k;

LCF_CSA2_SIZE = 8k;
LCF_USTACK2_SIZE = 32k;
LCF_ISTACK2_SIZE = 1k;

LCF_CSA3_SIZE = 8k;
LCF_USTACK3_SIZE = 32k;
LCF_ISTACK3_SIZE = 1k;

LCF_CSA4_SIZE = 8k;
LCF_USTACK4_SIZE = 32k;
LCF_ISTACK4_SIZE = 1k;

LCF_CSA5_SIZE = 8k;
LCF_USTACK5_SIZE = 32k;
LCF_ISTACK5_SIZE = 1k;

LCF_HEAP_SIZE = 8k;

LCF_DSPR5_START = 0x10000000;
LCF_DSPR5_SIZE = 96k;

LCF_DSPR4_START = 0x30000000;
LCF_DSPR4_SIZE = 96k;

LCF_DSPR3_START = 0x40000000;
LCF_DSPR3_SIZE = 96k;

LCF_DSPR2_START = 0x50000000;
LCF_DSPR2_SIZE = 96k;

LCF_DSPR1_START = 0x60000000;
LCF_DSPR1_SIZE = 96k;

LCF_DSPR0_START = 0x70000000;
LCF_DSPR0_SIZE = 96k;

__dlmu0_nc_START = 0xb0000000;
__dlmu0_nc_SIZE = 64K;
__dlmu1_nc_START = 0xb0010000;
__dlmu1_nc_SIZE = 64K;
__dlmu2_nc_START = 0xb0020000;
__dlmu2_nc_SIZE = 64K;
__dlmu3_nc_START = 0xb0030000;
__dlmu3_nc_SIZE = 64K;
__dlmu4_nc_START = 0xb0140000;
__dlmu4_nc_SIZE = 64K;
__dlmu5_nc_START = 0xb0150000;
__dlmu5_nc_SIZE = 64K;
    
__lmu0_nc_START = 0xb0040000;
__lmu0_nc_SIZE = 256K
}

MEMORY
{
    /* dsram5_local : ORIGIN = 0xd0000000, LENGTH = 96K */
    dsram5 : ORIGIN = LCF_DSPR5_START, LENGTH = LCF_DSPR5_SIZE
    psram5 : ORIGIN = 0x10100000, LENGTH = 64K

    /* dsram4_local : ORIGIN = 0xd0000000, LENGTH = 96K */
    dsram4 : ORIGIN = LCF_DSPR4_START, LENGTH = LCF_DSPR4_SIZE
    psram4 : ORIGIN = 0x30100000, LENGTH = 64K

    /* dsram3_local : ORIGIN = 0xd0000000, LENGTH = 96K */
    dsram3 : ORIGIN = LCF_DSPR3_START, LENGTH = LCF_DSPR3_SIZE
    psram3 : ORIGIN = 0x40100000, LENGTH = 64K

    /* dsram2_local : ORIGIN = 0xd0000000, LENGTH = 96K */
    dsram2 : ORIGIN = LCF_DSPR2_START, LENGTH = LCF_DSPR2_SIZE
    psram2 : ORIGIN = 0x50100000, LENGTH = 64K

    /* dsram1_local : ORIGIN = 0xd0000000, LENGTH = 96K */
    dsram1 : ORIGIN = LCF_DSPR1_START, LENGTH = LCF_DSPR1_SIZE
    psram1 : ORIGIN = 0x60100000, LENGTH = 64K

    /* dsram0_local : ORIGIN = 0xd0000000, LENGTH = 96K */
    dsram0 : ORIGIN = LCF_DSPR0_START, LENGTH = LCF_DSPR0_SIZE
    psram0 : ORIGIN = 0x70100000, LENGTH = 64K

    psram_local : ORIGIN = 0xc0000000, LENGTH = 96K

    Applpfls0 : ORIGIN = 0x80074000, LENGTH = 5680K

    /* pfls2 : ORIGIN = 0x80600000, LENGTH = 3M
    pfls2_nc : ORIGIN = 0xa0600000, LENGTH = 3M

    pfls3 : ORIGIN = 0x80900000, LENGTH = 3M
    pfls3_nc : ORIGIN = 0xa0900000, LENGTH = 3M

    pfls4 : ORIGIN = 0x80c00000, LENGTH = 3M
    pfls4_nc : ORIGIN = 0xa0c00000, LENGTH = 3M

    pfls5 : ORIGIN = 0x80f00000, LENGTH = 1M
    pfls5_nc : ORIGIN = 0xa0f00000, LENGTH = 1M */

    dfls0 : ORIGIN = 0xaf000000, LENGTH = 1M

    dlmu0 : ORIGIN = 0x90000000, LENGTH = 64K
    dlmu0_nc : ORIGIN = __dlmu0_nc_START, LENGTH = __dlmu0_nc_SIZE

    dlmu1 : ORIGIN = 0x90010000, LENGTH = 64K
    dlmu1_nc : ORIGIN = __dlmu1_nc_START, LENGTH = __dlmu1_nc_SIZE

    dlmu2 : ORIGIN = 0x90020000, LENGTH = 64K
    dlmu2_nc : ORIGIN = __dlmu2_nc_START, LENGTH = __dlmu2_nc_SIZE

    dlmu3 : ORIGIN = 0x90030000, LENGTH = 64K
    dlmu3_nc : ORIGIN = __dlmu3_nc_START, LENGTH = __dlmu3_nc_SIZE

    dlmu4 : ORIGIN = 0x90140000, LENGTH = 64K
    dlmu4_nc : ORIGIN = __dlmu4_nc_START, LENGTH = __dlmu4_nc_SIZE

    dlmu5 : ORIGIN = 0x90150000, LENGTH = 64K
    dlmu5_nc : ORIGIN = __dlmu5_nc_START, LENGTH = __dlmu5_nc_SIZE

	/* lmu non-cached  */
    lmu0_nc : ORIGIN = __lmu0_nc_START, LENGTH = __lmu0_nc_SIZE
}


/* for the size calculation of all flash blocks together ------------------- */
SECTIONS
{
     _DATA_BLOCK_SIZE = 0;
}

SECTIONS 
{ 
    _DATA_BLOCK_Applpfls0_START = ADDR(Applpfls0); 
    _DATA_BLOCK_Applpfls0_END = ADDR(Applpfls0) + sizeof(Applpfls0); 
    _DATA_BLOCK_Applpfls0_SIZE = sizeof(Applpfls0); 
    BLOCK_HEADER_Applpfls0_END = _DATA_BLOCK_Applpfls0_START; 
	
    .Applpfls0.begin (_DATA_BLOCK_Applpfls0_START) : {} > Applpfls0 
    
	.Applpfls0.BlockHeader (BLOCK_HEADER_Applpfls0_END) : 
    { 
        _BLOCK_HEADER_START = .;
        "*(.blockHeaderTableSection)"
    } > Applpfls0 
    BLOCK_HEADER_Applpfls0_END = .;
	
	.Applpfls0.VectorPointerTable (BLOCK_HEADER_Applpfls0_END) : 
    { 
       _VECTOR_TABLE_START = .;
       "*(.vectorTableSection)"
    } > Applpfls0 
    BLOCK_HEADER_Applpfls0_END = .;
	
	.Applpfls0.SubBlockPointerTable (BLOCK_HEADER_Applpfls0_END) : 
    { 
       _SUBBLOCK_POINTER_TABLE_START = .; 
       "*(.subBlockPointerTableSectionHead)" 
       "*(.subBlockPointerTableSection)"
    } > Applpfls0 
    BLOCK_HEADER_Applpfls0_END = .;
	
	/*.Applpfls0.user_rodata (BLOCK_HEADER_Applpfls0_END) : 
    { 
    } > Applpfls0 
    BLOCK_HEADER_Applpfls0_END = .; */
	
	.Applpfls0.rodata (BLOCK_HEADER_Applpfls0_END) : 
    { 
       "*(.rodata)" 
       _BUILDINFO_START = .; 
       "*(.buildinfo)"
    } > Applpfls0 
    BLOCK_HEADER_Applpfls0_END = .;
	
	.Applpfls0.start (BLOCK_HEADER_Applpfls0_END) : 
    { 
	    _start = .;
        "*(.start)"
    } > Applpfls0
	BLOCK_HEADER_Applpfls0_END = .;
	
	.Applpfls0.TraHa_trap_handlers : 
    { 
        "*(.text)"
    } > Applpfls0
	
	.Applpfls0.text : 
    { 
        "*(.text)"
		"*(.syscall)"
        "*(.TraHa_trap_handlers)" 
    } > Applpfls0
	
	.text  :
    {
        "*(.text)"
        "*(.text.*)"
    } > Applpfls0
	
	
}


SECTIONS	
{
	. = ALIGN(4);
	.ROM_CPU5_data ROM_NOCOPY(.CPU5.data) : > .
	__CPU5_ROM_data_START = ADDR(.ROM_CPU5_data);
	. = ALIGN(4);
	.ROM_CPU4_data ROM_NOCOPY(.CPU4.data) : > .
	__CPU4_ROM_data_START = ADDR(.ROM_CPU4_data);
	. = ALIGN(4);
	.ROM_CPU3_data ROM_NOCOPY(.CPU3.data) : > .
	__CPU3_ROM_data_START = ADDR(.ROM_CPU3_data);
	. = ALIGN(4);
	.ROM_CPU2_data ROM_NOCOPY(.CPU2.data) : > .
	/* .ROM_CPU2_data ROM_NOCOPY(.CPU2.data) : > dsram_ROMCOPYdata */
	__CPU2_ROM_data_START = ADDR(.ROM_CPU2_data);
	. = ALIGN(4);
	.ROM_CPU1_data ROM_NOCOPY(.CPU1.data) : > .
	__CPU1_ROM_data_START = ADDR(.ROM_CPU1_data);
	. = ALIGN(4);
	.ROM_CPU0_data ROM_NOCOPY(.CPU0.data) : > .
	__CPU0_ROM_data_START = ADDR(.ROM_CPU0_data);
	. = ALIGN(2);
	.ROM.CPU0.psram_text ROM_NOCOPY(.CPU0.psram_text) : > .
	. = ALIGN(2);
	.ROM.CPU2.psram_text ROM_NOCOPY(.CPU2.psram_text) : > .
	. = ALIGN(2);
	.ROM.CPU1.psram_text ROM_NOCOPY(.CPU1.psram_text) : > .
	. = ALIGN(4);
	
    .ROM_dlmu0_nc_data ROM_NOCOPY(.dlmu0_nc.data) : > . /* dlmu_ROMCOPYdata */
    __dlmu0_nc_ROM_data_START = ADDR(.ROM_dlmu0_nc_data);
    
    .ROM_dlmu1_nc_data ROM_NOCOPY(.dlmu1_nc.data) : > . /* dlmu_ROMCOPYdata */
    __dlmu1_nc_ROM_data_START = ADDR(.ROM_dlmu1_nc_data);
    
    .ROM_dlmu2_nc_data ROM_NOCOPY(.dlmu2_nc.data) : > . /* dlmu_ROMCOPYdata */
    __dlmu2_nc_ROM_data_START = ADDR(.ROM_dlmu2_nc_data);
    
    .ROM_dlmu3_nc_data ROM_NOCOPY(.dlmu3_nc.data) : > . /* dlmu_ROMCOPYdata */
    __dlmu3_nc_ROM_data_START = ADDR(.ROM_dlmu3_nc_data);
    
    .ROM_dlmu4_nc_data ROM_NOCOPY(.dlmu4_nc.data) : > . /* dlmu_ROMCOPYdata */
    __dlmu4_nc_ROM_data_START = ADDR(.ROM_dlmu4_nc_data);
    
    .ROM_dlmu5_nc_data ROM_NOCOPY(.dlmu5_nc.data) : > . /* dlmu_ROMCOPYdata */
    __dlmu5_nc_ROM_data_START = ADDR(.ROM_dlmu5_nc_data);
    
    .ROM_lmu0_nc_data ROM_NOCOPY(.lmu0_nc.data) : > . /* dlmu_ROMCOPYdata */
    __lmu0_nc_ROM_data_START = ADDR(.ROM_lmu0_nc_data);
    
    .ROM_default_data ROM_NOCOPY(.default_data) : > . /* dlmu_ROMCOPYdata */
    __default_ROM_data_START = ADDR(.ROM_default_data);
}

/* STACK placed at beginning of RAMs */
SECTIONS
{
   .CPU5.ustack (LCF_DSPR5_START):
    {
        __USTACK5_END = .;
        . = . + LCF_USTACK5_SIZE;
        __USTACK5 = .;
    } > dsram5
	
	.CPU5.istack (NOLOAD) (ADDR(.CPU5.ustack) + sizeof(.CPU5.ustack)):
    {
        __ISTACK5_END = .;
        . = . + LCF_ISTACK5_SIZE;
        __ISTACK5 = .;
    } > dsram5

    .CPU5.csa (NOLOAD) (ADDR(.CPU5.istack) + sizeof(.CPU5.istack)):
    {
       __CSA5 = .;
        . = . + LCF_CSA5_SIZE;
        __CSA5_END = .;
    } > dsram5

   .CPU4.ustack (LCF_DSPR4_START):
    {
        __USTACK4_END = .;
        . = . + LCF_USTACK4_SIZE;
        __USTACK4 = .;
    } > dsram4
	
    .CPU4.istack (NOLOAD) (ADDR(.CPU4.ustack) + sizeof(.CPU4.ustack)):
    {
        __ISTACK4_END = .;
        . = . + LCF_ISTACK4_SIZE;
        __ISTACK4 = .;
    } > dsram4

    .CPU4.csa (NOLOAD) (ADDR(.CPU4.istack) + sizeof(.CPU4.istack)):
    {
       __CSA4 = .;
        . = . + LCF_CSA4_SIZE;
        __CSA4_END = .;
    } > dsram4
	

   .CPU3.ustack (LCF_DSPR3_START):
    {
        __USTACK3_END = .;
        . = . + LCF_USTACK3_SIZE;
        __USTACK3 = .;
    } > dsram3
	
	.CPU3.istack (NOLOAD) (ADDR(.CPU3.ustack) + sizeof(.CPU3.ustack)):
    {
        __ISTACK3_END = .;
        . = . + LCF_ISTACK3_SIZE;
        __ISTACK3 = .;
    } > dsram3

    .CPU3.csa (NOLOAD) (ADDR(.CPU3.istack) + sizeof(.CPU3.istack)):
    {
       __CSA3 = .;
        . = . + LCF_CSA3_SIZE;
        __CSA3_END = .;
    } > dsram3

   .CPU2.ustack (LCF_DSPR2_START):
    {
        __USTACK2_END = .;
        . = . + LCF_USTACK2_SIZE;
        __USTACK2 = .;
    } > dsram2
	
	.CPU2.istack (NOLOAD) (ADDR(.CPU2.ustack) + sizeof(.CPU2.ustack)):
    {
        __ISTACK2_END = .;
        . = . + LCF_ISTACK2_SIZE;
        __ISTACK2 = .;
    } > dsram2

    .CPU2.csa (NOLOAD) (ADDR(.CPU2.istack) + sizeof(.CPU2.istack)):
    {
       __CSA2 = .;
        . = . + LCF_CSA2_SIZE;
        __CSA2_END = .;
    } > dsram2

    .CPU1.ustack (LCF_DSPR1_START):
    {
        __USTACK1_END = .;
        . = . + LCF_USTACK1_SIZE;
        __USTACK1 = .;
    } > dsram1
	
	.CPU1.istack (NOLOAD) (ADDR(.CPU1.ustack) + sizeof(.CPU1.ustack)):
    {
        __ISTACK1_END = .;
        . = . + LCF_ISTACK1_SIZE;
        __ISTACK1 = .;
    } > dsram1

    .CPU1.csa (NOLOAD) (ADDR(.CPU1.istack) + sizeof(.CPU1.istack)):
    {
        __CSA1 = .;
        . = . + LCF_CSA1_SIZE;
        __CSA1_END = .;
    } > dsram1

    .CPU0.ustack (LCF_DSPR0_START):
    {
        __USTACK0_END = .;
        . = . + LCF_USTACK0_SIZE;
        __USTACK0 = .;
    } > dsram0
	
	.CPU0.istack (NOLOAD) (ADDR(.CPU0.ustack) + sizeof(.CPU0.ustack)):
    {
        __ISTACK0_END = .;
        . = . + LCF_ISTACK0_SIZE;
        __ISTACK0 = .;
    } > dsram0

    .CPU0.csa (NOLOAD) (ADDR(.CPU0.istack) + sizeof(.CPU0.istack)):
    {
        __CSA0 = .;
        . = . + LCF_CSA0_SIZE;
        __CSA0_END = .;
    } > dsram0
	
	.intstack (NOLOAD) :
    {
    } > dsram0
}


SECTIONS
{
    .CPU5.data :
    {
        . = ALIGN(4) ;
        __CPU5_data_START = .;
        "*(.data_cpu5)"
        "*(.data_cpu5.*)"
    } > dsram5
    __CPU5_data_SIZE = sizeof(.CPU5.data); 

    .CPU5.bss  (CLEAR) (NOLOAD):
    {
        . = ALIGN(4) ;
        __CPU5_bss_START = .;
        "*(.bss_cpu5)"
        "*(.bss_cpu5.*)"
    } > dsram5
    __CPU5_bss_SIZE = sizeof(.CPU5.bss); 
	
	.CPU5.psram_text  :
    {
        . = ALIGN(2);
        "*(.cpu5_psram)"
    } > psram5
}

SECTIONS
{
    .CPU4.data :
    {
        . = ALIGN(4) ;
        __CPU4_data_START = .;
        "*(.data_cpu4)"
        "*(.data_cpu4.*)"
    } > dsram4
    __CPU4_data_SIZE = sizeof(.CPU4.data);

    .CPU4.bss  (CLEAR) (NOLOAD):
    {
        . = ALIGN(4) ;
        __CPU4_bss_START = .;
        "*(.bss_cpu4)"
        "*(.bss_cpu4.*)"
    } > dsram4
    __CPU4_bss_SIZE = sizeof(.CPU4.bss); 
	
	.CPU4.psram_text  :
    {
        . = ALIGN(2);
        "*(.cpu4_psram)"
    } > psram4
}

SECTIONS
{
    .CPU3.data :
    {
        . = ALIGN(4) ;
        __CPU3_data_START = .;
        "*(.data_cpu3)"
        "*(.data_cpu3.*)"
    } > dsram3
    __CPU3_data_SIZE = sizeof(.CPU3.data);

    .CPU3.bss  (CLEAR) (NOLOAD):
    {
        . = ALIGN(4) ;
        __CPU3_bss_START = .;
        "*(.bss_cpu3)"
        "*(.bss_cpu3.*)"
    } > dsram3
    __CPU3_bss_SIZE = sizeof(.CPU3.bss); 
	
	.CPU3.psram_text  :
    {
        . = ALIGN(2);
        "*(.cpu3_psram)"
    } > psram3
}

SECTIONS
{
    .CPU2.data :
    {
        . = ALIGN(4) ;
        __CPU2_data_START = .;
        "*(.data_cpu2)"
        "*(.data_cpu2.*)"
    } > dsram2
    __CPU2_data_SIZE = sizeof(.CPU2.data);

    .CPU2.bss  (CLEAR) (NOLOAD):
    {        
		. = ALIGN(4) ;
		__CPU2_bss_START = .;
        "*(.bss_cpu2)"
        "*(.bss_cpu2.*)"
    } > dsram2
    __CPU2_bss_SIZE = sizeof(.CPU2.bss); 
	
	.CPU2.psram_text  :
    {
        . = ALIGN(2);
        "*(.cpu2_psram)"
    } > psram2
}

SECTIONS
{
   .CPU1.data :
    {
        . = ALIGN(4) ;
        __CPU1_data_START = .;
        "*(.data_cpu1)"
        "*(.data_cpu1.*)"
    } > dsram1
    __CPU1_data_SIZE = sizeof(.CPU1.data);

    .CPU1.bss  (CLEAR) (NOLOAD):
    {
        . = ALIGN(4) ;
        __CPU1_bss_START = .;
        "*(.bss_cpu1)"
        "*(.bss_cpu1.*)"
    } > dsram1
    __CPU1_bss_SIZE = sizeof(.CPU1.bss); 
	
	.CPU1.psram_text  :
    {
        . = ALIGN(2);
        "*(.bss_rbSyslog_NotCpu0)"
    } > psram1
}

SECTIONS
{
    .CPU0.data :
    {
        . = ALIGN(4) ;
        __CPU0_data_START = .;
        "*(.data_cpu0)"
        "*(.data_cpu0.*)"
    } > dsram0
    __CPU0_data_SIZE = sizeof(.CPU0.data);

    .CPU0.bss  (CLEAR) (NOLOAD):
    {	
		. = ALIGN(4) ;
		__CPU0_bss_START = .;
        "*(.bss_cpu0)"
        "*(.bss_cpu0.*)"
    } > dsram0
     __CPU0_bss_SIZE = sizeof(.CPU0.bss); \

    .CPU0.psram_text  :
    {
        . = ALIGN(2);
        "*(.bss_rbSyslog_Cpu0)"
    } > psram0
}





SECTIONS
{
    .dlmu0_nc.data (__dlmu0_nc_START) : 
    { 
        __dlmu0_nc_data_START = .; 
        *(.data_dlmu0_nc) 
        __dlmu0_nc_data_END = .; 
    } > dlmu0_nc 
    __dlmu0_nc_data_SIZE = sizeof(.dlmu0_nc.data); 
    .dlmu0_nc.bss (CLEAR) (NOLOAD) (ADDR(.dlmu0_nc.data) + sizeof(.dlmu0_nc.data)) : 
    { 
        __dlmu0_nc_bss_START = .; 
        *(.bss_dlmu0_nc) 
       __dlmu0_nc_bss_END = .; 
    } > dlmu0_nc 
    __dlmu0_nc_bss_SIZE = sizeof(.dlmu0_nc.bss); 
}

SECTIONS
{
    .dlmu1_nc.data (__dlmu1_nc_START) : 
    { 
        __dlmu1_nc_data_START = .; 
        *(.data_dlmu1_nc) 
       __dlmu1_nc_data_END = .; 
    } > dlmu1_nc 
    __dlmu1_nc_data_SIZE = sizeof(.dlmu1_nc.data); 
    .dlmu1_nc.bss (CLEAR) (NOLOAD) (ADDR(.dlmu1_nc.data) + sizeof(.dlmu1_nc.data)) : 
    { 
        __dlmu1_nc_bss_START = .; 
        *(.bss_dlmu1_nc) 
        __dlmu1_nc_bss_END = .; 
    } > dlmu1_nc 
    __dlmu1_nc_bss_SIZE = sizeof(.dlmu1_nc.bss); 
	
	.contexts  :
    {
    } > dlmu1_nc
}

SECTIONS
{
    .dlmu2_nc.data (__dlmu2_nc_START) : 
    { 
        __dlmu2_nc_data_START = .; 
        *(.data_dlmu2_nc) 
        __dlmu2_nc_data_END = .; 
    } > dlmu2_nc 
    __dlmu2_nc_data_SIZE = sizeof(.dlmu2_nc.data); 
    .dlmu2_nc.bss (CLEAR) (NOLOAD) (ADDR(.dlmu2_nc.data) + sizeof(.dlmu2_nc.data)) : 
    { 
        __dlmu2_nc_bss_START = .; 
        *(.bss_dlmu2_nc) 
        __dlmu2_nc_bss_END = .; 
    } > dlmu2_nc 
    __dlmu2_nc_bss_SIZE = sizeof(.dlmu2_nc.bss); 
}

SECTIONS
{
    .dlmu3_nc.data (__dlmu3_nc_START) : 
    { 
        __dlmu3_nc_data_START = .; 
        *(.data_dlmu3_nc) 
        __dlmu3_nc_data_END = .; 
    } > dlmu3_nc 
    __dlmu3_nc_data_SIZE = sizeof(.dlmu3_nc.data); 
    .dlmu3_nc.bss (CLEAR) (NOLOAD) (ADDR(.dlmu3_nc.data) + sizeof(.dlmu3_nc.data)) : 
    { 
        __dlmu3_nc_bss_START = .; 
        *(.bss_dlmu3_nc) 
        __dlmu3_nc_bss_END = .; 
    } > dlmu3_nc 
    __dlmu3_nc_bss_SIZE = sizeof(.dlmu3_nc.bss); 
}

SECTIONS
{
    .dlmu4_nc.data (__dlmu4_nc_START) : 
    { 
        __dlmu4_nc_data_START = .; 
        *(.data_dlmu4_nc) 
        __dlmu4_nc_data_END = .; 
    } > dlmu4_nc 
    __dlmu4_nc_data_SIZE = sizeof(.dlmu4_nc.data); 
    .dlmu4_nc.bss (CLEAR) (NOLOAD) (ADDR(.dlmu4_nc.data) + sizeof(.dlmu4_nc.data)) : 
    { 
        __dlmu4_nc_bss_START = .; 
        *(.bss_dlmu4_nc) 
        __dlmu4_nc_bss_END = .; 
    } > dlmu4_nc 
    __dlmu4_nc_bss_SIZE = sizeof(.dlmu4_nc.bss); 
}

SECTIONS
{
    .dlmu5_nc.data (__dlmu5_nc_START) : 
    { 
        __dlmu5_nc_data_START = .; 
        *(.data_dlmu5_nc) 
        __dlmu5_nc_data_END = .; 
    } > dlmu5_nc 
    __dlmu5_nc_data_SIZE = sizeof(.dlmu5_nc.data); 
    .dlmu5_nc.bss (CLEAR) (NOLOAD) (ADDR(.dlmu5_nc.data) + sizeof(.dlmu5_nc.data)) : 
    { 
        __dlmu5_nc_bss_START = .; 
        *(.bss_dlmu5_nc) 
        __dlmu5_nc_bss_END = .; 
    } > dlmu5_nc 
    __dlmu5_nc_bss_SIZE = sizeof(.dlmu5_nc.bss); 
}

SECTIONS
{
    .lmu0_nc.data (__lmu0_nc_START) : 
    { 
        __lmu0_nc_data_START = .; 
        *(.data_lmu0_nc) 
        __lmu0_nc_data_END = .; 
    } > lmu0_nc 
    __lmu0_nc_data_SIZE = sizeof(.lmu0_nc.data); 
    .lmu0_nc.bss (CLEAR) (NOLOAD) (ADDR(.lmu0_nc.data) + sizeof(.lmu0_nc.data)) : 
    { 
        __lmu0_nc_bss_START = .; 
        *(.bss_lmu0_nc) 
        __lmu0_nc_bss_END = .; 
    } > lmu0_nc 
    __lmu0_nc_bss_SIZE = sizeof(.lmu0_nc.bss); 
}

SECTIONS
{
    /*.bss (CLEAR) (NOLOAD) :
    {
        . = ALIGN(4) ;
        "*(.bss)"
        "*(.bss.*)"
        
     } > lmu0_nc */

    .heap (NOLOAD) :
    {
        . = ALIGN(4);
        __HEAP = .;
        . += LCF_HEAP_SIZE;
        __HEAP_END = .;
    } > dsram0
}

SECTIONS
{
    /* Initialize data default section .data */
    .default_data :
    {
        __default_data_START = .;
        /* ECU_USED_DATA_SECTION */
        *(.data)
        __default_data_END = .;
     } > dsram1
     __default_data_SIZE = sizeof(.default_data);
     
     /* Initialize data default section .bss */
    .default_bss (CLEAR) (NOLOAD) :
    {
        __default_bss_START = .;
        /* ECU_USED_BSS_SECTION */
        *(.bss)
        *(COMMON)
        *(.tlsbss)
        *(.tls.cond.bss)        
        __default_bss_END = .;
    } > lmu0_nc
    __default_bss_SIZE = sizeof(.default_bss);
    
    /* Initialize data default section .sdata */
    /* we are not using sdata, but some compiler libs need this reference */
    .default_sdata :
    {
        __default_sdata_START = .;
        /* ECU_USED_SDATA_SECTION */
        *(.sdata)
        __default_sdata_END = .;
    } > dsram1
    __default_sdata_SIZE = sizeof(.default_sdata);
    
    /* due to the inclusion or use of some compiler libraries, it is necessary to define some symbols */
    _SMALL_DATA_ = ADDR(.default_sdata) + 0x8000;
    _SMALL_DATA_A8_ = 0;
    _SMALL_DATA_A9_ = 0;
    _LITERAL_DATA_ = 0;
}

SECTIONS
{
    .sdata3 :
    {
        "*(.rodata_a8)"
        "*(.rodata_a8.*)"
    } > Applpfls0

    _SMALL_DATA_A9_ = 0;

    .pfls0end :
    {
        /* end BootROM flash check here */
        /* the end address must be word aligned and is included in the check */
        . = ALIGN(4);
        RBA_SYSPREINIT_CFG_MEMORY_CHECK_END = .;
        /* fill the end address with a dummy word */
        /* LONG(0xDEADBEEF); */
    } > Applpfls0

    /*FLASH */
    /* FLASH      = 0xF8001000;
    FLASH0     = 0xF8001000; */

    /*System Control Unit */
    SCU        = 0xF0036008;

    /*Safety Management Unit */
    SMU        = 0xF0036800;

    /*GPIO Ports*/
    P00        = 0xF003A000;
    P01        = 0xF003A100;
    P02        = 0xF003A200;
    P20        = 0xF003C000;
    P33        = 0xF003D300;
    P34        = 0xF003D400;

    /* FLS */
    DMU         =   0xF8040000;
    PFI0        =   0xA8080000;
    PFI1        =   0xA8380000;
    PFI2        =   0xA8680000;
    PFI3        =   0xA8980000;
    PFI4        =   0xA8C80000;
    PFI5        =   0xA8F80000;
    
    /*SRC */
    SRC        = 0xF0038000;

    /* Queued Synchrounous Peripheral Interface*/
    QSPI       = 0xF0001C00;

    /* system timer */
    STM        = 0xF0000000;
    STM0       = 0xF0000000;
    STM1       = 0xF0000100;
    STM2       = 0xF0000200;

    /*EMEM */
    EMEM       = 0xF90E6000;

}

