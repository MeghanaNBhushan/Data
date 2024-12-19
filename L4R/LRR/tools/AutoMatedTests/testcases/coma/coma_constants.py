# -*- coding: utf-8 -*-

#MCS PDU constants
CONST_NO_SYNCHTYPE                                      = "00"
CONST_TIME_SLOT_SYNCHTYPE                               = "01"
CONST_INTERLEAVED_SYNCHTYPE                             = "02"

CONST_MEAS_PGM_MAX_VALUE_PDU                            = "ffff"

CONST_SENSORTIME_44_MILLI_SECONDS_PDU                   = "029f6300"
CONST_SENSORTIME_22_MILLI_SECONDS_PDU                   = "014fb180"
CONST_SENSORTIME_33_MILLI_SECONDS_PDU                   = "01f78a40"
CONST_SENSORTIME_0_MILLI_SECONDS_PDU                    = "00000000"


CONST_DSP_SENSORTIME_22_MILLI_SECONDS_PDU               = "014fb180"
CONST_DSP_SENSORTIME_11_MILLI_SECONDS_PDU               = "00a7d8c0"
CONST_DSP_SENSORTIME_0_MILLI_SECONDS_PDU                = "00000000"


CONST_EGO_VEHICLE_SPEED_MINVALUE                        = "c2c80000"
CONST_EGO_VEHICLE_SPEED_MAXVALUE                        = "42c80000"
CONST_EGO_VEHICLE_SPEED_MIDVALUE                        = "42480000"
CONST_EGO_VEHICLE_SPEED_BEYONDMINVALUE                  = "c3020000"
CONST_EGO_VEHICLE_SPEED_BEYONDMAXVALUE                  = "43020000"

CONST_DSP_EGO_VEHICLE_SPEED_MINVALUE                    = -25600
CONST_DSP_EGO_VEHICLE_SPEED_MAXVALUE                    = 25600
CONST_DSP_EGO_VEHICLE_SPEED_MIDVALUE                    = 12800
CONST_DSP_EGO_VEHICLE_SPEED_BEYONDMIN                   = -32768
CONST_DSP_EGO_VEHICLE_SPEED_BEYONDMAX                   = 32767

CONST_IHD_EGO_VEHICLE_SPEED_MINVALUE                    = "-100.0"
CONST_IHD_EGO_VEHICLE_SPEED_MAXVALUE                    = "100.0"
CONST_IHD_EGO_VEHICLE_SPEED_MIDVALUE                    = "50.0"
CONST_IHD_EGO_VEHICLE_SPEED_BEYONDMIN                   = "-110.0"
CONST_IHD_EGO_VEHICLE_SPEED_BEYONDMAX                   = "110.0"

CONST_EGO_VEHICLE_SPEED_DEV_MINVALUE                    = "c3000000"
CONST_EGO_VEHICLE_SPEED_DEV_MAXVALUE                    = "42fffae1"
CONST_EGO_VEHICLE_SPEED_DEV_MIDVALUE                    = "428c0000"
CONST_EGO_VEHICLE_SPEED_DEV_BEYONDMINVALUE              = "c3020000"
CONST_EGO_VEHICLE_SPEED_DEV_BEYONDMAXVALUE              = "43020000"

CONST_DSP_EGO_VEHICLE_SPEED_DEV_MINVALUE                = -32768
CONST_DSP_EGO_VEHICLE_SPEED_DEV_MAXVALUE                = 32765
CONST_DSP_EGO_VEHICLE_SPEED_DEV_MIDVALUE                = 17920
CONST_DSP_EGO_VEHICLE_SPEED_DEV_BEYONDMIN               = -32768
CONST_DSP_EGO_VEHICLE_SPEED_DEV_BEYONDMAX               = 32767

CONST_IHD_EGO_VEHICLE_SPEED_DEV_MINVALUE                = "-128.0"
CONST_IHD_EGO_VEHICLE_SPEED_DEV_MAXVALUE                = "127.99"
CONST_IHD_EGO_VEHICLE_SPEED_DEV_MIDVALUE                = "70.0"
CONST_IHD_EGO_VEHICLE_SPEED_DEV_BEYONDMIN               = "-130.0"
CONST_IHD_EGO_VEHICLE_SPEED_DEV_BEYONDMAX               = "130.0"

CONST_EGO_VEHICLE_YAW_RATE_MINVALUE                     = "c2e52e14"
CONST_EGO_VEHICLE_YAW_RATE_MAXVALUE                     = "42e52e14"
CONST_EGO_VEHICLE_YAW_RATE_MIDVALUE                     = "42c80000"
CONST_EGO_VEHICLE_YAW_RATE_BEYONDMINVALUE               = "c2f00000"
CONST_EGO_VEHICLE_YAW_RATE_BEYONDMAXVALUE               = "42f00000"

CONST_DSP_EGO_VEHICLE_YAW_RATE_MINVALUE                 = -32767
CONST_DSP_EGO_VEHICLE_YAW_RATE_MAXVALUE                 = 32767
CONST_DSP_EGO_VEHICLE_YAW_RATE_MIDVALUE                 = 28595
CONST_DSP_EGO_VEHICLE_YAW_RATE_BEYONDMIN                = -32768
CONST_DSP_EGO_VEHICLE_YAW_RATE_BEYONDMAX                = 32767

CONST_IHD_EGO_VEHICLE_YAW_RATE_MINVALUE                 = "-114.59"
CONST_IHD_EGO_VEHICLE_YAW_RATE_MAXVALUE                 = "114.59"
CONST_IHD_EGO_VEHICLE_YAW_RATE_MIDVALUE                 = "100.0"
CONST_IHD_EGO_VEHICLE_YAW_RATE_BEYONDMIN                = "-120.0"
CONST_IHD_EGO_VEHICLE_YAW_RATE_BEYONDMAX                = "120.0"

CONST_EGO_VEHICLE_ACCEL_MINVALUE                        = "c1800000"
CONST_EGO_VEHICLE_ACCEL_MAXVALUE                        = "417fd70a"
CONST_EGO_VEHICLE_ACCEL_MIDVALUE                        = "41200000"
CONST_EGO_VEHICLE_ACCEL_BEYONDMINVALUE                  = "c1a00000"
CONST_EGO_VEHICLE_ACCEL_BEYONDMAXVALUE                  = "41a00000"

CONST_DSP_EGO_VEHICLE_ACCEL_MINVALUE                    = -32768
CONST_DSP_EGO_VEHICLE_ACCEL_MAXVALUE                    = 32747
CONST_DSP_EGO_VEHICLE_ACCEL_MIDVALUE                    = 20480
CONST_DSP_EGO_VEHICLE_ACCEL_BEYONDMIN                   = -32768
CONST_DSP_EGO_VEHICLE_ACCEL_BEYONDMAX                   = 32767

CONST_IHD_EGO_VEHICLE_ACCEL_MINVALUE                    = "-16.0"
CONST_IHD_EGO_VEHICLE_ACCEL_MAXVALUE                    = "15.99"
CONST_IHD_EGO_VEHICLE_ACCEL_MIDVALUE                    = "10.0"
CONST_IHD_EGO_VEHICLE_ACCEL_BEYONDMIN                   = "-20.0"
CONST_IHD_EGO_VEHICLE_ACCEL_BEYONDMAX                   = "20.0"

#Constants for systme variable for TX PDUs 
CONST_INVALID_ENUM                                      = -3
CONST_CLEAR_ENUM                                        = -2
CONST_READY_TO_READDATA_ENUM                            = -1
CONST_LOCATION_ATTRIBUTE_ENUM                           = 0
CONST_LOCATION_DATA0_ENUM                               = 1
CONST_SENSORSTATE_ENUM                                  = 2
CONST_SENSORFEEDBACK_ENUM                               = 3
CONST_SENSORBROADCAST_ENUM                              = 4

#Location data and Attribute, Sensor state, Sensor feedback PDU common Constants
CONST_DEFAULT_SOURCE_IP_ADDRESS                         = '0xc0a82833'
CONST_DEFAULT_SOURCE_MAC_ADDRESS                        = '0x8834fe000001'
CONST_DEFAULT_SOURCE_PORT_NUMBER                        = '0x76c6'
CONST_DEFAULT_DEST_IP_ADDRESS                           = '0xc0a82802'
CONST_DEFAULT_DEST_MAC_ADDRESS                          = '0x284cf3bbe10'
CONST_DEFAULT_DEST_PORT_NUMBER                          = '0x76c0'

#Location attribute PDU Constants
CONST_LOCATION_ATTRIBUTE_PDU_ID                         = '0x133bddcf'
CONST_LOCATION_ATTRIBUTE_PDU_LEN                        = 514
CONST_LOCATION_ATTRIBUTE_CYCLETIME_MIN                  = 60
CONST_LOCATION_ATTRIBUTE_CYCLETIME_MAX                  = 70

#Location Data_0 PDU Constants
CONST_LOCATION_DATA0_PDU_ID                             = '0x13370001'
CONST_LOCATION_DATA0_PDU_LEN                            = 1190
CONST_LOCATION_DATA0_CYCLETIME_MIN                      = 60
CONST_LOCATION_DATA0_CYCLETIME_MAX                      = 70

#SensorFeedback PDU Constants
CONST_SENSORFEEDBACK_PDU_ID                             = '0x133addcf'
CONST_SENSORFEEDBACK_PDU_LEN                            = 100
CONST_SENSORFEEDBACK_CYCLETIME_MIN                      = 45
CONST_SENSORFEEDBACK_CYCLETIME_MAX                      = 55
CONST_SENSORFEEDBACK_EGOVEH_YAW_RATE1                   = 100
CONST_SENSORFEEDBACK_EGOVEH_SPEED1                      = 50
CONST_SENSORFEEDBACK_EGOVEH_SPEED_DEV1                  = 50
CONST_SENSORFEEDBACK_EGOVEH_ACCEL1                      = 10
CONST_SENSORFEEDBACK_EGOVEH_YAW_RATE2                   = 114
CONST_SENSORFEEDBACK_EGOVEH_SPEED2                      = 20
CONST_SENSORFEEDBACK_EGOVEH_SPEED_DEV2                  = 20
CONST_SENSORFEEDBACK_EGOVEH_ACCEL2                      = 5
CONST_FLOATING_POINT_ABS_COMPARE                        = 1

#PTP STBM Time Syn
CONST_STBM_ON                                           = '08'
CONST_STBM_OFF                                          = '09'
CONST_STBM_LEAPPAST                                     = '28'
CONST_STBM_LEAPFUTURE                                   = '18'
CONST_STBM_GLOBAL_TIME_ZERO                             = '00'

#E2E Constants
CONST_LOC_ATTR_E2E_LENGTH                               = 514
CONST_LOC_DATA_E2E_LENGTH								= 1190
CONST_SENSOR_STATE_E2E_LENGTH                           = 64
CONST_SENSOR_FEEDBACK_E2E_LENGTH                        = 100

CONST_LOC_ATTR_E2E_DATAID			    			    = 322690511
CONST_LOC_DATA_E2E_DATAID                               = 322371585
CONST_SENSOR_STATE_E2E_DATAID                           = 322493903
CONST_SENSOR_FEEDBACK_E2E_DATAID                        = 322624975

#SensorState PDU Constants
CONST_SENSORSTATE_PDU_ID                                = '0x1338ddcf'
CONST_SENSORSTATE_PDU_LEN                               = 64
CONST_SENSORSTATE_CYCLETIME_MIN                         = 8
CONST_SENSORSTATE_CYCLETIME_MAX                         = 12
CONST_SENSORSTATE_UNASSIGNED1                           = ('0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff')
CONST_SENSORSTATE_UNASSIGNED                            = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                                 
#SensorBroadcast PDU Constants
CONST_SENSORBORADCAST_CYCLETIME_MAX                    = 1005
CONST_SENSORBORADCAST_CYCLETIME_MIN                    = 995
CONST_BROADCAST_SOURCE_PORT_NUMBER                     = '0x7600'    
CONST_BROADCAST_DEST_IP_ADDRESS                        = '0xffffffff'
CONST_BROADCAST_DEST_MAC_ADDRESS                       = '0xffffffffffff' 
CONST_SENSORBORADCAST_PDU_ID                           = '0x133cddcf' 
CONST_BROADCAST_SouPort                                = '0x76c6'
CONST_SENSORBORADCAST_PDU_LEN                          = 160
CONST_BROADCAST_SenIpAdd                               = 3232245811                
CONST_BROADCAST_DestIpAdd                              = 3232245762               
CONST_BROADCAST_DiagSouIpAdd                           = 2852000405        
CONST_BROADCAST_DiagNetmask                            = 4294901760
CONST_BROADCAST_SenNetmask                             = '0xffff0000' 
CONST_BROADCAST_SenVlan                                = 65535
CONST_BROADCAST_DiagVlan                               = 1
CONST_BROADCAST_DestPortUnassigned                     = 0.0000
CONST_BROADCAST_DestPort                               = "0x76c0"      
CONST_BROADCAST_DoIPTarAdd                             = '0xef8'  
CONST_BROADCAST_SenDoIPFuncAdd                         = 65535 
CONST_BROADCAST_SenDoIPPhyAdd                          = 4757
CONST_BROADCAST_SenMacAdd                              = 149761181089793 
CONST_BROADCAST_DiagPort                               = 13400   
CONST_BROADCAST_Unassigned                             = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
CONST_BROADCAST_SenNetmask                             = 4294901760
CONST_BROADCAST_SouPortUnassigned                      = 0.0000
CONST_BROADCAST_SENSOR_NETMASK_SET1                    = 4278190080
CONST_BROADCAST_SENSOR_NETMASK_SET2                    = 4293918720
CONST_USERDEFINED_RADAR_IP_RANGE_1                     = 167772161
CONST_USERDEFINED_REMOTE_IP_RANGE_1                    = 184549374
CONST_USER_DEFINED_REMOTE_PORT_SET1                    = "0x8756"
CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET1         = 2851995649
CONST_USERDEFINED_MAC_SET1                             = 149761189810469
CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET1             = 1
CONST_USERDEFINED_RADAR_IP_RANGE_2                     = 2886729729                     
CONST_USERDEFINED_REMOTE_IP_RANGE_2                    = 2887778302
CONST_USER_DEFINED_REMOTE_PORT_SET2                    = "0x9645"
CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET2         = 2852061182
CONST_USERDEFINED_MAC_SET2                             = 149761185637272
CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET2             = 65535
