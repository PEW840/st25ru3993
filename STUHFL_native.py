#******************************************************************************
#  * \attention
#  *
#  * <h2><center>&copy; COPYRIGHT(c) 2021 STMicroelectronics</center></h2>
#  *
#  * Licensed under ST MYLIBERTY SOFTWARE LICENSE AGREEMENT (the "License");
#  * You may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at:
#  *
#  *        www.st.com/myliberty
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
#  * AND SPECIFICALLY DISCLAIMING THE IMPLIED WARRANTIES OF MERCHANTABILITY,
#  * FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  *
#******************************************************************************

import os
import sys

import ctypes
from ctypes import *

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
lib = None
#libPath = "Release\\x86\\STUHFL.dll"        # 32 bits/Release
#libPath = "Debug\\x86\\STUHFL.dll"          # 32 bits/Debug
#libPath = "Release\\x64\\STUHFL.dll"        # 64 bits/Release
libPath = "Debug\\x64\\STUHFL.dll"          # 64 bits/Debug


# - Defines -----------------------------------------------------------------
STUHFL_D_MAX_VERSION_INFO_LENGTH = 64
MAX_REGISTERS = 64
#
STUHFL_D_MAX_TAG_LIST_SIZE = 64
#
STUHFL_D_MAX_EPC_LENGTH = 64
STUHFL_D_MAX_XPC_LENGTH = 4
STUHFL_D_MAX_TID_LENGTH = 12
STUHFL_D_MAX_PC_LENGTH = 2
STUHFL_D_GEN2_MAXQ = 15
STUHFL_D_MAX_FREQUENCY = 53
STUHFL_D_NB_C_VALUES = 16
STUHFL_D_MAX_ANTENNA = 4
#
STUHFL_D_PASSWORD_LEN = 4
STUHFL_D_MAX_READ_DATA_LEN = 64
STUHFL_D_MAX_WRITE_DATA_LEN = 2
STUHFL_D_MAX_BLOCKWRITE_DATA_LEN = 16
#
STUHFL_D_GEN2_MAX_SELECT_MASK_LENGTH = 32
STUHFL_D_GEN2_LOCK_MASK_ACTION_LEN = 3
STUHFL_D_GEN2_GENERIC_CMD_MAX_SND_DATA_BYTES = 64   #(512 / 8)
STUHFL_D_GEN2_GENERIC_CMD_MAX_RCV_DATA_BYTES = 128
#
STUHFL_D_GB29768_MAX_SORT_MASK_LENGTH = 32
#
STUHFL_D_INVENTORYREPORT_HEARTBEAT_DURATION_MS = 400
#
STUHFL_D_RESET_DEFAULT_ALL_FREQS = 0
STUHFL_D_FREQUENCY_MAX_VALUE = 999000
STUHFL_D_DEFAULT_FREQUENCY = 865700
#
STUHFL_D_GEN2_TIMING_USE_DEFAULT_T4MIN = 0
#
STUHFL_D_LOG_LEVEL_COUNT = 10

STUHFL_ERR_DLL = 0x10000000
STUHFL_ERR_NONE = 0

# ---------------------------------------------------------------------------
# General 
# ---------------------------------------------------------------------------
# region General
class STUHFL_T_Version(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("major", ctypes.c_uint8),
                ("minor", ctypes.c_uint8),
                ("micro", ctypes.c_uint8),
                ("nano" , ctypes.c_uint8)]

class STUHFL_T_VersionInfo(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("info", ctypes.c_char * STUHFL_D_MAX_VERSION_INFO_LENGTH),  
                ("infoLength", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_Register(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("addr", ctypes.c_uint8),  
                ("data", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_RwdConfig(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("id", ctypes.c_uint8),  
                ("value", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_RxFilter(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("blf", ctypes.c_uint8),
                ("coding", ctypes.c_uint8),        
                ("value", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_FilterCalibration(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("blf", ctypes.c_uint8),
                ("coding", ctypes.c_uint8),        
                ("highPass", ctypes.c_uint8),
                ("lowPass", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_AntennaPower(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("mode", ctypes.c_uint8),
                ("timeout", ctypes.c_uint16),        
                ("frequency", ctypes.c_uint32)]
# endregion General

# ---------------------------------------------------------------------------
# Configuration 
# ---------------------------------------------------------------------------
# region Configuration
class STUHFL_T_ST25RU3993_FreqRssi(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("frequency", ctypes.c_uint32),
                ("rssiLogI", ctypes.c_uint8),
                ("rssiLogQ", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_FreqReflectedPowerInfo(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("frequency", ctypes.c_uint32),
                ("applyTunerSetting", ctypes.c_bool),
                ("reflectedI", ctypes.c_int8),
                ("reflectedQ", ctypes.c_int8)]

class STUHFL_T_ST25RU3993_Caps(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("cin", ctypes.c_uint8),
	            ("clen", ctypes.c_uint8),
	            ("cout", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_ChannelItem(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("frequency", ctypes.c_uint32),
	            ("caps", STUHFL_T_ST25RU3993_Caps),
	            ("rfu1", ctypes.c_uint8),
                ("rfu2", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_ChannelList(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("antenna", ctypes.c_uint8),
             ("persistent", ctypes.c_bool),
             ("numFrequencies", ctypes.c_uint8),
             ("channelListIdx", ctypes.c_uint8),
             ("itemList", STUHFL_T_ST25RU3993_ChannelItem * STUHFL_D_MAX_FREQUENCY)]

class STUHFL_T_ST25RU3993_FreqHop(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("maxSendingTime", ctypes.c_uint16),
             ("minSendingTime", ctypes.c_uint16),
             ("mode", ctypes.c_uint8),
             ("rfu", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_FreqLBT(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("listeningTime", ctypes.c_uint16),
                ("idleTime", ctypes.c_uint16),
                ("rssiLogThreshold", ctypes.c_uint8),
                ("skipLBTcheck", ctypes.c_bool)]

class STUHFL_T_ST25RU3993_FreqContinuousModulation(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("frequency", ctypes.c_uint32),
                ("enable", ctypes.c_bool),
                ("maxSendingTime", ctypes.c_uint16),
                ("mode", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_Gen2_Timings(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("T4Min", ctypes.c_uint16)]

class STUHFL_T_ST25RU3993_Gen2_ProtocolCfg(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("tari", ctypes.c_uint8),
                ("blf", ctypes.c_uint8),
                ("coding", ctypes.c_uint8),
                ("trext", ctypes.c_bool)]

class STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("trext", ctypes.c_bool),
                ("blf", ctypes.c_uint8),
                ("coding", ctypes.c_uint8),
                ("tc", ctypes.c_uint8)] 

class STUHFL_T_ST25RU3993_TxRxCfg(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("txOutputLevel", ctypes.c_int8),
                ("rxSensitivity", ctypes.c_int8),
                ("usedAntenna", ctypes.c_uint8),
                ("alternateAntennaInterval", ctypes.c_uint16),
                ("rfu", ctypes.c_uint8)] 

class STUHFL_T_ST25RU3993_PowerAmplifierCfg(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("external", ctypes.c_bool)]

class STUHFL_T_ST25RU3993_AutoTuning(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("interval", ctypes.c_uint16),
                ("level", ctypes.c_uint8),
                ("algorithm", ctypes.c_uint8),
                ("falsePositiveDetection", ctypes.c_bool)]

class STUHFL_T_ST25RU3993_AdaptiveSensitivity(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("interval", ctypes.c_uint16),
                ("enable", ctypes.c_uint8)]

class STUHFL_T_ST25RU3993_Gen2_InventoryOption(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("fast", ctypes.c_bool),
                ("autoAck", ctypes.c_bool),
                ("readTID", ctypes.c_bool)]

class STUHFL_T_ST25RU3993_Gen2_Anticollision(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("adaptiveQ", ctypes.c_bool),
                ("startQ", ctypes.c_uint8),
                ("minQ", ctypes.c_uint8),
                ("maxQ", ctypes.c_uint8),
                ("options", ctypes.c_uint8),
                ("C1", ctypes.c_uint8 * STUHFL_D_NB_C_VALUES),
                ("C2", ctypes.c_uint8 * STUHFL_D_NB_C_VALUES)]

class STUHFL_T_ST25RU3993_Gen2_QueryParams(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("sel", ctypes.c_uint8),
                ("session", ctypes.c_uint8),
                ("target", ctypes.c_uint8),
                ("toggleTarget", ctypes.c_bool),
                ("targetDepletionMode", ctypes.c_bool)]

class STUHFL_T_ST25RU3993_Gen2_InventoryCfg(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("inventoryOption", STUHFL_T_ST25RU3993_Gen2_InventoryOption),
                ("antiCollision", STUHFL_T_ST25RU3993_Gen2_Anticollision),
                ("autoTuning", STUHFL_T_ST25RU3993_AutoTuning),
                ("queryParams", STUHFL_T_ST25RU3993_Gen2_QueryParams),
                ("adaptiveSensitivity", STUHFL_T_ST25RU3993_AdaptiveSensitivity)]

class STUHFL_T_ST25RU3993_Gb29768_QueryParams(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("condition", ctypes.c_uint8),
                ("session", ctypes.c_uint8),
                ("target", ctypes.c_uint8),
                ("toggleTarget", ctypes.c_bool),
                ("targetDepletionMode", ctypes.c_bool)]

class STUHFL_T_ST25RU3993_Gb29768_Anticollision(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("endThreshold", ctypes.c_uint16),
                ("ccnThreshold", ctypes.c_uint16),
                ("cinThreshold", ctypes.c_uint16)]

class STUHFL_T_ST25RU3993_Gb29768_InventoryOption(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("readTID", ctypes.c_bool)]
    
class STUHFL_T_ST25RU3993_Gb29768_InventoryCfg(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("autoTuning", STUHFL_T_ST25RU3993_AutoTuning),
                ("adaptiveSensitivity", STUHFL_T_ST25RU3993_AdaptiveSensitivity),
                ("queryParams", STUHFL_T_ST25RU3993_Gb29768_QueryParams),
                ("antiCollision", STUHFL_T_ST25RU3993_Gb29768_Anticollision),
                ("inventoryOption", STUHFL_T_ST25RU3993_Gb29768_InventoryOption)]

# endregion Configuration

# ---------------------------------------------------------------------------
# Tuning 
# ---------------------------------------------------------------------------
#region Tuning
class STUHFL_T_ST25RU3993_TuningCaps(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("antenna", ctypes.c_uint8),
                ("channelListIdx", ctypes.c_uint8),
                ("caps", STUHFL_T_ST25RU3993_Caps)]

class STUHFL_T_ST25RU3993_TuneCfg(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("falsePositiveDetection", ctypes.c_bool),
                ("persistent", ctypes.c_bool),
                ("channelListIdx", ctypes.c_uint8),
                ("antenna", ctypes.c_uint8),
                ("algorithm", ctypes.c_uint8),
                ("tuneAll", ctypes.c_bool)]
#endregion Tuning

# ---------------------------------------------------------------------------
# Gen2 
# ---------------------------------------------------------------------------
# region Gen2
class STUHFL_T_Gen2_Select(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("mode", ctypes.c_uint8),
                ("target", ctypes.c_uint8),
                ("action", ctypes.c_uint8),
                ("memoryBank", ctypes.c_uint8),
                ("mask", ctypes.c_uint8 * STUHFL_D_GEN2_MAX_SELECT_MASK_LENGTH),
                ("maskBitPointer", ctypes.c_uint32),
                ("maskBitLength", ctypes.c_uint8),
                ("truncation", ctypes.c_uint8)]

class STUHFL_T_Read(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("wordPtr", ctypes.c_uint32),
                ("memoryBank", ctypes.c_uint8),
                ("numBytesToRead", ctypes.c_uint8),
                ("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN),
                ("numReadBytes", ctypes.c_uint8),
                ("data", ctypes.c_uint8 * STUHFL_D_MAX_READ_DATA_LEN)]

class STUHFL_T_Write(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("wordPtr", ctypes.c_uint32),
                ("memoryBank", ctypes.c_uint8),
                ("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN),
                ("data", ctypes.c_uint8 * STUHFL_D_MAX_WRITE_DATA_LEN),
                ("tagReply", ctypes.c_uint8)]

class STUHFL_T_Gen2_BlockWrite(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("wordPtr", ctypes.c_uint32),
                ("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN),
                ("memoryBank", ctypes.c_uint8),
                ("numBytesToWrite", ctypes.c_uint8),
                ("data", ctypes.c_uint8 * STUHFL_D_MAX_BLOCKWRITE_DATA_LEN),
                ("tagReply", ctypes.c_uint8)]

class STUHFL_T_Gen2_Lock(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("mask", ctypes.c_uint8 * STUHFL_D_GEN2_LOCK_MASK_ACTION_LEN),
                ("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN),
                ("tagReply", ctypes.c_uint8)]

class STUHFL_T_Kill(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN),
                ("recommission", ctypes.c_uint8),
                ("tagReply", ctypes.c_uint8)]

class STUHFL_T_Gen2_GenericCmd(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN),
                ("cmd", ctypes.c_uint8),
                ("noResponseTime", ctypes.c_uint8),
                ("expectedRcvDataBitLength", ctypes.c_uint16),
                ("sndDataBitLength", ctypes.c_uint16),
                ("appendRN16", ctypes.c_bool),
                ("sndData", ctypes.c_uint8 * STUHFL_D_GEN2_GENERIC_CMD_MAX_SND_DATA_BYTES),
                ("rcvDataLength", ctypes.c_uint16),
                ("rcvData", ctypes.c_uint8 * STUHFL_D_GEN2_GENERIC_CMD_MAX_RCV_DATA_BYTES)]

class STUHFL_T_Gen2_QueryMeasureRssi(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("frequency", ctypes.c_uint32),
                ("measureCnt", ctypes.c_uint8),
                ("agc", ctypes.c_uint8 * 256),
                ("rssiLogI", ctypes.c_uint8 * 256),
                ("rssiLogQ", ctypes.c_uint8 * 256),
                ("rssiLinI", ctypes.c_int8 * 256),
                ("rssiLinQ", ctypes.c_int8 * 256)]

# GB/T29768 ##################################################################
class STUHFL_T_Gb29768_Sort(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("mode", ctypes.c_uint8),
                ("target", ctypes.c_uint8),
                ("rule", ctypes.c_uint8),
                ("memoryBank", ctypes.c_uint8),
                ("mask", ctypes.c_uint8 * STUHFL_D_GB29768_MAX_SORT_MASK_LENGTH),
                ("maskBitPointer", ctypes.c_uint32),
                ("maskBitLength", ctypes.c_uint8)]

class STUHFL_T_Gb29768_Lock(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("memoryBank", ctypes.c_uint8),
                ("configuration", ctypes.c_uint8),
                ("action", ctypes.c_uint8),
                ("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN)]

class STUHFL_T_Gb29768_Erase(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("memoryBank", ctypes.c_uint8),
                ("numBytesToErase", ctypes.c_uint8),
                ("bytePtr", ctypes.c_uint32),
                ("pwd", ctypes.c_uint8 * STUHFL_D_PASSWORD_LEN)]



# ---------------------------------------------------------------------------
# Inventory 
# ---------------------------------------------------------------------------
class STUHFL_T_InventoryOption(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("rssiMode", ctypes.c_uint8),
                ("roundCnt", ctypes.c_uint32),
                ("inventoryDelay", ctypes.c_uint16),
                ("options", ctypes.c_uint8)]

class STUHFL_T_InventoryTagXPC(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("length", ctypes.c_uint8),
                ("data", ctypes.c_uint8 * STUHFL_D_MAX_XPC_LENGTH)]

class STUHFL_T_InventoryTagEPC(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("length", ctypes.c_uint8),
                ("data", ctypes.c_uint8 * STUHFL_D_MAX_EPC_LENGTH)]

class STUHFL_T_InventoryTagTID(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("length", ctypes.c_uint8),
                ("data", ctypes.c_uint8 * STUHFL_D_MAX_TID_LENGTH)]

class STUHFL_T_InventoryTag(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("timestamp", ctypes.c_uint32),
                ("antenna", ctypes.c_uint8),
                ("agc", ctypes.c_uint8),
                ("rssiLogI", ctypes.c_uint8),
                ("rssiLogQ", ctypes.c_uint8),
                ("rssiLinI", ctypes.c_int8),
                ("rssiLinQ", ctypes.c_int8),
                ("pc", ctypes.c_uint8 * STUHFL_D_MAX_PC_LENGTH),
                ("xpc", STUHFL_T_InventoryTagXPC),
                ("epc", STUHFL_T_InventoryTagEPC),
                ("tid", STUHFL_T_InventoryTagTID)]

class STUHFL_T_InventoryStatistics(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("timestamp", ctypes.c_uint32),
                ("roundCnt", ctypes.c_uint32),
                ("tuningStatus", ctypes.c_uint8),
                ("rssiLogMean", ctypes.c_uint8),
                ("sensitivity", ctypes.c_int8),
                ("Q", ctypes.c_uint8),
                ("frequency", ctypes.c_uint32),
                ("adc", ctypes.c_uint16),
                ("tagCnt", ctypes.c_uint32),
                ("emptySlotCnt", ctypes.c_uint32),
                ("collisionCnt", ctypes.c_uint32),
                ("skipCnt", ctypes.c_uint32),
                ("preambleErrCnt", ctypes.c_uint32),
                ("crcErrCnt", ctypes.c_uint32),
                ("headerErrCnt", ctypes.c_uint32),
                ("rxCountErrCnt", ctypes.c_uint32)]

class STUHFL_T_InventoryData(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("statistics", STUHFL_T_InventoryStatistics),
                ("tagList", ctypes.POINTER(STUHFL_T_InventoryTag)),
                ("tagListSize", ctypes.c_uint16),
                ("tagListSizeMax", ctypes.c_uint16)]


# ---------------------------------------------------------------------------
# Logging 
# ---------------------------------------------------------------------------

class STUHFL_T_LogOption(ctypes.Structure):
	_pack_ = 1
	_fields_ = [("generateLogTimestamp", ctypes.c_bool),
                ("logLevels", ctypes.c_uint32),
                ("logBuf", ctypes.c_char * STUHFL_D_LOG_LEVEL_COUNT * 1024),
                ("logBufSize", ctypes.c_uint16  * STUHFL_D_LOG_LEVEL_COUNT )]
                














# ---------------------------------------------------------------------------
# Functions 
# ---------------------------------------------------------------------------


def loadSTUHFL_DLL():
    # Checks DLL exists and is reachable
    for path in os.environ["PATH"].split(";"):
        if os.path.isfile(path + "\\" + libPath):
            return cdll.LoadLibrary(libPath)

    print("""
***************************** CAUTION *****************************************
Cannot open STUHFL DLL:
{}

Please ensure STUHFL DLL has been generated before using STUHFL Python wrapper
*******************************************************************************
""".format(libPath))
    sys.exit()
    return None

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Connect(char *szComPort);
def Connect(comPort):
    global lib
    lib = loadSTUHFL_DLL()
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        retCode = lib.Connect(comPort)
        if retCode != STUHFL_ERR_NONE:
            del lib
            lib = None
    else:
        print("DLL connection error..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Disconnect(void);
def Disconnect():
    global lib
    retCode = STUHFL_ERR_NONE
    if lib is not None:
        retCode = lib.Disconnect()
        del lib
        lib = None
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API void CALL_CONV Reboot(void);
def Reboot():
    if lib is not None:
        lib.Reboot()

## Maps from STUHFL.dll to STUHFL_DLL_API void CALL_CONV EnterBootloader(void);
def EnterBootloader():
    if lib is not None:
        lib.EnterBootloader()

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_VERSION CALL_CONV STUHFL_F_GetLibVersion(void);
def GetLibVersion():
    global lib
    old_lib = lib
    if old_lib is None:
        lib = loadSTUHFL_DLL()
    if lib is not None:
        GetLibVersionFunc = lib.STUHFL_F_GetLibVersion
        GetLibVersionFunc.restype = ctypes.c_uint32
        return GetLibVersionFunc()
    else:
        print("not connected..")
    if old_lib is None:
        del lib
        lib = None                          # Reset library, Connect() is to be done
    return STUHFL_ERR_NONE

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_BoardVersion(STUHFL_T_Version *swVersion, STUHFL_T_Version *hwVersion);
def Get_BoardVersion(_nativeSwVer, _nativeHwVer):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_BoardVersionFunc = lib.Get_BoardVersion
        Get_BoardVersionFunc.argtypes = [POINTER(STUHFL_T_Version), POINTER(STUHFL_T_Version)]
        Get_BoardVersionFunc.restype = ctypes.c_uint32
        retCode = Get_BoardVersionFunc(_nativeSwVer, _nativeHwVer)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_BoardInfo(STUHFL_T_VersionInfo *swInfo, STUHFL_T_VersionInfo *hwInfo);
def Get_BoardInfo(_swVersionInfo, _hwVersionInfo):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_BoardInfoFunc = lib.Get_BoardInfo
        Get_BoardInfoFunc.argtypes = [POINTER(STUHFL_T_VersionInfo), POINTER(STUHFL_T_VersionInfo)]
        Get_BoardInfoFunc.restype = ctypes.c_uint32
        retCode = Get_BoardInfoFunc(_swVersionInfo, _hwVersionInfo)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Register(STUHFL_T_ST25RU3993_Register *reg);
def Set_Register(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_RegisterFunc = lib.Set_Register
        Set_RegisterFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Register)]
        Set_RegisterFunc.restype = ctypes.c_uint32
        retCode = Set_RegisterFunc(_native)
    else:
        print("not connected..")
    return retCode    

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Register(STUHFL_T_ST25RU3993_Register *reg);
def Get_Register(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_RegisterFunc = lib.Get_Register
        Get_RegisterFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Register)]
        Get_RegisterFunc.restype = ctypes.c_uint32
        retCode = Get_RegisterFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_RegisterMultiple(STUHFL_T_ST25RU3993_Register **reg, uint8_t numReg);
def Set_RegisterMultiple(_native, lg):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_RegisterMultipleFunc = lib.Set_RegisterMultiple
        Set_RegisterMultipleFunc.argtypes = [POINTER(POINTER(STUHFL_T_ST25RU3993_Register)), ctypes.c_uint8]
        Set_RegisterMultipleFunc.restype = ctypes.c_uint32
        retCode = Set_RegisterMultipleFunc(_native, lg)
    else:
        print("not connected..")
    return retCode 

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_RegisterMultiple(uint8_t numReg, STUHFL_T_ST25RU3993_Register **reg);
def Get_RegisterMultiple(lg, _native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_RegisterMultipleFunc = lib.Get_RegisterMultiple
        Get_RegisterMultipleFunc.argtypes = [ctypes.c_uint8, POINTER(POINTER(STUHFL_T_ST25RU3993_Register))]
        Get_RegisterMultipleFunc.restype = ctypes.c_uint32
        retCode = Get_RegisterMultipleFunc(lg, _native)            
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_RwdCfg(STUHFL_T_ST25RU3993_RwdConfig *rwdCfg);
def Set_RwdCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_RwdCfgFunc = lib.Set_RwdCfg
        Set_RwdCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_RwdConfig)]
        Set_RwdCfgFunc.restype = ctypes.c_uint32
        retCode = Set_RwdCfgFunc(_native)
    else:
        print("not connected..")
    return retCode    

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_RwdCfg(STUHFL_T_ST25RU3993_RwdConfig *rwdCfg);
def Get_RwdCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_RwdCfgFunc = lib.Get_RwdCfg
        Get_RwdCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_RwdConfig)]
        Get_RwdCfgFunc.restype = ctypes.c_uint32
        retCode = Get_RwdCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
def Set_Gen2_RxFilter(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Set_Gen2_RxFilter
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_RxFilter)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
def Get_Gen2_RxFilter(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Get_Gen2_RxFilter
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_RxFilter)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gb29768_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
def Set_Gb29768_RxFilter(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Set_Gb29768_RxFilter
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_RxFilter)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gb29768_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
def Get_Gb29768_RxFilter(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Get_Gb29768_RxFilter
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_RxFilter)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE Set_Gen2_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal)
def Set_Gen2_FilterCalibration(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Set_Gen2_FilterCalibration
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_FilterCalibration)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE Get_Gen2_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal)
def Get_Gen2_FilterCalibration(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Get_Gen2_FilterCalibration
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_FilterCalibration)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE Set_Gb29768_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal)
def Set_Gb29768_FilterCalibration(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Set_Gb29768_FilterCalibration
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_FilterCalibration)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE Get_Gb29768_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal)
def Get_Gb29768_FilterCalibration(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Func = lib.Get_Gb29768_FilterCalibration
        Func.argtypes = [POINTER(STUHFL_T_ST25RU3993_FilterCalibration)]
        Func.restype = ctypes.c_uint32
        retCode = Func(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_AntennaPower(STUHFL_T_ST25RU3993_AntennaPower *antPwr);
def Set_AntennaPower(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_AntennaPowerFunc = lib.Set_AntennaPower
        Set_AntennaPowerFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_AntennaPower)]
        Set_AntennaPowerFunc.restype = ctypes.c_uint32
        retCode = Set_AntennaPowerFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_AntennaPower(STUHFL_T_ST25RU3993_AntennaPower *antPwr);
def Get_AntennaPower(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_AntennaPowerFunc = lib.Get_AntennaPower
        Get_AntennaPowerFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_AntennaPower)]
        Get_AntennaPowerFunc.restype = ctypes.c_uint32
        retCode = Get_AntennaPowerFunc(_native)
    else:
        print("not connected..")
    return retCode
                
## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqRSSI(STUHFL_T_ST25RU3993_FreqRssi *freqRssi);
def Get_FreqRSSI(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_FreqRSSIFunc = lib.Get_FreqRSSI
        Get_FreqRSSIFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_FreqRssi)]
        Get_FreqRSSIFunc.restype = ctypes.c_uint32
        retCode = Get_FreqRSSIFunc(_native)
    else:
        print("not connected..")
    return retCode
            
## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqReflectedPower(STUHFL_T_ST25RU3993_FreqReflectedPowerInfo *freqReflectedPower);
def Get_FreqReflectedPower(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_FreqReflectedPowerFunc = lib.Get_FreqReflectedPower
        Get_FreqReflectedPowerFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_FreqReflectedPowerInfo)]
        Get_FreqReflectedPowerFunc.restype = ctypes.c_uint32
        retCode = Get_FreqReflectedPowerFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_ChannelList(STUHFL_T_ST25RU3993_ChannelList *channelList);
def Set_ChannelList(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_ChannelListFunc = lib.Set_ChannelList
        Set_ChannelListFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_ChannelList)]
        Set_ChannelListFunc.restype = ctypes.c_uint32
        retCode = Set_ChannelListFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_ChannelList(STUHFL_T_ST25RU3993_ChannelList *channelList);
def Get_ChannelList(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_ChannelListFunc = lib.Get_ChannelList
        Get_ChannelListFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_ChannelList)]
        Get_ChannelListFunc.restype = ctypes.c_uint32
        retCode = Get_ChannelListFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_TuningCaps(STUHFL_T_ST25RU3993_TuningCaps *tuning);
def Set_TuningCaps(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_TuningCapsFunc = lib.Set_TuningCaps
        Set_TuningCapsFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_TuningCaps)]
        Set_TuningCapsFunc.restype = ctypes.c_uint32
        retCode = Set_TuningCapsFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_TuningCaps(STUHFL_T_ST25RU3993_TuningCaps *tuning);    
def Get_TuningCaps(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_TuningCapsFunc = lib.Get_TuningCaps
        Get_TuningCapsFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_TuningCaps)]
        Get_TuningCapsFunc.restype = ctypes.c_uint32
        retCode = Get_TuningCapsFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV TuneChannel(STUHFL_T_ST25RU3993_TuneCfg *tuneCfg);
def TuneChannel(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        TuneChannelFunc = lib.TuneChannel
        TuneChannelFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_TuneCfg)]
        TuneChannelFunc.restype = ctypes.c_uint32
        retCode = TuneChannelFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_FreqHop(STUHFL_T_ST25RU3993_FreqHop *freqHop);
def Set_FreqHop(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_FreqHopFunc = lib.Set_FreqHop
        Set_FreqHopFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_FreqHop)]
        Set_FreqHopFunc.restype = ctypes.c_uint32
        retCode = Set_FreqHopFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqHop(STUHFL_T_ST25RU3993_FreqHop *freqHop);
def Get_FreqHop(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_FreqHopFunc = lib.Get_FreqHop
        Get_FreqHopFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_FreqHop)]
        Get_FreqHopFunc.restype = ctypes.c_uint32
        retCode = Get_FreqHopFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_FreqLBT(STUHFL_T_ST25RU3993_FreqLBT *freqLBT);
def Set_FreqLBT(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_FreqLBTFunc = lib.Set_FreqLBT
        Set_FreqLBTFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_FreqLBT)]
        Set_FreqLBTFunc.restype = ctypes.c_uint32
        retCode = Set_FreqLBTFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqLBT(STUHFL_T_ST25RU3993_FreqLBT *freqLBT);
def Get_FreqLBT(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_FreqLBTFunc = lib.Get_FreqLBT
        Get_FreqLBTFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_FreqLBT)]
        Get_FreqLBTFunc.restype = ctypes.c_uint32
        retCode = Get_FreqLBTFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_FreqContinuousModulation(STUHFL_T_ST25RU3993_FreqContinuousModulation *continuousModulation);
def Set_FreqContinuousModulation(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_FreqContinuousModulationFunc = lib.Set_FreqContinuousModulation
        Set_FreqContinuousModulationFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_FreqContinuousModulation)]
        Set_FreqContinuousModulationFunc.restype = ctypes.c_uint32
        retCode = Set_FreqContinuousModulationFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_Timings(STUHFL_T_ST25RU3993_Gen2_Timings *gen2Timing);
def Set_Gen2_Timings(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_Gen2_TimingsFunc = lib.Set_Gen2_Timings
        Set_Gen2_TimingsFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gen2_Timings)]
        Set_Gen2_TimingsFunc.restype = ctypes.c_uint32
        retCode = Set_Gen2_TimingsFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_Timings(STUHFL_T_ST25RU3993_Gen2_Timings *gen2Timing);
def Get_Gen2_Timings(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_Gen2_TimingsFunc = lib.Get_Gen2_Timings
        Get_Gen2_TimingsFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gen2_Timings)]
        Get_Gen2_TimingsFunc.restype = ctypes.c_uint32
        retCode = Get_Gen2_TimingsFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_ProtocolCfg(STUHFL_T_ST25RU3993_Gen2_ProtocolCfg *protocolCfg);
def Set_Gen2_ProtocolCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_Gen2_ProtocolCfgFunc = lib.Set_Gen2_ProtocolCfg
        Set_Gen2_ProtocolCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gen2_ProtocolCfg)]
        Set_Gen2_ProtocolCfgFunc.restype = ctypes.c_uint32
        retCode = Set_Gen2_ProtocolCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_ProtocolCfg(STUHFL_T_ST25RU3993_Gen2_ProtocolCfg *protocolCfg);
def Get_Gen2_ProtocolCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_Gen2_ProtocolCfgFunc = lib.Get_Gen2_ProtocolCfg
        Get_Gen2_ProtocolCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gen2_ProtocolCfg)]
        Get_Gen2_ProtocolCfgFunc.restype = ctypes.c_uint32
        retCode = Get_Gen2_ProtocolCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gb29768_ProtocolCfg(STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg *protocolCfg);
def Set_Gb29768_ProtocolCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_Gb29768_ProtocolCfgFunc = lib.Set_Gb29768_ProtocolCfg
        Set_Gb29768_ProtocolCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg)]
        Set_Gb29768_ProtocolCfgFunc.restype = ctypes.c_uint32
        retCode = Set_Gb29768_ProtocolCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gb29768_ProtocolCfg(STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg *protocolCfg);
def Get_Gb29768_ProtocolCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_Gb29768_ProtocolCfgFunc = lib.Get_Gb29768_ProtocolCfg
        Get_Gb29768_ProtocolCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg)]
        Get_Gb29768_ProtocolCfgFunc.restype = ctypes.c_uint32
        retCode = Get_Gb29768_ProtocolCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_TxRxCfg(STUHFL_T_ST25RU3993_TxRxCfg *txRxCfg);
def Set_TxRxCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_TxRxCfgFunc = lib.Set_TxRxCfg
        Set_TxRxCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_TxRxCfg)]
        Set_TxRxCfgFunc.restype = ctypes.c_uint32
        retCode = Set_TxRxCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_TxRxCfg(STUHFL_T_ST25RU3993_TxRxCfg *txRxCfg);
def Get_TxRxCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_TxRxCfgFunc = lib.Get_TxRxCfg
        Get_TxRxCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_TxRxCfg)]
        Get_TxRxCfgFunc.restype = ctypes.c_uint32
        retCode = Get_TxRxCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_PowerAmplifierCfg(STUHFL_T_ST25RU3993_PowerAmplifierCfg *PACfg);
def Set_PowerAmplifierCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_PowerAmplifierCfgFunc = lib.Set_PowerAmplifierCfg
        Set_PowerAmplifierCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_PowerAmplifierCfg)]
        Set_PowerAmplifierCfgFunc.restype = ctypes.c_uint32
        retCode = Set_PowerAmplifierCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_PowerAmplifierCfg(STUHFL_T_ST25RU3993_PowerAmplifierCfg *PACfg);
def Get_PowerAmplifierCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_PowerAmplifierCfgFunc = lib.Get_PowerAmplifierCfg
        Get_PowerAmplifierCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_PowerAmplifierCfg)]
        Get_PowerAmplifierCfgFunc.restype = ctypes.c_uint32
        retCode = Get_PowerAmplifierCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_InventoryCfg(STUHFL_T_ST25RU3993_Gen2_InventoryCfg *gen2Cfg);
def Set_Gen2_InventoryCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_Gen2_InventoryCfgFunc = lib.Set_Gen2_InventoryCfg
        Set_Gen2_InventoryCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gen2_InventoryCfg)]
        Set_Gen2_InventoryCfgFunc.restype = ctypes.c_uint32
        retCode = Set_Gen2_InventoryCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_InventoryCfg(STUHFL_T_ST25RU3993_Gen2_InventoryCfg *gen2Cfg);
def Get_Gen2_InventoryCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_Gen2_InventoryCfgFunc = lib.Get_Gen2_InventoryCfg
        Get_Gen2_InventoryCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gen2_InventoryCfg)]
        Get_Gen2_InventoryCfgFunc.restype = ctypes.c_uint32
        retCode = Get_Gen2_InventoryCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gb29768_InventoryCfg(STUHFL_T_ST25RU3993_Gb29768_InventoryCfg *gbCfg);
def Set_Gb29768_InventoryCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Set_Gb29768_InventoryCfgFunc = lib.Set_Gb29768_InventoryCfg
        Set_Gb29768_InventoryCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gb29768_InventoryCfg)]
        Set_Gb29768_InventoryCfgFunc.restype = ctypes.c_uint32           
        retCode = Set_Gb29768_InventoryCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gb29768_InventoryCfg(STUHFL_T_ST25RU3993_Gb29768_InventoryCfg *gbCfg);
def Get_Gb29768_InventoryCfg(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Get_Gb29768_InventoryCfgFunc = lib.Get_Gb29768_InventoryCfg
        Get_Gb29768_InventoryCfgFunc.argtypes = [POINTER(STUHFL_T_ST25RU3993_Gb29768_InventoryCfg)]
        Get_Gb29768_InventoryCfgFunc.restype = ctypes.c_uint32
        retCode = Get_Gb29768_InventoryCfgFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Select(STUHFL_T_Gen2_Select *genSelect);
def Gen2_Select(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_SelectFunc = lib.Gen2_Select
        Gen2_SelectFunc.argtypes = [POINTER(STUHFL_T_Gen2_Select)]
        Gen2_SelectFunc.restype = ctypes.c_uint32
        retCode = Gen2_SelectFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Read(STUHFL_T_Read *read);
def Gen2_Read(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_ReadFunc = lib.Gen2_Read
        Gen2_ReadFunc.argtypes = [POINTER(STUHFL_T_Read)]
        Gen2_ReadFunc.restype = ctypes.c_uint32
        retCode = Gen2_ReadFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Write(STUHFL_T_Gen2_Write *write);
def Gen2_Write(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_WriteFunc = lib.Gen2_Write
        Gen2_WriteFunc.argtypes = [POINTER(STUHFL_T_Write)]
        Gen2_WriteFunc.restype = ctypes.c_uint32
        retCode = Gen2_WriteFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_BlockWrite(STUHFL_T_Gen2_BlockWrite *blockWrite);
def Gen2_BlockWrite(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_BlockWriteFunc = lib.Gen2_BlockWrite
        Gen2_BlockWriteFunc.argtypes = [POINTER(STUHFL_T_Gen2_BlockWrite)]
        Gen2_BlockWriteFunc.restype = ctypes.c_uint32
        retCode = Gen2_BlockWriteFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Lock(STUHFL_T_Gen2_Lock *lock);
def Gen2_Lock(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_LockFunc = lib.Gen2_Lock
        Gen2_LockFunc.argtypes = [POINTER(STUHFL_T_Gen2_Lock)]
        Gen2_LockFunc.restype = ctypes.c_uint32
        retCode = Gen2_LockFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Kill(STUHFL_T_Gen2_Kill *kill);
def Gen2_Kill(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_KillFunc = lib.Gen2_Kill
        Gen2_KillFunc.argtypes = [POINTER(STUHFL_T_Kill)]
        Gen2_KillFunc.restype = ctypes.c_uint32
        retCode = Gen2_KillFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_GenericCmd(STUHFL_T_Gen2_GenericCmd *genericCmd);
def Gen2_GenericCmd(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_GenericCmdFunc = lib.Gen2_GenericCmd
        Gen2_GenericCmdFunc.argtypes = [POINTER(STUHFL_T_Gen2_GenericCmd)]
        Gen2_GenericCmdFunc.restype = ctypes.c_uint32
        retCode = Gen2_GenericCmdFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_QueryMeasureRssi(STUHFL_T_QueryMeasureRssi *measureRssi);
def Gen2_QueryMeasureRssi(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2_QueryMeasureRssiFunc = lib.Gen2_QueryMeasureRssi
        Gen2_QueryMeasureRssiFunc.argtypes = [POINTER(STUHFL_T_QueryMeasureRssi)]
        Gen2_QueryMeasureRssiFunc.restype = ctypes.c_uint32
        retCode = Gen2_QueryMeasureRssiFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Sort(STUHFL_T_Gb29768_Sort *gb29768Sort);
def Gb29768_Sort(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gb29768_SortFunc = lib.Gb29768_Sort
        Gb29768_SortFunc.argtypes = [POINTER(STUHFL_T_Gb29768_Sort)]
        Gb29768_SortFunc.restype = ctypes.c_uint32
        retCode = Gb29768_SortFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Read(STUHFL_T_Gb29768_Read *read);
def Gb29768_Read(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gb29768_ReadFunc = lib.Gb29768_Read
        Gb29768_ReadFunc.argtypes = [POINTER(STUHFL_T_Read)]
        Gb29768_ReadFunc.restype = ctypes.c_uint32
        retCode = Gb29768_ReadFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Write(STUHFL_T_Gb29768_Write *write);
def Gb29768_Write(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gb29768_WriteFunc = lib.Gb29768_Write
        Gb29768_WriteFunc.argtypes = [POINTER(STUHFL_T_Write)]
        Gb29768_WriteFunc.restype = ctypes.c_uint32
        retCode = Gb29768_WriteFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Lock(STUHFL_T_Gb29768_Lock *lock);
def Gb29768_Lock(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gb29768_LockFunc = lib.Gb29768_Lock
        Gb29768_LockFunc.argtypes = [POINTER(STUHFL_T_Gb29768_Lock)]
        Gb29768_LockFunc.restype = ctypes.c_uint32
        retCode = Gb29768_LockFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Kill(STUHFL_T_Gb29768_Kill *kill);
def Gb29768_Kill(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gb29768_KillFunc = lib.Gb29768_Kill
        Gb29768_KillFunc.argtypes = [POINTER(STUHFL_T_Kill)]
        Gb29768_KillFunc.restype = ctypes.c_uint32
        retCode = Gb29768_KillFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Erase(STUHFL_T_Gb29768_Erase *erase);
def Gb29768_Erase(_native):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gb29768_EraseFunc = lib.Gb29768_Erase
        Gb29768_EraseFunc.argtypes = [POINTER(STUHFL_T_Gb29768_Erase)]
        Gb29768_EraseFunc.restype = ctypes.c_uint32
        retCode = Gb29768_EraseFunc(_native)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Inventory(STUHFL_T_InventoryOption *invOption, STUHFL_T_InventoryData *invData);
def Gen2_Inventory(_native, _invData):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gen2InventoryFunc = lib.Gen2_Inventory
        Gen2InventoryFunc.argtypes = [POINTER(STUHFL_T_InventoryOption), POINTER(STUHFL_T_InventoryData)]
        Gen2InventoryFunc.restype = ctypes.c_uint32
        retCode = Gen2InventoryFunc(_native, _invData)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Inventory(STUHFL_T_InventoryOption *invOption, STUHFL_T_InventoryData *invData);
def Gb29768_Inventory(_native, _invData):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Gb29768InventoryFunc = lib.Gb29768_Inventory
        Gb29768InventoryFunc.argtypes = [POINTER(STUHFL_T_InventoryOption), POINTER(STUHFL_T_InventoryData)]
        Gb29768InventoryFunc.restype = ctypes.c_uint32
        retCode = Gb29768InventoryFunc(_native, _invData)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Inventory_RunnerStart(STUHFL_T_InventoryOption *option, STUHFL_T_InventoryCycle cycleCallback, STUHFL_T_InventoryFinished finishedCallback, STUHFL_T_InventoryData *data);
def Inventory_RunnerStart(_native, _cycleCB, _finishCB, _invData):
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Inventory_RunnerStartFunc = lib.Inventory_RunnerStart
        Inventory_RunnerStartFunc.argtypes = [POINTER(STUHFL_T_InventoryOption), ctypes.CFUNCTYPE(c_uint16, POINTER(STUHFL_T_InventoryData)), ctypes.CFUNCTYPE(c_uint16, POINTER(STUHFL_T_InventoryData)), POINTER(STUHFL_T_InventoryData)]
        Inventory_RunnerStartFunc.restype = ctypes.c_uint32
        retCode = Inventory_RunnerStartFunc(_native, _cycleCB, _finishCB, _invData)
    else:
        print("not connected..")
    return retCode

## Maps from STUHFL.dll to STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Inventory_RunnerStop(void)
def Inventory_RunnerStop():
    retCode = STUHFL_ERR_DLL
    if lib is not None:
        Inventory_RunnerStopFunc = lib.Inventory_RunnerStop
        Inventory_RunnerStopFunc.argtypes = []
        Inventory_RunnerStopFunc.restype = ctypes.c_uint32
        retCode = Inventory_RunnerStopFunc()
    else:
        print("not connected..")
    return retCode
