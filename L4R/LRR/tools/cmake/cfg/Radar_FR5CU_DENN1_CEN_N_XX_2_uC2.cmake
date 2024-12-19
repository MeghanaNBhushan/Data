set(RB_PROJECT_TARGET_ACTIVATION "Radar_FR5CU_DENN1_CEN_N_XX_2_uC2" CACHE INTERNAL "")
include(${CMAKE_CURRENT_LIST_DIR}/Radar_C0.cmake)
include (${RB_ARCH_BUILD_CFG_DIR}/development_settings.cmake)
include (${CMAKE_CURRENT_LIST_DIR}/uC2_Premium_LayoutLinker.cmake)
set (RB_PROJECT_GLOBAL_DEFINES ${RB_PROJECT_GLOBAL_DEFINES} RBDIA_CFG_DOIP RB_XL_DEVICE_TRANSITION RB_PREMIUM_BX_TO_C0_TRANSITION_UC2 DSP_MT_ENABLED DEVELOPER_MODE_ENABLED Radar_FR5CU_DENN1_CEN_N_XX_2_uC2)
set(RB_PROJECT_EXTERNAL_LINK_LIBS ${RB_PROJECT_EXTERNAL_LINK_LIBS} "${RB_ROOT_DIR}/ip_if/radar_if/component/rtaos/xR5yU_XX_uC2/out/RTAOS.a" CACHE INTERNAL "List of external libraries" )
set(RB_PROJECT_HAWCC_MERGE_HEXFILES "ad_radar_apl/cubas/cfg/EcuCybSec_VMS-2_PJIF/Hsm_XX_PremM/HSM_7_8_R20_VMS_2_0_1__PJIF_XX_PremM__001.hex" "ad_radar_apl/cubas/cfg/EcuCybSec_VMS-2_PJIF/HsmEnabling/UCB-HSM_DbgEnabled_HsmEnabled_09-0D-08-07.hex" CACHE INTERNAL "")
set(RB_PROJECT_SCOM_CONFIG_FILE "${CMAKE_CURRENT_LIST_DIR}/scom_config_uC2.cmake" CACHE INTERNAL "cmake scom config file")
include(${RB_PROJECT_SCOM_CONFIG_FILE})
set(RB_PROJECT_RUN_scom_generator true)

set(RB_PROJECT_SCOM_GENERATOR_OPTIONS 
				-p
				-f "${FLUX_FILE}"
				-i "${SYSTEM_INSTANCE}"
				-o "${OS}"
				-s "${SCOM_PATH}"
				--log "${LOG}"
				--generate_unconnected_mempools 
				--DynAddrSig_static "${DynAddrSig_static}"
				--MempoolOptSize "${MempoolOptSize}"
				--var "${Var}"
				--xml "${RB_PROJECT_SCOM_XML_FILE}"
	)

