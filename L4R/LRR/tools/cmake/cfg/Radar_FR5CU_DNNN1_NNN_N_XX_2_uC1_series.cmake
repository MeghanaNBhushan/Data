set(RB_PROJECT_TARGET_ACTIVATION "Radar_FR5CU_DNNN1_NNN_N_XX_2_uC1_series" CACHE INTERNAL "")
include(${CMAKE_CURRENT_LIST_DIR}/Radar_C0.cmake)
include (${CMAKE_CURRENT_LIST_DIR}/uC1_XL_Premium_LayoutLinker.cmake)
set (RB_PROJECT_GLOBAL_DEFINES ${RB_PROJECT_GLOBAL_DEFINES} RBDIA_CFG_DOIP RB_XL_DEVICE_TRANSITION RB_PREMIUM_BX_TO_C0_TRANSITION_UC1 DSP_MT_ENABLED SERIES_MODE_ENABLED Radar_FR5CU_DNNN1_NNN_N_XX_2_uC1)
set(RB_PROJECT_EXTERNAL_LINK_LIBS ${RB_PROJECT_EXTERNAL_LINK_LIBS} "${RB_ROOT_DIR}/ip_if/radar_if/component/rtaos/xR5yU_XX_uC1/out/RTAOS.a" CACHE INTERNAL "List of external libraries" )
set(RB_PROJECT_HAWCC_MERGE_HEXFILES "ad_radar_apl/cubas/cfg/EcuCybSec_VMS-2_PJIF/Hsm_LX_PremS/HSM_7_6_R1_VMS_2_0_1__PJIF_LX_PremS__001.hex" "ad_radar_apl/cubas/cfg/EcuCybSec_VMS-2_PJIF/HsmEnabling/UCB-HSM_DbgEnabled_HsmEnabled_09-0D-08-07.hex" CACHE INTERNAL "")
