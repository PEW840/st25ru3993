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
import time
from time import sleep
import ctypes
from ctypes import *
import abc
from abc import ABC, abstractmethod 
#from deprecated import deprecated

import STUHFL_native

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

# - Native defines -----------------------------------------------------------------
STUHFL_D_MAX_VERSION_INFO_LENGTH = STUHFL_native.STUHFL_D_MAX_VERSION_INFO_LENGTH
MAX_REGISTERS = STUHFL_native.MAX_REGISTERS
#
STUHFL_D_MAX_TAG_LIST_SIZE = STUHFL_native.STUHFL_D_MAX_TAG_LIST_SIZE
#
STUHFL_D_MAX_EPC_LENGTH = STUHFL_native.STUHFL_D_MAX_EPC_LENGTH
STUHFL_D_MAX_XPC_LENGTH = STUHFL_native.STUHFL_D_MAX_XPC_LENGTH
STUHFL_D_MAX_TID_LENGTH = STUHFL_native.STUHFL_D_MAX_TID_LENGTH
STUHFL_D_MAX_PC_LENGTH = STUHFL_native.STUHFL_D_MAX_PC_LENGTH
STUHFL_D_GEN2_MAXQ = STUHFL_native.STUHFL_D_GEN2_MAXQ
STUHFL_D_MAX_FREQUENCY = STUHFL_native.STUHFL_D_MAX_FREQUENCY
STUHFL_D_NB_C_VALUES = STUHFL_native.STUHFL_D_NB_C_VALUES
STUHFL_D_MAX_ANTENNA = STUHFL_native.STUHFL_D_MAX_ANTENNA
#
STUHFL_D_PASSWORD_LEN = STUHFL_native.STUHFL_D_PASSWORD_LEN
STUHFL_D_MAX_READ_DATA_LEN = STUHFL_native.STUHFL_D_MAX_READ_DATA_LEN
STUHFL_D_MAX_WRITE_DATA_LEN = STUHFL_native.STUHFL_D_MAX_WRITE_DATA_LEN
STUHFL_D_MAX_BLOCKWRITE_DATA_LEN = STUHFL_native.STUHFL_D_MAX_BLOCKWRITE_DATA_LEN
#
STUHFL_D_GEN2_MAX_SELECT_MASK_LENGTH = STUHFL_native.STUHFL_D_GEN2_MAX_SELECT_MASK_LENGTH
STUHFL_D_GEN2_LOCK_MASK_ACTION_LEN = STUHFL_native.STUHFL_D_GEN2_LOCK_MASK_ACTION_LEN
STUHFL_D_GEN2_GENERIC_CMD_MAX_SND_DATA_BYTES = STUHFL_native.STUHFL_D_GEN2_GENERIC_CMD_MAX_SND_DATA_BYTES
STUHFL_D_GEN2_GENERIC_CMD_MAX_RCV_DATA_BYTES = STUHFL_native.STUHFL_D_GEN2_GENERIC_CMD_MAX_RCV_DATA_BYTES
#
STUHFL_D_GB29768_MAX_SORT_MASK_LENGTH = STUHFL_native.STUHFL_D_GB29768_MAX_SORT_MASK_LENGTH
#
STUHFL_D_INVENTORYREPORT_HEARTBEAT_DURATION_MS = STUHFL_native.STUHFL_D_INVENTORYREPORT_HEARTBEAT_DURATION_MS
#
STUHFL_D_RESET_DEFAULT_ALL_FREQS = STUHFL_native.STUHFL_D_RESET_DEFAULT_ALL_FREQS
STUHFL_D_FREQUENCY_MAX_VALUE = STUHFL_native.STUHFL_D_FREQUENCY_MAX_VALUE
STUHFL_D_DEFAULT_FREQUENCY = STUHFL_native.STUHFL_D_DEFAULT_FREQUENCY
#
STUHFL_D_GEN2_TIMING_USE_DEFAULT_T4MIN = STUHFL_native.STUHFL_D_GEN2_TIMING_USE_DEFAULT_T4MIN
#
STUHFL_D_LOG_LEVEL_COUNT = STUHFL_native.STUHFL_D_LOG_LEVEL_COUNT


# - EvalAPI defines -----------------------------------------------------------------
#STUHFL_ACTION
STUHFL_D_ACTION_INVENTORY = 0x00
STUHFL_D_ACTION_INVENTORY_W_SLOT_STATISTICS = 0x01

#STUHFL_RESET
STUHFL_D_RESET_TYPE_SOFT = 0x00
STUHFL_D_RESET_TYPE_HARD = 0x01
STUHFL_D_RESET_TYPE_CLEAR_COMM = 0x02

#LOG_LEVEL
STUHFL_D_LOG_LEVEL_INFO            = 0x00000001
STUHFL_D_LOG_LEVEL_WARNING         = 0x00000002
STUHFL_D_LOG_LEVEL_DEBUG           = 0x00000004
STUHFL_D_LOG_LEVEL_ERROR           = 0x00000008
STUHFL_D_LOG_LEVEL_TRACE_AL        = 0x00000010
STUHFL_D_LOG_LEVEL_TRACE_SL        = 0x00000020
STUHFL_D_LOG_LEVEL_TRACE_DL        = 0x00000040
STUHFL_D_LOG_LEVEL_TRACE_PL        = 0x00000080
STUHFL_D_LOG_LEVEL_TRACE_EVAL_API  = 0x00000100
STUHFL_D_LOG_LEVEL_TRACE_BL        = 0x00000200
STUHFL_D_LOG_LEVEL_ALL             = 0xFFFFFFFF

#RET_CODE
STUHFL_ERR_GENERIC                     =  1    
STUHFL_ERR_NONE                        =  0    
STUHFL_ERR_NOMEM                       = 0xFFFFFFFF+1-1         # Handle 32bits ANSI-C negative error codes: 4 294 967 295
STUHFL_ERR_BUSY                        = 0xFFFFFFFF+1-2    
STUHFL_ERR_IO                          = 0xFFFFFFFF+1-3    
STUHFL_ERR_TIMEOUT                     = 0xFFFFFFFF+1-4    
STUHFL_ERR_REQUEST                     = 0xFFFFFFFF+1-5    
STUHFL_ERR_NOMSG                       = 0xFFFFFFFF+1-6    
STUHFL_ERR_PARAM                       = 0xFFFFFFFF+1-7    
STUHFL_ERR_PROTO                       = 0xFFFFFFFF+1-8    

FIRST_ST25RU3993_ERROR                  = 0xFFFFFFFF+1-33
STUHFL_ERR_CHIP_NORESP                     = FIRST_ST25RU3993_ERROR - 0         # 4 294 967 263
STUHFL_ERR_CHIP_HEADER                     = FIRST_ST25RU3993_ERROR - 1
STUHFL_ERR_CHIP_PREAMBLE                   = FIRST_ST25RU3993_ERROR - 2
STUHFL_ERR_CHIP_RXCOUNT                    = FIRST_ST25RU3993_ERROR - 3
STUHFL_ERR_CHIP_CRCERROR                   = FIRST_ST25RU3993_ERROR - 4
STUHFL_ERR_CHIP_FIFO                       = FIRST_ST25RU3993_ERROR - 5
STUHFL_ERR_CHIP_COLL                       = FIRST_ST25RU3993_ERROR - 6
                                             
STUHFL_ERR_REFLECTED_POWER                 = FIRST_ST25RU3993_ERROR - 16        # 4 294 967 247
                                             
STUHFL_ERR_GEN2_SELECT                     = FIRST_ST25RU3993_ERROR - 32        # 4 294 967 231
STUHFL_ERR_GEN2_ACCESS                     = FIRST_ST25RU3993_ERROR - 33
STUHFL_ERR_GEN2_REQRN                      = FIRST_ST25RU3993_ERROR - 34
STUHFL_ERR_GEN2_CHANNEL_TIMEOUT            = FIRST_ST25RU3993_ERROR - 35
                                             
STUHFL_ERR_GEN2_ERRORCODE_OTHER            = FIRST_ST25RU3993_ERROR - 36        # 4 294 967 227
STUHFL_ERR_GEN2_ERRORCODE_NOTSUPPORTED     = FIRST_ST25RU3993_ERROR - 37
STUHFL_ERR_GEN2_ERRORCODE_PRIVILEGES       = FIRST_ST25RU3993_ERROR - 38
STUHFL_ERR_GEN2_ERRORCODE_MEMOVERRUN       = FIRST_ST25RU3993_ERROR - 39
STUHFL_ERR_GEN2_ERRORCODE_MEMLOCKED        = FIRST_ST25RU3993_ERROR - 40
STUHFL_ERR_GEN2_ERRORCODE_CRYPTO           = FIRST_ST25RU3993_ERROR - 41
STUHFL_ERR_GEN2_ERRORCODE_ENCAPSULATION    = FIRST_ST25RU3993_ERROR - 42
STUHFL_ERR_GEN2_ERRORCODE_RESPBUFOVERFLOW  = FIRST_ST25RU3993_ERROR - 43
STUHFL_ERR_GEN2_ERRORCODE_SECURITYTIMEOUT  = FIRST_ST25RU3993_ERROR - 44
STUHFL_ERR_GEN2_ERRORCODE_POWER_SHORTAGE   = FIRST_ST25RU3993_ERROR - 45
STUHFL_ERR_GEN2_ERRORCODE_NONSPECIFIC      = FIRST_ST25RU3993_ERROR - 46
                                             
STUHFL_ERR_GB29768_POWER_SHORTAGE          = FIRST_ST25RU3993_ERROR - 48        # 4 294 967 215
STUHFL_ERR_GB29768_PERMISSION_ERROR        = FIRST_ST25RU3993_ERROR - 49  
STUHFL_ERR_GB29768_STORAGE_OVERFLOW        = FIRST_ST25RU3993_ERROR - 50  
STUHFL_ERR_GB29768_STORAGE_LOCKED          = FIRST_ST25RU3993_ERROR - 51  
STUHFL_ERR_GB29768_PASSWORD_ERROR          = FIRST_ST25RU3993_ERROR - 52  
STUHFL_ERR_GB29768_AUTH_ERROR              = FIRST_ST25RU3993_ERROR - 53  
STUHFL_ERR_GB29768_ACCESS_ERROR            = FIRST_ST25RU3993_ERROR - 54  
STUHFL_ERR_GB29768_ACCESS_TIMEOUT_ERROR    = FIRST_ST25RU3993_ERROR - 55  
STUHFL_ERR_GB29768_OTHER                   = FIRST_ST25RU3993_ERROR - 56  

# ---------------------------------------------------------------------------
# Connection access
# ---------------------------------------------------------------------------
# region Connection access

## Maps STUHFL ANSI-C API: Connect()   \n
#  STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Connect(char *szComPort);
#  Connect to board
# @param comPort: ComPort to which establish the connection
# @return error code
def Connect(comPort):
    retCode = STUHFL_native.Connect(comPort.encode('utf_8'))
    if retCode == STUHFL_ERR_NONE:
        # give board time to wakeup
        time.sleep(0.6)
    return retCode

## Maps STUHFL ANSI-C API: Disconnect()   \n
# STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Disconnect(void);
# Disconnect from board
#@return error code
def Disconnect():
    return STUHFL_native.Disconnect()

## Maps STUHFL ANSI-C API: Reboot()   \n
# STUHFL_DLL_API void CALL_CONV Reboot(void);
# Reboot board
#@return error code
def Reboot():
    return STUHFL_native.Reboot()

## Maps STUHFL ANSI-C API: EnterBootloader()   \n
# STUHFL_DLL_API void CALL_CONV EnterBootloader(void);
# Enter boot loader
#@return error code
def EnterBootloader():
    return STUHFL_native.EnterBootloader()

#endregion Connection access


# ---------------------------------------------------------------------------
# General 
# ---------------------------------------------------------------------------
# region General

## Maps STUHFL ANSI-C structure: STUHFL_T_Version (specifically for Lib Version)   \n
#  and maps all related functions through dedicated methods 
#
class STUHFL_T_VersionLib:
    def __init__(self):
        # "public" members
        ## O Param: [Major, Minor, Micro, Nano] version 
        self.version = []

    # Internal methods
    def _setFromNative(self, _native):
        self.version[:] = [(_native & 0xFF000000)>>24, (_native & 0x00FF0000)>>16, (_native & 0x0000FF00)>>8, (_native & 0x000000FF)>>0 ]  

    ## Maps STUHFL ANSI-C API: STUHFL_F_GetLibVersion()   \n
    #  Nota: can be executed at any time (even before board connection)
    #@return error code
    #
    def fetch(self):
        _native = STUHFL_native.GetLibVersion()
        self._setFromNative(_native)
        return STUHFL_ERR_NONE

## Maps STUHFL ANSI-C structure: STUHFL_T_Version (specifically for HW/SW Version)   \n
# and maps all related functions through dedicated methods 
#
class STUHFL_T_VersionBoard:
    def __init__(self):
        # "public" members
        ## O Param: [Major, Minor, Micro, Nano] SW version 
        self.swVersion = []
        ## O Param: [Major, Minor, Micro, Nano] HW version 
        self.hwVersion = []

    # Internal methods
    def _setFromNative(self, _nativeSwVer, _nativeHwVer):
        self.swVersion[:] = [_nativeSwVer.major, _nativeSwVer.minor, _nativeSwVer.micro, _nativeSwVer.nano]  
        self.hwVersion[:] = [_nativeHwVer.major, _nativeHwVer.minor, _nativeHwVer.micro, _nativeHwVer.nano]  
    
    ## Maps STUHFL ANSI-C API: Get_BoardVersion()   \n
    #  Nota: can only be executed once board connection is established
    #@return error code
    #
    def fetch(self):
        _nativeSwVer = STUHFL_native.STUHFL_T_Version()
        _nativeHwVer = STUHFL_native.STUHFL_T_Version()
        retCode = STUHFL_native.Get_BoardVersion(_nativeSwVer, _nativeHwVer)
        self._setFromNative(_nativeSwVer, _nativeHwVer)  
        return retCode

#
class STUHFL_T_VersionInfo:
    def __init__(self):
        # "public" members
        ## O Param: SW version textual information 
        self.swVersionInfo = ""
        ## O Param: HW version textual information 
        self.hwVersionInfo = ""
        # "private" members for native argument access
        self.__swVersionInfo = STUHFL_native.STUHFL_T_VersionInfo()
        self.__hwVersionInfo = STUHFL_native.STUHFL_T_VersionInfo()
        # allocate memory and initalize
        self.__swVersionInfo.info = bytes(bytearray(STUHFL_native.STUHFL_D_MAX_VERSION_INFO_LENGTH))
        self.__hwVersionInfo.info = bytes(bytearray(STUHFL_native.STUHFL_D_MAX_VERSION_INFO_LENGTH))
        self.__swVersionInfo.infoLength = 0
        self.__hwVersionInfo.infoLength = 0
 
    ## Maps STUHFL ANSI-C API: Get_BoardInfo()   \n
    #@return error code
    #
    # STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_BoardInfo(STUHFL_T_VersionInfo *swInfo, STUHFL_T_VersionInfo *hwInfo);
    def fetch(self):
        retCode = STUHFL_native.Get_BoardInfo(self.__swVersionInfo, self.__hwVersionInfo)
        self.swVersionInfo = (self.__swVersionInfo.info).decode("utf-8")
        self.hwVersionInfo = (self.__hwVersionInfo.info).decode("utf-8")
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Register     \n
#   and maps all related functions through dedicated methods 
#
class STUHFL_T_ST25RU3993_Register:
    ## Content of a 'multi' entry
    class Item:
        def __init__(self, addr = 0, data = 0):
            ## I Param: Register address 
            self.addr = addr
            ## I/O Param: Register data 
            self.data = data

    ## @param addr: address of single element
    ## @param data: data of single element
    def __init__(self, addr = 0, data = 0):
        # "public" members
        ## I Param: Register address 
        self.addr = addr
        ## I/O Param: Register data 
        self.data = data
        ## I/O multi: Multi registers access array 
        self.multi = []

    # Internal methods
    def _toNative(self):
        return self._toNativeSingle()

    def _toNativeSingle(self):
        _nativeSingle = STUHFL_native.STUHFL_T_ST25RU3993_Register()
        _nativeSingle.addr = self.addr
        _nativeSingle.data = self.data
        return _nativeSingle

    def _setFromNativeSingle(self, _nativeSingle):
        self.addr = _nativeSingle.addr
        self.data = _nativeSingle.data

    def _toNativeMulti(self):
        _nativeMultiple = ctypes.cast((STUHFL_native.STUHFL_T_ST25RU3993_Register * STUHFL_native.MAX_REGISTERS)(), ctypes.POINTER(STUHFL_native.STUHFL_T_ST25RU3993_Register))
        for idx, i in enumerate(self.multi):
            _nativeMultiple[idx].addr = i.addr
            _nativeMultiple[idx].data = i.data
        return _nativeMultiple

    def _setFromNativeMulti(self, _nativeMultiple):
        for idx, i in enumerate(self.multi):
            i.addr = _nativeMultiple[idx].addr
            i.data = _nativeMultiple[idx].data

    ## Maps STUHFL ANSI-C API: Set_Register()   \n
    ##  Set register with predefined class members addr + data
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Register(STUHFL_T_ST25RU3993_Register *reg);
    def commit(self):
        _native = self._toNativeSingle()
        retCode = STUHFL_native.Set_Register(_native)
        return retCode    

    ## Maps STUHFL ANSI-C API: Get_Register()   \n
    ## Get register into class member data
    ##@param regAddr: Address of register to be accessed
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Register(STUHFL_T_ST25RU3993_Register *reg);
    def fetch(self, regAddr=None):
        if regAddr is not None:
            self.addr = regAddr
        _native = self._toNativeSingle()
        retCode = STUHFL_native.Get_Register(_native)
        self._setFromNativeSingle(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Set_RegisterMultiple()   \n
    ## Set multiple registers with all predefined class members multi[].addr + multi[].data
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_RegisterMultiple(STUHFL_T_ST25RU3993_Register **reg, uint8_t numReg);
    def commitmultiple(self):
        if len(self.multi) > STUHFL_native.MAX_REGISTERS:
            print('Only max {} registers can be accessed at once..'.format(STUHFL_native.MAX_REGISTERS))
            return STUHFL_ERR_PARAM
        _native = self._toNativeMulti()
        retCode = STUHFL_native.Set_RegisterMultiple(_native, len(self.multi))
        return retCode 

    ## Maps STUHFL ANSI-C API: Get_RegisterMultiple()   \n
    ## Get multiple registers from all predefined class members multi[].addr into class members multi[].data
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_RegisterMultiple(uint8_t numReg, STUHFL_T_ST25RU3993_Register **reg);
    def fetchmultiple(self):
        if len(self.multi) > STUHFL_native.MAX_REGISTERS:
            print('Only max {} registers can be accessed at once..'.format(STUHFL_native.MAX_REGISTERS))
            return STUHFL_ERR_PARAM
        _native = self._toNativeMulti()
        retCode = STUHFL_native.Get_RegisterMultiple(len(self.multi), _native)            
        self._setFromNativeMulti(_native)
        return retCode

# STUHFL_D_RWD_CFG_ID
STUHFL_D_RWD_CFG_ID_POWER_DOWN_MODE = 0x00
STUHFL_D_RWD_CFG_ID_EXTVCO  = 0x01
STUHFL_D_RWD_CFG_ID_POWER_AMPLIFIER = 0x02
STUHFL_D_RWD_CFG_ID_INPUT = 0x03
STUHFL_D_RWD_CFG_ID_ANTENNA_SWITCH = 0x04
STUHFL_D_RWD_CFG_ID_TUNER = 0x05
STUHFL_D_RWD_CFG_ID_HARDWARE_ID_NUM = 0x06

#RWD_CFG_HW_ID
STUHFL_D_RWD_CFG_HW_ID_DISCOVERY = 1
STUHFL_D_RWD_CFG_HW_ID_EVAL      = 2
STUHFL_D_RWD_CFG_HW_ID_JIGEN     = 3
STUHFL_D_RWD_CFG_HW_ID_ELANCE    = 4

#RWD_CFG_POWER_MODE
STUHFL_D_RWD_CFG_POWER_MODE_DOWN        = 0
STUHFL_D_RWD_CFG_POWER_MODE_NORMAL      = 1
STUHFL_D_RWD_CFG_POWER_MODE_NORMAL_RF   = 2
STUHFL_D_RWD_CFG_POWER_MODE_STANDBY     = 3

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_RwdConfig     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_RwdConfig:
    ##
    ## @param id: Reader configuration ID
    ## @param value: Corresponding configuration value
    ##
    def __init__(self, id = STUHFL_D_RWD_CFG_ID_HARDWARE_ID_NUM, value = 0):
        # "public" members
        ## I Param: Reader configuration ID 
        self.id = id
        ## I/O Param: Corresponding configuration value 
        self.value = value

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_RwdConfig()
        _native.id = self.id
        _native.value = self.value
        return _native

    def _setFromNative(self, _native):
        self.id = _native.id
        self.value = _native.value

    ## Maps STUHFL ANSI-C API: Set_RwdCfg()   \n
    ## Set RwdConfig with predefined class members id + value
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_RwdCfg(STUHFL_T_ST25RU3993_RwdConfig *rwdCfg);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_RwdCfg(_native)
        return retCode    

    ## Maps STUHFL ANSI-C API: Get_RwdCfg()   \n
    ## Get RwdConfig with predefined class members id into class member value
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_RwdCfg(STUHFL_T_ST25RU3993_RwdConfig *rwdCfg);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_RwdCfg(_native)
        self._setFromNative(_native)
        return retCode

#ANTENNA_POWER
STUHFL_D_ANTENNA_POWER_MODE_ON = 0
STUHFL_D_ANTENNA_POWER_MODE_OFF = 0xFF

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_AntennaPower     \n
##  and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_AntennaPower:
    ##
    ##  @param mode: Antenna Power mode
    ##  @param timeout: Timeout before settings will be applied
    ##  @param frequency: Frequency to be used
    ##
    def __init__(self, mode = STUHFL_D_ANTENNA_POWER_MODE_OFF, timeout = 0, frequency = STUHFL_native.STUHFL_D_DEFAULT_FREQUENCY):
        # "public" members
        ## I/O Param: Antenna Power mode 
        self.mode      = mode
        ## I/O Param: Timeout before settings will be applied 
        self.timeout   = timeout
        ## I/O Param: Frequency to be used 
        self.frequency = frequency
   
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_AntennaPower()
        _native.mode      = self.mode
        _native.timeout   = self.timeout  
        _native.frequency = self.frequency
        return _native

    def _setFromNative(self, _native):
        self.mode      = _native.mode
        self.timeout   = _native.timeout  
        self.frequency = _native.frequency

    ## Maps STUHFL ANSI-C API: Set_AntennaPower()   \n
    ## Set Antenna Power with predefined class members mode + timeout + frequency
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_AntennaPower(STUHFL_T_ST25RU3993_AntennaPower *antPwr);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_AntennaPower(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_AntennaPower()   \n
    ## Get Antenna Power 
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_AntennaPower(STUHFL_T_ST25RU3993_AntennaPower *antPwr);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_AntennaPower(_native)
        self._setFromNative(_native)
        return retCode

# endregion General



# ---------------------------------------------------------------------------
# Configuration 
# ---------------------------------------------------------------------------
# region Configuration

##  Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_FreqRssi     \n
##  and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_FreqRssi:
    ##
    ## @param frequency: Frequency for RSSI
    ##
    def __init__(self, frequency = STUHFL_native.STUHFL_D_DEFAULT_FREQUENCY):
        # "public" members
        ## I Param: Frequency for RSSI 
        self.frequency = frequency
        ## O Param: I parameter of logarithmic scaled RSSI 
        self.rssiLogI  = 0
        ## O Param: Q parameter of logarithmic scaled RSSI 
        self.rssiLogQ  = 0
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_FreqRssi()
        _native.frequency   =     self.frequency
        _native.rssiLogI    =     self.rssiLogI 
        _native.rssiLogQ    =     self.rssiLogQ 
        return _native

    def _setFromNative(self, _native):
        self.frequency = _native.frequency
        self.rssiLogI  = _native.rssiLogI 
        self.rssiLogQ  = _native.rssiLogQ 

    ## Maps STUHFL ANSI-C API: Get_FreqRSSI()   \n
    ## Get RSSI with predefined class members frequency
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqRSSI(STUHFL_T_ST25RU3993_FreqRssi *freqRssi);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_FreqRSSI(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_FreqReflectedPowerInfo     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_FreqReflectedPowerInfo:
    ##
    ## @param frequency: Frequency to be used for the measurement 
    ## @param applyTunerSetting: flag to apply tuner settings for frequency 
    ##
    def __init__(self, frequency = STUHFL_native.STUHFL_D_DEFAULT_FREQUENCY, applyTunerSetting = False):
        # "public" members
        ## I Param: Frequency to be used for the measurement 
        self.frequency         = frequency
        ## I Param: flag to apply tuner settings for frequency 
        self.applyTunerSetting = applyTunerSetting
        ## O Param: Reflected I 
        self.reflectedI        = 0
        ## O Param: Reflected Q 
        self.reflectedQ        = 0
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_FreqReflectedPowerInfo()
        _native.frequency             =   self.frequency          
        _native.applyTunerSetting     =   self.applyTunerSetting  
        _native.reflectedI            =   self.reflectedI         
        _native.reflectedQ            =   self.reflectedQ        
        return _native

    def _setFromNative(self, _native):
        self.frequency         = _native.frequency        
        self.applyTunerSetting = _native.applyTunerSetting
        self.reflectedI        = _native.reflectedI       
        self.reflectedQ        = _native.reflectedQ       

    ## Maps STUHFL ANSI-C API: Get_FreqReflectedPower()   \n
    ## Get Reflected Power from predefined class members frequency + applyTunerSetting
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqReflectedPower(STUHFL_T_ST25RU3993_FreqReflectedPowerInfo *reflectedPowerInfo);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_FreqReflectedPower(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Caps     \n
##
class STUHFL_T_ST25RU3993_Caps:
    def __init__(self, cin = 0, clen = 0, cout = 0):
        # "public" members
        ## I/O Param: IN capacitance of tuning table 
        self.cin  = cin
        ## I/O Param: LEN capacitance of tuning table 
        self.clen = clen
        ## I/O Param: OUT capacitance of tuning table 
        self.cout = cout

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Caps()
        _native.cin         =   self.cin          
        _native.clen        =   self.clen          
        _native.cout        =   self.cout          
        return _native

    def _setFromNative(self, _native):
        self.cin        = _native.cin 
        self.clen       = _native.clen
        self.cout       = _native.cout

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_ChannelItem     \n
##
class STUHFL_T_ST25RU3993_ChannelItem:
    def __init__(self, frequency = STUHFL_native.STUHFL_D_DEFAULT_FREQUENCY, caps = STUHFL_T_ST25RU3993_Caps(), rfu1=0, rfu2=0):
        # "public" members
        ## I/O Param: Frequency to be used for channel item 
        self.frequency = frequency
        ## I/O Param: Tuning capacitors for this frequency 
        self.caps      = caps
        self.rfu1      = rfu1
        self.rfu2      = rfu2

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_ChannelItem()
        _native.frequency   =   self.frequency          
        _native.caps        =   self.caps._toNative()          
        _native.rfu1        =   self.rfu1          
        _native.rfu2        =   self.rfu2         
        return _native

    def _setFromNative(self, _native):
        self.frequency   =   _native.frequency          
        self.caps._setFromNative(_native.caps)          
        self.rfu1        =   _native.rfu1            
        self.rfu2        =   _native.rfu2           

#PROFILE
STUHFL_D_PROFILE_EUROPE = 1
STUHFL_D_PROFILE_USA = 2
STUHFL_D_PROFILE_JAPAN = 3
STUHFL_D_PROFILE_CHINA = 4
STUHFL_D_PROFILE_CHINA2 = 5

#ANTENNA
STUHFL_D_ANTENNA_1   = 0
STUHFL_D_ANTENNA_2   = 1
STUHFL_D_ANTENNA_3   = 2
STUHFL_D_ANTENNA_4   = 3
STUHFL_D_ANTENNA_ALT = 0xFF

#TUNING_ALGO
STUHFL_D_TUNING_ALGO_NONE        = 0     ## No Tuning 
STUHFL_D_TUNING_ALGO_FAST        = 1     ## Simple automatic tuning function.This function tries to find an optimized tuner setting(minimal reflected power). The function starts at the current tuner setting and modifies the tuner caps until a setting with a minimum of reflected power is found.When changing the tuner further leads to an increase of reflected power the algorithm stops. Note that, although the algorithm has been optimized to not immediately stop at local minima of reflected power, it still might not find the tuner setting with the lowest reflected power.The algorithm of tunerMultiHillClimb() is probably producing better results, but it is slower.
STUHFL_D_TUNING_ALGO_SLOW        = 2     ## Sophisticated automatic tuning function.This function tries to find an optimized tuner setting(minimal reflected power). The function splits the 3 - dimensional tuner - setting - space(axis are Cin, Clen and Cout) into segments and searches in each segment(by using tunerOneHillClimb()) for its local minimum of reflected power. The tuner setting(point in tuner - setting - space) which has the lowest reflected power is returned in parameter res. This function has a much higher probability to find the tuner setting with the lowest reflected power than tunerOneHillClimb() but on the other hand takes much longer.
STUHFL_D_TUNING_ALGO_MEDIUM      = 3     ## Enhanced Sophisticated automatic tuning function.This function tries to find an optimized tuner setting(minimal reflected power). The function splits the 3 - dimensional tuner - setting - space(axis are Cin, Clen and Cout) into segments and get reflected power for each of them.A tunerOneHillClimb() is then run on the 3 segments with minimum of reflected power. The tuner setting(point in tuner - setting - space) which has the lowest reflected power is then returned in parameter res. This function has a much higher probability to find the tuner setting with the lowest reflected power than tunerOneHillClimb() and is faster than tunerMultiHillClimb().

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_TuningCaps     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_TuningCaps:
    ##
    ## @param antenna: Antenna to which the ChannelList belongs 
    ## @param channelListIdx: Current itemList index in channel list 
    ## @param caps: tuning caps. 
    ##
    def __init__(self, antenna = STUHFL_D_ANTENNA_1, channelListIdx = 0, caps = STUHFL_T_ST25RU3993_Caps()):
        # "public" members
         ## I Param: Antenna to which the ChannelList belongs 
        self.antenna            = antenna
        ## I/O Param: Current itemList index in channel list 
        self.channelListIdx     = channelListIdx
        ## I/O Param: Tuning caps at antenna 
        self.caps               = caps

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_TuningCaps()
        _native.antenna         = self.antenna       
        _native.channelListIdx  = self.channelListIdx
        _native.caps            = self.caps._toNative()          
        return _native

    def _setFromNative(self, _native):
        self.antenna                = _native.antenna       
        self.channelListIdx         = _native.channelListIdx
        self.caps._setFromNative(_native.caps)

    ## Maps STUHFL ANSI-C API: Set_TuningCaps()   \n
    ## Set TuningCaps with predefined class members antenna + channelListIdx + caps
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_TuningCaps(STUHFL_T_ST25RU3993_TuningCaps *tuning);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_TuningCaps(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_TuningCaps()   \n
    ## Get TuningCaps from predefined class members antenna + channelListIdx into class member caps
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_TuningCaps(STUHFL_T_ST25RU3993_TuningCaps *tuning);    
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_TuningCaps(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_ChannelList     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_ChannelList:
    ##
    ## @param profile: Frequencies profile (STUHFL_D_PROFILE_EUROPE, STUHFL_D_PROFILE_USA, STUHFL_D_PROFILE_CHINA, ...) to be generated 
    ## @param antenna: Antenna to which the ChannelList belongs 
    ## @param persistent: Get channel list from persistent flash memory / Save tuning values after Tuning
    ## @param itemList: Array of Channel list items. 
    ## @param channelListIdx: Current itemList index in channel list 
    ##
    def __init__(self, profile=None, antenna = STUHFL_D_ANTENNA_1, persistent = False, itemList = [STUHFL_T_ST25RU3993_ChannelItem()], channelListIdx = 0):
        # "public" members
        #ChannelList
        ## I Param: Antenna to which the ChannelList belongs 
        self.antenna               = antenna
        ## I Param: Set/Get channel list to/from persistent flash memory 
        self.persistent            = persistent
        ## I/O Param: Current itemList index in channel list 
        self.channelListIdx        = channelListIdx

        #TuneCfg
        ## I Param: Do False Positive Detection check 
        self.falsePositiveDetection          = True    
        ## I Param: Used algorithm for tuning. 
        self.algorithm          = STUHFL_D_TUNING_ALGO_MEDIUM      

        if profile is not None:
            if profile == STUHFL_D_PROFILE_EUROPE:
                self.itemList = [STUHFL_T_ST25RU3993_ChannelItem(866900), STUHFL_T_ST25RU3993_ChannelItem(865700), STUHFL_T_ST25RU3993_ChannelItem(866300), STUHFL_T_ST25RU3993_ChannelItem(867500)]
            elif profile == STUHFL_D_PROFILE_USA:
                self.itemList = [STUHFL_T_ST25RU3993_ChannelItem(902750), STUHFL_T_ST25RU3993_ChannelItem(915250), STUHFL_T_ST25RU3993_ChannelItem(903250), STUHFL_T_ST25RU3993_ChannelItem(915750), STUHFL_T_ST25RU3993_ChannelItem(903750),
                                 STUHFL_T_ST25RU3993_ChannelItem(916250), STUHFL_T_ST25RU3993_ChannelItem(904250), STUHFL_T_ST25RU3993_ChannelItem(916750), STUHFL_T_ST25RU3993_ChannelItem(904750), STUHFL_T_ST25RU3993_ChannelItem(917250),
                                 STUHFL_T_ST25RU3993_ChannelItem(905250), STUHFL_T_ST25RU3993_ChannelItem(917750), STUHFL_T_ST25RU3993_ChannelItem(905750), STUHFL_T_ST25RU3993_ChannelItem(918250), STUHFL_T_ST25RU3993_ChannelItem(906250),
                                 STUHFL_T_ST25RU3993_ChannelItem(918750), STUHFL_T_ST25RU3993_ChannelItem(906750), STUHFL_T_ST25RU3993_ChannelItem(919250), STUHFL_T_ST25RU3993_ChannelItem(907250), STUHFL_T_ST25RU3993_ChannelItem(919750),
                                 STUHFL_T_ST25RU3993_ChannelItem(907750), STUHFL_T_ST25RU3993_ChannelItem(920250), STUHFL_T_ST25RU3993_ChannelItem(908250), STUHFL_T_ST25RU3993_ChannelItem(920750), STUHFL_T_ST25RU3993_ChannelItem(908750),
                                 STUHFL_T_ST25RU3993_ChannelItem(921250), STUHFL_T_ST25RU3993_ChannelItem(909250), STUHFL_T_ST25RU3993_ChannelItem(921750), STUHFL_T_ST25RU3993_ChannelItem(909750), STUHFL_T_ST25RU3993_ChannelItem(922250),
                                 STUHFL_T_ST25RU3993_ChannelItem(910250), STUHFL_T_ST25RU3993_ChannelItem(922750), STUHFL_T_ST25RU3993_ChannelItem(910750), STUHFL_T_ST25RU3993_ChannelItem(923250), STUHFL_T_ST25RU3993_ChannelItem(911250),
                                 STUHFL_T_ST25RU3993_ChannelItem(923750), STUHFL_T_ST25RU3993_ChannelItem(911750), STUHFL_T_ST25RU3993_ChannelItem(924250), STUHFL_T_ST25RU3993_ChannelItem(912250), STUHFL_T_ST25RU3993_ChannelItem(924750),
                                 STUHFL_T_ST25RU3993_ChannelItem(912750), STUHFL_T_ST25RU3993_ChannelItem(925250), STUHFL_T_ST25RU3993_ChannelItem(913250), STUHFL_T_ST25RU3993_ChannelItem(925750), STUHFL_T_ST25RU3993_ChannelItem(913750),
                                 STUHFL_T_ST25RU3993_ChannelItem(926250), STUHFL_T_ST25RU3993_ChannelItem(914250), STUHFL_T_ST25RU3993_ChannelItem(926750), STUHFL_T_ST25RU3993_ChannelItem(914750), STUHFL_T_ST25RU3993_ChannelItem(927250)]
            elif profile == STUHFL_D_PROFILE_JAPAN:
                self.itemList = [STUHFL_T_ST25RU3993_ChannelItem(920500), STUHFL_T_ST25RU3993_ChannelItem(920700), STUHFL_T_ST25RU3993_ChannelItem(920900), STUHFL_T_ST25RU3993_ChannelItem(921100), STUHFL_T_ST25RU3993_ChannelItem(921300),
                                 STUHFL_T_ST25RU3993_ChannelItem(921500), STUHFL_T_ST25RU3993_ChannelItem(921700), STUHFL_T_ST25RU3993_ChannelItem(921900), STUHFL_T_ST25RU3993_ChannelItem(922100)]
            elif profile == STUHFL_D_PROFILE_CHINA:
                self.itemList = [STUHFL_T_ST25RU3993_ChannelItem(840625), STUHFL_T_ST25RU3993_ChannelItem(840875), STUHFL_T_ST25RU3993_ChannelItem(841125), STUHFL_T_ST25RU3993_ChannelItem(841375), STUHFL_T_ST25RU3993_ChannelItem(841625),
                                 STUHFL_T_ST25RU3993_ChannelItem(841875), STUHFL_T_ST25RU3993_ChannelItem(842125), STUHFL_T_ST25RU3993_ChannelItem(842375), STUHFL_T_ST25RU3993_ChannelItem(842625), STUHFL_T_ST25RU3993_ChannelItem(842875),
                                 STUHFL_T_ST25RU3993_ChannelItem(843125), STUHFL_T_ST25RU3993_ChannelItem(843375), STUHFL_T_ST25RU3993_ChannelItem(843625), STUHFL_T_ST25RU3993_ChannelItem(843875), STUHFL_T_ST25RU3993_ChannelItem(844125),
                                 STUHFL_T_ST25RU3993_ChannelItem(844375)]
            elif profile == STUHFL_D_PROFILE_CHINA2:
                self.itemList = [STUHFL_T_ST25RU3993_ChannelItem(920625), STUHFL_T_ST25RU3993_ChannelItem(920875), STUHFL_T_ST25RU3993_ChannelItem(921125), STUHFL_T_ST25RU3993_ChannelItem(921375), STUHFL_T_ST25RU3993_ChannelItem(921625),
                                 STUHFL_T_ST25RU3993_ChannelItem(921875), STUHFL_T_ST25RU3993_ChannelItem(922125), STUHFL_T_ST25RU3993_ChannelItem(922375), STUHFL_T_ST25RU3993_ChannelItem(922625), STUHFL_T_ST25RU3993_ChannelItem(922875),
                                 STUHFL_T_ST25RU3993_ChannelItem(923125), STUHFL_T_ST25RU3993_ChannelItem(923375), STUHFL_T_ST25RU3993_ChannelItem(923625), STUHFL_T_ST25RU3993_ChannelItem(923875), STUHFL_T_ST25RU3993_ChannelItem(924125),
                                 STUHFL_T_ST25RU3993_ChannelItem(924375)]
            else:
                self.itemList = itemList
        else:
            self.itemList = itemList


    # Internal methods
    def _toNative(self):
        return self._toNativeChannelList()

    def _toNativeChannelList(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_ChannelList()
        _native.antenna               = self.antenna              
        _native.persistent            = self.persistent           
        _native.numFrequencies        = len(self.itemList)
        _native.channelListIdx        = self.channelListIdx
        for i, itemList in enumerate(self.itemList):
            _native.itemList[i]  = self.itemList[i]._toNative()
        return _native

    def _setFromNativeChannelList(self, _native):
        self.antenna               = _native.antenna              
        self.persistent            = _native.persistent           
        self.channelListIdx        = _native.channelListIdx
        self.itemList              = [STUHFL_T_ST25RU3993_ChannelItem(_native.itemList[i].frequency, STUHFL_T_ST25RU3993_Caps(_native.itemList[i].caps.cin, _native.itemList[i].caps.clen, _native.itemList[i].caps.cout), _native.itemList[i].rfu1, _native.itemList[i].rfu2) for i in range(_native.numFrequencies)]

    def _toNativeTuneCfg(self, tuneAll):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_TuneCfg()
        _native.falsePositiveDetection         = self.falsePositiveDetection        
        _native.persistent        = self.persistent       
        _native.channelListIdx    = self.channelListIdx   
        _native.antenna           = self.antenna          
        _native.algorithm         = self.algorithm        
        _native.tuneAll           = True if tuneAll else False
        return _native

    ## Maps STUHFL ANSI-C API: Set_ChannelList()   \n
    ## Set Channel List with predefined class members antenna + persistent + channelListIdx + itemList[]
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_ChannelList(STUHFL_T_ST25RU3993_ChannelList *channelList);
    def commit(self):
        if len(self.itemList) > STUHFL_native.STUHFL_D_MAX_FREQUENCY:
            print('Item exceeds max len of {} ({}) ..'.format(STUHFL_native.STUHFL_D_MAX_FREQUENCY, len(self.itemList)))
            return STUHFL_ERR_PARAM
        _native = self._toNativeChannelList()
        retCode = STUHFL_native.Set_ChannelList(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_ChannelList()   \n
    ## Get Channel List from predefined class members antenna + persistent + channelListIdx into class members itemList[]
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_ChannelList(STUHFL_T_ST25RU3993_ChannelList *channelList);
    def fetch(self):
        if len(self.itemList) > STUHFL_native.STUHFL_D_MAX_FREQUENCY:
            print('Item exceeds max len of {} ({}) ..'.format(STUHFL_native.STUHFL_D_MAX_FREQUENCY, len(self.itemList)))
            return STUHFL_ERR_PARAM
        _native = self._toNativeChannelList()
        retCode = STUHFL_native.Get_ChannelList(_native)
        self._setFromNativeChannelList(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: TuneChannel()   \n
    ## Tune itemList[channelIdx] with predefined class members falsePositiveDetection + persistent + antenna + algorithm
    ## Tune all frequencies if 'channelIdx' is not provided
    ##@param channelIdx: Channel index to which apply tuning 
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV TuneChannel(STUHFL_T_ST25RU3993_TuneCfg *tuneCfg);
    def tune(self, channelIdx=None):
        if channelIdx is not None:
            self.channelListIdx = channelIdx
            _native = self._toNativeTuneCfg(False)
        else:
            _native = self._toNativeTuneCfg(True)
        retCode = STUHFL_native.TuneChannel(_native)
        return retCode




#FREQUENCY_HOP_MODE
STUHFL_D_FREQUENCY_HOP_MODE_IGNORE_MIN   = 0
STUHFL_D_FREQUENCY_HOP_MODE_POWER_SAFE   = 1
STUHFL_D_FREQUENCY_HOP_MODE_FAST         = 2
STUHFL_D_FREQUENCY_HOP_MODE_FAIR         = 3    

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_FreqHop     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_FreqHop:
    ##
    ## @param maxSendingTime: Maximum sending time frequency hopping 
    ## @param minSendingTime: Minimum sending time before frequency hopping is performed 
    ## @param mode: Mode
    ##
    def __init__(self, maxSendingTime = 400, minSendingTime = 400, mode = STUHFL_D_FREQUENCY_HOP_MODE_IGNORE_MIN):
        # "public" members
        ## I/O Param: Maximum sending time before frequency hopping is performed. Minimum allowed value: 40ms
        self.maxSendingTime = maxSendingTime
        ## I/O Param: Minimum sending time before frequency hopping is performed
        self.minSendingTime = minSendingTime
        ## I/O Param: Hopping mode
        self.mode           = mode          

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_FreqHop()
        _native.maxSendingTime = self.maxSendingTime
        _native.minSendingTime = self.minSendingTime
        _native.mode           = self.mode          
        _native.rfu            = 0
        return _native

    def _setFromNative(self, _native):
        self.maxSendingTime = _native.maxSendingTime
        self.minSendingTime = _native.minSendingTime
        self.mode           = _native.mode          

    ## Maps STUHFL ANSI-C API: Set_FreqHop()   \n
    ## Set Freq hop with predefined class members maxSendingTime + minSendingTime + mode
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_FreqHop(STUHFL_T_ST25RU3993_FreqHop *freqHop);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_FreqHop(_native)
        return retCode
    
    ## Maps STUHFL ANSI-C API: Get_FreqHop()   \n
    ## Get Freq hop into class members maxSendingTime + minSendingTime + mode
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqHop(STUHFL_T_ST25RU3993_FreqHop *freqHop);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_FreqHop(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_FreqLBT     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_FreqLBT:
    ##
    ## @param listeningTime: Time for listing periode 
    ## @param idleTime: Idle time for LBT 
    ## @param rssiLogThreshold: RSSI threshold value 
    ## @param skipLBTcheck: Flag to wheter LBT check shall be skipped at all 
    ##
    def __init__(self, listeningTime = 1, idleTime = 0, rssiLogThreshold = 31, skipLBTcheck = True):
        # "public" members
        ## I/O Param: Time for listing periode 
        self.listeningTime    = listeningTime   
        ## I/O Param: Idle time for LBT 
        self.idleTime         = idleTime        
        ## I/O Param: RSSI threshold value 
        self.rssiLogThreshold = rssiLogThreshold
        ## I/O Param: Flag to wheter LBT check shall be skipped at all 
        self.skipLBTcheck     = skipLBTcheck    
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_FreqLBT()
        _native.listeningTime    = self.listeningTime   
        _native.idleTime         = self.idleTime        
        _native.rssiLogThreshold = self.rssiLogThreshold
        _native.skipLBTcheck     = self.skipLBTcheck    
        return _native

    def _setFromNative(self, _native):
        self.listeningTime    = _native.listeningTime   
        self.idleTime         = _native.idleTime        
        self.rssiLogThreshold = _native.rssiLogThreshold
        self.skipLBTcheck     = _native.skipLBTcheck    

    ## Maps STUHFL ANSI-C API: Set_FreqLBT()   \n
    ## Set Freq Lbt with predefined class members listeningTime + idleTime + rssiLogThreshold + skipLBTcheck
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_FreqLBT(STUHFL_T_ST25RU3993_FreqLBT *freqLBT);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_FreqLBT(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_FreqLBT()   \n
    ## Get Freq Lbt into class members listeningTime + idleTime + rssiLogThreshold + skipLBTcheck
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_FreqLBT(STUHFL_T_ST25RU3993_FreqLBT *freqLBT);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_FreqLBT(_native)
        self._setFromNative(_native)
        return retCode

#CONTINUOUS_MODULATION_MODE
STUHFL_D_CONTINUOUS_MODULATION_MODE_STATIC          = 0
STUHFL_D_CONTINUOUS_MODULATION_MODE_PSEUDO_RANDOM   = 1
STUHFL_D_CONTINUOUS_MODULATION_MODE_ETSI            = 2
STUHFL_D_CONTINUOUS_MODULATION_MODE_OFF             = 3

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_FreqContinuousModulation     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_FreqContinuousModulation:
    ##
    ## @param frequency: Frequency to be used for continuouse modulation 
    ## @param enable: Flag to enable or disable modulation 
    ## @param maxSendingTime: Maximum modulation time in ms. If zero the modulation will not stopped automatically 
    ## @param mode: Modulation mode 
    ##
    def __init__(self, frequency = STUHFL_native.STUHFL_D_DEFAULT_FREQUENCY, enable = False, maxSendingTime = 0, mode = STUHFL_D_CONTINUOUS_MODULATION_MODE_OFF):
        # "public" members
        ## I Param: Frequency to be used for continuouse modulation 
        self.frequency      = frequency     
        ## I Param: Flag to enable or disable modulation 
        self.enable  = enable 
        ## I Param: Maximum modulation time in ms. If zero the modulation will not stopped automatically. To stop a infite continuous modulation the command must be resend with enable flag set to false.
        self.maxSendingTime = maxSendingTime
        ## I Param: Modulation mode 
        self.mode = mode
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_FreqContinuousModulation()
        _native.frequency      = self.frequency     
        _native.enable  = self.enable 
        _native.maxSendingTime = self.maxSendingTime
        _native.mode = self.mode
        return _native

    def _setFromNative(self, _native):
        self.frequency      = _native.frequency     
        self.enable  = _native.enable 
        self.maxSendingTime = _native.maxSendingTime
        self.mode = _native.mode

    ## Maps STUHFL ANSI-C API: Set_FreqContinuousModulation()   \n
    ## Set Continuous mode with predefined class members frequency + enable + maxSendingTime + mode
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_FreqContinuousModulation(STUHFL_T_ST25RU3993_FreqContinuousModulation *continuousMod);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_FreqContinuousModulation(_native)
        return retCode

#TREXT_LEAD
STUHFL_D_TREXT_OFF         = False
STUHFL_D_TREXT_ON          = True 

#GEN2_TARI
STUHFL_D_GEN2_TARI_6_25      = 0 
STUHFL_D_GEN2_TARI_12_50     = 1 
STUHFL_D_GEN2_TARI_25_00     = 2 

#GEN2_BLF
STUHFL_D_GEN2_BLF_40       = 0 
STUHFL_D_GEN2_BLF_160      = 6 
STUHFL_D_GEN2_BLF_213      = 8 
STUHFL_D_GEN2_BLF_256      = 9 
STUHFL_D_GEN2_BLF_320      = 12
STUHFL_D_GEN2_BLF_640      = 15

#GEN2_COD
STUHFL_D_GEN2_CODING_FM0         = 0 
STUHFL_D_GEN2_CODING_MILLER2     = 1 
STUHFL_D_GEN2_CODING_MILLER4     = 2 
STUHFL_D_GEN2_CODING_MILLER8     = 3

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gen2_ProtocolCfg     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gen2_ProtocolCfg:
    ##
    ## @param tari: Tari setting 
    ## @param blf: Link frequency (STUHFL_D_GEN2_BLF_40, ...)
    ## @param coding: Coding (STUHFL_D_GEN2_CODING_FM0, ...) 
    ## @param trext: ON if the preamble is long, i.e. with pilot tone 
    ##
    def __init__(self, tari = STUHFL_D_GEN2_TARI_25_00, blf = STUHFL_D_GEN2_BLF_256, coding = STUHFL_D_GEN2_CODING_MILLER8, trext = STUHFL_D_TREXT_ON):
        # "public" members
        ## I/O Param: Tari setting 
        self.tari        = tari  
        ## I/O Param: backscatter link frequency factor: STUHFL_D_GEN2_BLF_40, ...
        self.blf         = blf   
        ## I/O Param: Coding: STUHFL_D_GEN2_CODING_FM0, ...
        self.coding      = coding
        ## I/O Param: Usage of short or long preamble: ON if the preamble is long, i.e. with pilot tone */
        self.trext       = trext 

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gen2_ProtocolCfg()
        _native.tari   = self.tari       
        _native.blf    = self.blf        
        _native.coding = self.coding     
        _native.trext  = self.trext      
        return _native

    def _setFromNative(self, _native):
        self.tari        = _native.tari       
        self.blf         = _native.blf        
        self.coding      = _native.coding     
        self.trext       = _native.trext      

    ## Maps STUHFL ANSI-C API: Set_Gen2_ProtocolCfg()   \n
    ## Set Gen2 Protocol Cfg with predefined class members tari + blf + coding + trext
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_ProtocolCfg(STUHFL_T_ST25RU3993_Gen2_ProtocolCfg *protocolCfg);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gen2_ProtocolCfg(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gen2_ProtocolCfg()   \n
    ## Get Gen2 Protocol Cfg with predefined class members tari + blf + coding + trext
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_ProtocolCfg(STUHFL_T_ST25RU3993_Gen2_ProtocolCfg *protocolCfg);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gen2_ProtocolCfg(_native)
        self._setFromNative(_native)
        return retCode

#GB29768_TC
STUHFL_D_GB29768_TC_6_25      = 0 
STUHFL_D_GB29768_TC_12_50     = 1 

#GB29768_BLF
STUHFL_D_GB29768_BLF_64      = 0
STUHFL_D_GB29768_BLF_137     = 1
STUHFL_D_GB29768_BLF_174     = 2
STUHFL_D_GB29768_BLF_320     = 3
STUHFL_D_GB29768_BLF_128     = 4
STUHFL_D_GB29768_BLF_274     = 5
STUHFL_D_GB29768_BLF_349     = 6
STUHFL_D_GB29768_BLF_640     = 7

#GB29768_COD
STUHFL_D_GB29768_CODING_FM0         = 0 
STUHFL_D_GB29768_CODING_MILLER2     = 1 
STUHFL_D_GB29768_CODING_MILLER4     = 2 
STUHFL_D_GB29768_CODING_MILLER8     = 3

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg:
    ##
    ## @param tc: TC value (STUHFL_D_GB29768_TC_12_5, STUHFL_D_GB29768_TC_6_25) 
    ## @param blf: backscatter link frequency factor 
    ## @param coding: coding mode (STUHFL_D_GB29768_CODING_FM0, STUHFL_D_GB29768_CODING_MILLER2, ...) 
    ## @param trext: ON if the lead code is sent, OFF otherwise 
    ##
    def __init__(self, tc = STUHFL_D_GB29768_TC_12_50, blf = STUHFL_D_GB29768_BLF_320, coding = STUHFL_D_GB29768_CODING_MILLER2, trext = STUHFL_D_TREXT_ON):
        # "public" members
        ## I/O Param: Usage of short or long preamble: ON if the lead code is sent, false otherwise
        self.trext     = trext 
        ## I/O Param: backscatter link frequency factor 
        self.blf       = blf   
        ## I/O Param: Coding: STUHFL_D_GB29768_CODING.FM0, STUHFL_D_GB29768_CODING.MILLER2, ...
        self.coding    = coding
        ## I/O Param: Refernce time of forward link: STUHFL_D_GB29768_TC.TC_12_5, STUHFL_D_GB29768_TC.TC_6_25
        self.tc        = tc  
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg()
        _native.tc     = self.tc       
        _native.blf    = self.blf        
        _native.coding = self.coding     
        _native.trext  = self.trext      
        return _native

    def _setFromNative(self, _native):
        self.tc        = _native.tc       
        self.blf       = _native.blf        
        self.coding    = _native.coding     
        self.trext     = _native.trext      

    ## Maps STUHFL ANSI-C API: Set_Gb29768_ProtocolCfg()   \n
    ## Set Gb29768 Protocol Cfg with predefined class members tc + blf + coding + trext
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gb29768_ProtocolCfg(STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg *protocolCfg);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gb29768_ProtocolCfg(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gb29768_ProtocolCfg()   \n
    ## Get Gb29768 Protocol Cfg with predefined class members tc + blf + coding + trext
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gb29768_ProtocolCfg(STUHFL_T_ST25RU3993_Gb29768_ProtocolCfg *protocolCfg);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gb29768_ProtocolCfg(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_TxRxCfg     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_TxRxCfg:
    ##
    ## @param txOutputLevel:               Tx output level. See Modulator control register 3 for further info. Range [0db..-19db] 
    ## @param rxSensitivity:               Rx sensitivity level. Range [+17dB..-19dB] 
    ## @param usedAntenna:                 Antenna to be used 
    ## @param alternateAntennaInterval:    Time in ms for alternating the antennas when alternating mode is used 
    ##
    def __init__(self, txOutputLevel = -2, rxSensitivity = 3, usedAntenna = STUHFL_D_ANTENNA_1, alternateAntennaInterval = 1):
        # "public" members
        ## I/O Param: Tx output level. See Modulator control register 3 for further info. Range [0db..-19db] 
        self.txOutputLevel               = txOutputLevel           
        ## I/O Param: Rx sensitivity level. Range [+17dB..-19dB] 
        self.rxSensitivity               = rxSensitivity           
        ## I/O Param: Antenna to be used 
        self.usedAntenna                 = usedAntenna             
        ## I/O Param: Time in ms for alternating the antennas when alternating mode is used 
        self.alternateAntennaInterval    = alternateAntennaInterval
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_TxRxCfg()
        _native.txOutputLevel            = self.txOutputLevel            
        _native.rxSensitivity            = self.rxSensitivity              
        _native.usedAntenna              = self.usedAntenna                
        _native.alternateAntennaInterval = self.alternateAntennaInterval   
        _native.rfu                      = 3                       
        return _native

    def _setFromNative(self, _native):
        self.txOutputLevel               = _native.txOutputLevel           
        self.rxSensitivity               = _native.rxSensitivity            
        self.usedAntenna                 = _native.usedAntenna              
        self.alternateAntennaInterval    = _native.alternateAntennaInterval 

    ## Maps STUHFL ANSI-C API: Set_TxRxCfg()   \n
    ## Set TxRx Cfg with predefined class members txOutputLevel + rxSensitivity + usedAntenna + alternateAntennaInterval
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_TxRxCfg(STUHFL_T_ST25RU3993_TxRxCfg *txRxCfg);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_TxRxCfg(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_TxRxCfg()   \n
    ## Get TxRx Cfg with predefined class members txOutputLevel + rxSensitivity + usedAntenna + alternateAntennaInterval
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_TxRxCfg(STUHFL_T_ST25RU3993_TxRxCfg *txRxCfg);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_TxRxCfg(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_PowerAmplifierCfg     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_PowerAmplifierCfg:
        ##
        ## @param external: Use external Power Amplifier 
        ##
    def __init__(self, external = True):
        # "public" members
        ## I/O Param: Force usage of external power amplifier. If 'false' internal PA is used */
        self.external     = external 
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_PowerAmplifierCfg()
        _native.external     = self.external       
        return _native

    def _setFromNative(self, _native):
        self.external     = _native.external      

    ## Maps STUHFL ANSI-C API: Set_PowerAmplifierCfg()   \n
    ## Set PA Cfg with predefined class members external
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_PowerAmplifierCfg(STUHFL_T_ST25RU3993_PowerAmplifierCfg *PowerAmplifierCfg);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_PowerAmplifierCfg(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_PowerAmplifierCfg()   \n
    ## Get PA Cfg with predefined class members external
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_PowerAmplifierCfg(STUHFL_T_ST25RU3993_PowerAmplifierCfg *PowerAmplifierCfg);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_PowerAmplifierCfg(_native)
        self._setFromNative(_native)
        return retCode

#GEN2_SESSION
STUHFL_D_GEN2_SESSION_S0  = 0 
STUHFL_D_GEN2_SESSION_S1  = 1
STUHFL_D_GEN2_SESSION_S2  = 2 
STUHFL_D_GEN2_SESSION_S3  = 3 

#GEN2_TARGET
STUHFL_D_GEN2_TARGET_A = 0 
STUHFL_D_GEN2_TARGET_B = 1 

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_AutoTuning
class STUHFL_T_ST25RU3993_AutoTuning:
    def __init__(self, autoTuningInterval, autoTuningLevel, autoTuningAlgo, falsePositiveDetection):
        ## I/O Param: Auto tuning check interval (in inventory rounds)
        self.interval               = autoTuningInterval
        ## I/O Param: Deviation level for retuning in percentage 
        self.level                  = autoTuningLevel
        ## I/O Param: Algorithm used for automatic (re)tuning.  
        self.algorithm              = autoTuningAlgo
        ## I/O Param: Do false Positive Detection check.  
        self.falsePositiveDetection = falsePositiveDetection

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_AutoTuning()
        _native.interval                 = self.interval            
        _native.level                    = self.level               
        _native.algorithm                = self.algorithm
        _native.falsePositiveDetection   = self.falsePositiveDetection
        return _native

    def _setFromNative(self, _native):
        self.interval                    = _native.interval
        self.level                       = _native.level               
        self.algorithm                   = _native.algorithm                
        self.falsePositiveDetection      = _native.falsePositiveDetection                

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_AdaptiveSensitivity
class STUHFL_T_ST25RU3993_AdaptiveSensitivity:
    def __init__(self, adaptiveSensitivityInterval, adaptiveSensitivityEnable):
        ## I/O Param: Adaptive sensitivity interval (in inventory rounds)
        self.interval      = adaptiveSensitivityInterval
        ## I/O Param: Flag to enable automatic sensitivity adjustment 
        self.enable        = adaptiveSensitivityEnable

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_AdaptiveSensitivity()
        _native.interval        = self.interval   
        _native.enable          = self.enable     
        return _native

    def _setFromNative(self, _native):
        self.interval           = _native.interval   
        self.enable             = _native.enable 


## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gen2_InventoryOption
class STUHFL_T_ST25RU3993_Gen2_InventoryOption:
    def __init__(self, fastInv, autoAck, readTID):
        ## I/O Param: Fast Inventory enabling. If set to false normal inventory round will be performed, if set to true fast inventory rounds will be performed.
        self.fast                          = fastInv                       
        ## I/O Param: Automatic Ack enabling. If set to false inventory round commands will be triggered by the FW, otherwise the autoACK feature of the reader will be used which sends the required Gen2 commands automatically.
        self.autoAck                          = autoAck                       
        ## I/O Param: read TID enabling.  If set to true an read of the TID will be performed in inventory rounds.
        self.readTID                          = readTID                       

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gen2_InventoryOption()
        _native.fast                  = self.fast                       
        _native.autoAck               = self.autoAck                       
        _native.readTID               = self.readTID                       
        return _native

    def _setFromNative(self, _native):
        self.fast                     = _native.fast                       
        self.autoAck                  = _native.autoAck                       
        self.readTID                  = _native.readTID                       

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gen2_Anticollision
class STUHFL_T_ST25RU3993_Gen2_Anticollision:
    def __init__(self, adaptiveQEnable, startQ, minQ, maxQ, adjustOptions, C1, C2):
        ## I/O Param: Flag to enable automatic Q adaption 
        self.adaptiveQ                          = adaptiveQEnable               
        ## I/O Param: Q starting value 
        self.startQ                             = startQ                        
        ## I/O Param: Minimum value that Q could reach 
        self.minQ                               = minQ                          
        ## I/O Param: Maximum value that Q could reach. If value exceeds 15 it is truncated to 15. 
        self.maxQ                               = maxQ                          
        ## I/O Param: Q algorithm options. Bitfield to define additional anticollision options (STUHFL_D_USE_QUERY_ADJUST_NIC, STUHFL_D_SINGLE_ADJUST, STUHFL_D_USE_CEIL_FLOOR, STUHFL_D_RESET_Q_AFTER_ROUND)
        self.options                            = adjustOptions                 
        ## I/O Param: Q algorithm C1 values for each Q 
        self.C1                                 = C1                          
        ## I/O Param: Q algorithm C2 values for each Q 
        self.C2                                 = C2                          

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gen2_Anticollision()
        _native.startQ                = self.startQ                        
        _native.adaptiveQ             = self.adaptiveQ               
        _native.minQ                  = self.minQ                          
        _native.maxQ                  = self.maxQ                          
        _native.options               = self.options                 
        for i, C1 in enumerate(self.C1):
            _native.C1[i] = C1
        for i, C2 in enumerate(self.C2):
            _native.C2[i] = C2
        return _native

    def _setFromNative(self, _native):
        self.startQ                   = _native.startQ                        
        self.adaptiveQ                = _native.adaptiveQ               
        self.minQ                     = _native.minQ                          
        self.maxQ                     = _native.maxQ                          
        self.options                  = _native.options                 
        self.C1                       = [_native.C1[i] for i in range(STUHFL_native.STUHFL_D_NB_C_VALUES)]
        self.C2                       = [_native.C2[i] for i in range(STUHFL_native.STUHFL_D_NB_C_VALUES)]

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gen2_QueryParams
class STUHFL_T_ST25RU3993_Gen2_QueryParams:
    def __init__(self, sel, session, target, toggleTarget, targetDepletionMode):
         ## I/O Param: QUERY command Sel field
        self.sel                              = sel                           
        ## I/O Param: Query session information: STUHFL_D_GEN2_SESSION_S0, ...
        self.session                          = session                       
        ## I/O Param: QUERY target field
        self.target                           = target                        
        ## I/O Param: Toggle between Target A and B
        self.toggleTarget                     = toggleTarget                  
        ## I/O Param: If set to true and the target shall be toggled in inventory an additional inventory round before the target is toggled will be executed. This gives "weak" transponders an additional chance to reply.
        self.targetDepletionMode              = targetDepletionMode           

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gen2_QueryParams()
        _native.sel                     = self.sel                           
        _native.session                 = self.session                       
        _native.target                  = self.target                        
        _native.toggleTarget            = self.toggleTarget                  
        _native.targetDepletionMode     = self.targetDepletionMode           
        return _native

    def _setFromNative(self, _native):
        self.sel                        = _native.sel                           
        self.session                    = _native.session                       
        self.target                     = _native.target                        
        self.toggleTarget               = _native.toggleTarget                  
        self.targetDepletionMode        = _native.targetDepletionMode           

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gen2_InventoryCfg     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gen2_InventoryCfg:
    ##
    ## @param fastInv: Fast Inventory enabling. If set to 0 normal inventory round will be performed, if set to 1 fast inventory rounds will be performed.
    ## @param autoAck:                        Automatic Ack enabling. If set to 0 inventory round commands will be triggered by the FW, otherwise the autoACK feature of the reader will be used which sends the required Gen2 commands automatically.
    ## @param readTID: read TID enabling.  If set to 1, read of the TID will be performed in inventory rounds.
    ## @param startQ: Q starting value 
    ## @param adaptiveQEnable: Flag to enable automatic Q adaption 
    ## @param minQ: Minimum value that Q could reach 
    ## @param maxQ: Maximum value that Q could reach. If value exceeds 15 it is truncated to 15. 
    ## @param adjustOptions: Q algorithm options 
    ## @param C2: Q algorithm C2 values for each Q
    ## @param C1: Q algorithm C1 values for each Q
    ## @param autoTuningInterval: Auto tuning check interval (in inventory rounds)
    ## @param autoTuningLevel: Deviation level for retuning in percentage 
    ## @param autoTuningAlgo: Algorithm used for automatic (re)tuning. 
    ## @param falsePositiveDetection: Do false Positive Detection check 
    ## @param sel: For QUERY Sel field
    ## @param session: STUHFL_D_GEN2_SESSION_S0, ... 
    ## @param target: For QUERY Target field 
    ## @param toggleTarget: Toggle between Target A and B 
    ## @param targetDepletionMode: If set to 1 and the target shall be toggled in inventory an additional inventory round before the target is toggled will be executed. This gives "weak" transponders an additional chance to reply. 
    ## @param adaptiveSensitivityInterval: Adaptive sensitivity interval (in inventory rounds)
    ## @param adaptiveSensitivityEnable: Flag to enable automatic sensitivity adjustment 
    ##
    def __init__(self, fastInv = True, autoAck = False, readTID = False, 
                        adaptiveQEnable = True, startQ = 4, minQ = 0, maxQ = 15, adjustOptions = 0, C1 = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15], C2 = [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35],
                        autoTuningInterval = 7, autoTuningLevel = 20, autoTuningAlgo = STUHFL_D_TUNING_ALGO_FAST, falsePositiveDetection=False,
                        sel = 0, session = STUHFL_D_GEN2_SESSION_S0, target = STUHFL_D_GEN2_TARGET_A, toggleTarget = True, targetDepletionMode = False, 
                        adaptiveSensitivityInterval = 5, adaptiveSensitivityEnable = False):
        self.inventoryOption       = STUHFL_T_ST25RU3993_Gen2_InventoryOption(fastInv, autoAck, readTID)
        self.antiCollision          = STUHFL_T_ST25RU3993_Gen2_Anticollision(adaptiveQEnable, startQ, minQ, maxQ, adjustOptions, C1, C2)                        
        self.autoTuning             = STUHFL_T_ST25RU3993_AutoTuning(autoTuningInterval, autoTuningLevel, autoTuningAlgo, falsePositiveDetection)                
        self.queryParams            = STUHFL_T_ST25RU3993_Gen2_QueryParams(sel, session, target, toggleTarget, targetDepletionMode)
        self.adaptiveSensitivity    = STUHFL_T_ST25RU3993_AdaptiveSensitivity(adaptiveSensitivityInterval, adaptiveSensitivityEnable)   

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gen2_InventoryCfg()
        _native.inventoryOption           = self.inventoryOption._toNative()
        _native.antiCollision              = self.antiCollision._toNative()                        
        _native.autoTuning                 = self.autoTuning._toNative()            
        _native.queryParams                = self.queryParams._toNative()                           
        _native.adaptiveSensitivity        = self.adaptiveSensitivity._toNative()   
        return _native

    def _setFromNative(self, _native):
        self.inventoryOption._setFromNative(_native.inventoryOption)                       
        self.antiCollision._setFromNative(_native.antiCollision)
        self.autoTuning._setFromNative(_native.autoTuning)
        self.queryParams._setFromNative(_native.queryParams)
        self.adaptiveSensitivity._setFromNative(_native.adaptiveSensitivity)

    ## Maps STUHFL ANSI-C API: Set_Gen2_InventoryCfg()   \n
    ## Set Gen2 Inventory Cfg with all predefined class members
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_InventoryCfg(STUHFL_T_ST25RU3993_Gen2_InventoryCfg *inventoryCfg);
    def commit(self):
        if len(self.antiCollision.C1) != STUHFL_native.STUHFL_D_NB_C_VALUES:
            print('antiCollision.C1 must contain {} values..'.format(STUHFL_native.STUHFL_D_NB_C_VALUES))
            return STUHFL_ERR_PARAM
        if len(self.antiCollision.C2) != STUHFL_native.STUHFL_D_NB_C_VALUES:
            print('antiCollision.C2 must contain {} values..'.format(STUHFL_native.STUHFL_D_NB_C_VALUES))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gen2_InventoryCfg(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gen2_InventoryCfg()   \n
    ## Get Gen2 Inventory Cfg with all predefined class members
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_InventoryCfg(STUHFL_T_ST25RU3993_Gen2_InventoryCfg *inventoryCfg);
    def fetch(self):
        if len(self.antiCollision.C1) != STUHFL_native.STUHFL_D_NB_C_VALUES:
            print('antiCollision.C1 must contain {} values..'.format(STUHFL_native.STUHFL_D_NB_C_VALUES))
            return STUHFL_ERR_PARAM
        if len(self.antiCollision.C2) != STUHFL_native.STUHFL_D_NB_C_VALUES:
            print('antiCollision.C2 must contain {} values..'.format(STUHFL_native.STUHFL_D_NB_C_VALUES))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gen2_InventoryCfg(_native)
        self._setFromNative(_native)
        return retCode

#GB29768_CONDITION
STUHFL_D_GB29768_CONDITION_ALL = 0 
STUHFL_D_GB29768_CONDITION_FLAG1 = 1 
STUHFL_D_GB29768_CONDITION_FLAG0 = 1 

#GB29768_SESSION
STUHFL_D_GB29768_SESSION_S0 = 0 
STUHFL_D_GB29768_SESSION_S1 = 1 
STUHFL_D_GB29768_SESSION_S2 = 2 
STUHFL_D_GB29768_SESSION_S3 = 3 

#GB29768_TARGET
STUHFL_D_GB29768_TARGET_0 = 0 
STUHFL_D_GB29768_TARGET_1 = 1 

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gb29768_QueryParams
class STUHFL_T_ST25RU3993_Gb29768_QueryParams:
    def __init__(self, condition, session, target, toggleTarget, targetDepletionMode):
        ## I/O Param: QUERY command condition field
        self.condition                        = condition
        ## I/O Param: Query session information: STUHFL_D_GB29768_SESSION_S0, ...
        self.session                          = session                       
        ## I/O Param: QUERY target field
        self.target                           = target                        
        ## I/O Param: Toggle between Target 0 and 1
        self.toggleTarget                     = toggleTarget                  
        ## I/O Param: If set to true and the target shall be toggled in inventory an additional inventory round before the target is toggled will be executed. This gives "weak" transponders an additional chance to reply.
        self.targetDepletionMode              = targetDepletionMode           

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gb29768_QueryParams()
        _native.condition                   = self.condition            
        _native.session                     = self.session            
        _native.target                      = self.target            
        _native.toggleTarget                = self.toggleTarget            
        _native.targetDepletionMode         = self.targetDepletionMode            
        return _native

    def _setFromNative(self, _native):
        self.condition                      = _native.condition
        self.session                        = _native.session
        self.target                         = _native.target
        self.toggleTarget                   = _native.toggleTarget
        self.targetDepletionMode            = _native.targetDepletionMode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gb29768_Anticollision
class STUHFL_T_ST25RU3993_Gb29768_Anticollision:
    def __init__(self, endThreshold, ccnThreshold, cinThreshold):
        ## I/O Param: GBT anticollision END threshold parameter.
        self.endThreshold                     = endThreshold
        ## I/O Param: GBT anticollision CCN threshold parameter.
        self.ccnThreshold                     = ccnThreshold
        ## I/O Param: GBT anticollision CIN threshold parameter.
        self.cinThreshold                     = cinThreshold

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gb29768_Anticollision()
        _native.endThreshold                 = self.endThreshold            
        _native.ccnThreshold                 = self.ccnThreshold            
        _native.cinThreshold                 = self.cinThreshold            
        return _native

    def _setFromNative(self, _native):
        self.endThreshold                    = _native.endThreshold
        self.ccnThreshold                    = _native.ccnThreshold
        self.cinThreshold                    = _native.cinThreshold

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gb29768_InventoryOption
class STUHFL_T_ST25RU3993_Gb29768_InventoryOption:
    def __init__(self, readTID):
        ## I/O Param: read TID enabling.  If set to true, a read of the TID will be performed in inventory rounds.
        self.readTID                          = readTID

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gb29768_InventoryOption()
        _native.readTID                 = self.readTID            
        return _native

    def _setFromNative(self, _native):
        self.readTID                    = _native.readTID

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gb29768_InventoryCfg     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gb29768_InventoryCfg:
    ## 
    ## @param autoTuningInterval: Auto tuning check interval (in inventory rounds)
    ## @param autoTuningLevel: Deviation level for retuning in percentage 
    ## @param autoTuningAlgo: Algorithm used for automatic (re)tuning. 
    ## @param falsePositiveDetection: Do false Positive Detection check 
    ## @param adaptiveSensitivityInterval: Adaptive sensitivity interval (in inventory rounds)
    ## @param adaptiveSensitivityEnable: Flag to enable automatic sensitivity adjustment 
    ## @param condition: Condition setting 
    ## @param session: STUHFL_D_GB29768_SESSION_S0, ... 
    ## @param target: For QUERY Target field 
    ## @param toggleTarget: Target A/B toggle 
    ## @param targetDepletionMode: If TRUE and the target shall be toggled in inventory an additional inventory round before the target is toggled will be executed. This gives "weak" transponders an additional chance to reply. 
    ## @param endThreshold: GBT anticollision end threshold parameter.
    ## @param ccnThreshold: GBT anticollision CCN threshold parameter.
    ## @param cinThreshold: GBT anticollision CIN threshold parameter.
    ## @param readTID: read TID enabling.  If set to 1, read of the TID will be performed in inventory rounds.
    ## 
    def __init__(self, autoTuningInterval = 7, autoTuningLevel = 20, autoTuningAlgo = STUHFL_D_TUNING_ALGO_FAST, falsePositiveDetection=False, 
                        condition = STUHFL_D_GB29768_CONDITION_ALL, session = STUHFL_D_GB29768_SESSION_S0, target = STUHFL_D_GB29768_TARGET_0, toggleTarget = True, targetDepletionMode = False, 
                        adaptiveSensitivityInterval = 5, adaptiveSensitivityEnable = False,
                        endThreshold = 2, ccnThreshold = 3, cinThreshold = 4,
                        readTID = False):
        self.inventoryOption       = STUHFL_T_ST25RU3993_Gb29768_InventoryOption(readTID)
        self.antiCollision          = STUHFL_T_ST25RU3993_Gb29768_Anticollision(endThreshold, ccnThreshold, cinThreshold)
        self.autoTuning             = STUHFL_T_ST25RU3993_AutoTuning(autoTuningInterval, autoTuningLevel, autoTuningAlgo, falsePositiveDetection)                
        self.queryParams            = STUHFL_T_ST25RU3993_Gb29768_QueryParams(condition, session, target, toggleTarget, targetDepletionMode)
        self.adaptiveSensitivity    = STUHFL_T_ST25RU3993_AdaptiveSensitivity(adaptiveSensitivityInterval, adaptiveSensitivityEnable)   

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gb29768_InventoryCfg()
        _native.inventoryOption           = self.inventoryOption._toNative()
        _native.antiCollision              = self.antiCollision._toNative()                        
        _native.autoTuning                 = self.autoTuning._toNative()            
        _native.queryParams                = self.queryParams._toNative()                           
        _native.adaptiveSensitivity        = self.adaptiveSensitivity._toNative()   
        return _native

    def _setFromNative(self, _native):
        self.inventoryOption._setFromNative(_native.inventoryOption)                       
        self.antiCollision._setFromNative(_native.antiCollision)
        self.autoTuning._setFromNative(_native.autoTuning)
        self.queryParams._setFromNative(_native.queryParams)
        self.adaptiveSensitivity._setFromNative(_native.adaptiveSensitivity)

    ## Maps STUHFL ANSI-C API: Set_Gb29768_InventoryCfg()   \n
    ## Set Gb29768 Inventory Cfg with all predefined class members
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gb29768_InventoryCfg(STUHFL_T_ST25RU3993_Gb29768_InventoryCfg *inventoryCfg);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gb29768_InventoryCfg(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gb29768_InventoryCfg()   \n
    ## Get Gb29768 Inventory Cfg with all predefined class members
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gb29768_InventoryCfg(STUHFL_T_ST25RU3993_Gb29768_InventoryCfg *inventoryCfg);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gb29768_InventoryCfg(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_RxFilter for Gen2 tags     \n
##  and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gen2_RxFilter:
    ##
    ##  @param blf: Link Frequency for which filter value shall be applied
    ##  @param coding: Coding for which filter value shall be applied
    ##  @param value: RX filter value
    ##
    def __init__(self, blf = STUHFL_D_GEN2_BLF_256, coding = STUHFL_D_GEN2_CODING_MILLER8, value = 0x34):
        # "public" members
        ## I Param: Link Frequency for which filter value shall be applied
        self.blf      = blf
        ## I Param: Coding for which filter value shall be applied
        self.coding   = coding
        ## I/O Param: RX filter value 
        self.value = value
   
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_RxFilter()
        _native.blf       = self.blf   
        _native.coding    = self.coding
        _native.value     = self.value 
        return _native

    def _setFromNative(self, _native):
        self.blf    = _native.blf   
        self.coding = _native.coding
        self.value  = _native.value 

    ## Maps STUHFL ANSI-C API: Set_Gen2_RxFilter()   \n
    ## Set Rx Filter calibration with predefined class members blf + coding + value
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gen2_RxFilter(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gen2_RxFilter()   \n
    ## Get Rx Filter calibration 
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gen2_RxFilter(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_RxFilter for Gb29768 tags     \n
##  and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gb29768_RxFilter:
    ##
    ##  @param blf: Link Frequency for which filter value shall be applied
    ##  @param coding: Coding for which filter value shall be applied
    ##  @param value: RX filter value
    ##
    def __init__(self, blf = STUHFL_D_GB29768_BLF_320, coding = STUHFL_D_GB29768_CODING_MILLER8, value = 0x2B):
        # "public" members
        ## I Param: Link Frequency for which filter value shall be applied
        self.blf      = blf
        ## I Param: Coding for which filter value shall be applied
        self.coding   = coding
        ## I/O Param: RX filter value 
        self.value = value
   
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_RxFilter()
        _native.blf       = self.blf   
        _native.coding    = self.coding
        _native.value     = self.value 
        return _native

    def _setFromNative(self, _native):
        self.blf    = _native.blf   
        self.coding = _native.coding
        self.value  = _native.value 

    ## Maps STUHFL ANSI-C API: Set_Gb29768_RxFilter()   \n
    ## Set Rx Filter calibration with predefined class members blf + coding + value
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gb29768_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gb29768_RxFilter(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gb29768_RxFilter()   \n
    ## Get Rx Filter calibration 
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gb29768_RxFilter(STUHFL_T_ST25RU3993_RxFilter *rxFilter);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gb29768_RxFilter(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_FilterCalibration for Gen2 tags    \n
##  and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gen2_FilterCalibration:
    ##
    ##  @param blf: Link Frequency for which highPass/lowPass values shall be applied
    ##  @param coding: Coding for which highPass/lowPass values shall be applied
    ##  @param highPass: High pass filter value. Range [0..15]. Step size = 4%
    ##  @param lowPass: Low pass filter value. Range [0..15]. Step size = 4%
    ##
    def __init__(self, blf = STUHFL_D_GEN2_BLF_256, coding = STUHFL_D_GEN2_CODING_MILLER8, highPass = 0x08, lowPass = 0x08):
        # "public" members
        ## I Param: Link Frequency for which highPass/lowPass values shall be applied
        self.blf      = blf
        ## I Param: Coding for which highPass/lowPass values shall be applied
        self.coding   = coding
        ## I/O Param: High pass filter value. Range [0..15]. Step size = 4%
        self.highPass = highPass
        ## I/O Param: Low pass filter value. Range [0..15]. Step size = 4%
        self.lowPass = lowPass
   
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_FilterCalibration()
        _native.blf       = self.blf   
        _native.coding    = self.coding
        _native.highPass        = self.highPass
        _native.lowPass        = self.lowPass
        return _native

    def _setFromNative(self, _native):
        self.blf        = _native.blf   
        self.coding     = _native.coding
        self.highPass         = _native.highPass
        self.lowPass         = _native.lowPass

    ## Maps STUHFL ANSI-C API: Set_Gen2_FilterCalibration()   \n
    ## Set Rx Filter calibration with predefined class members blf + coding + highPass + lowPass
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gen2_FilterCalibration(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gen2_FilterCalibration()   \n
    ## Get Rx Filter calibration 
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gen2_FilterCalibration(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gb29768_FilterCalibration for Gb29768 tags     \n
##  and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gb29768_FilterCalibration:
    ##
    ##  @param blf: Link Frequency for which highPass/lowPass values shall be applied
    ##  @param coding: Coding for which highPass/lowPass values shall be applied
    ##  @param highPass: High pass filter value. Range [0..15]. Step size = 4%
    ##  @param lowPass: Low pass filter value. Range [0..15]. Step size = 4%
    ##
    def __init__(self, blf = STUHFL_D_GEN2_BLF_256, coding = STUHFL_D_GEN2_CODING_MILLER8, highPass = 0x08, lowPass = 0x08):
        # "public" members
        ## I Param: Link Frequency for which highPass/lowPass values shall be applied
        self.blf      = blf
        ## I Param: Coding for which highPass/lowPass values shall be applied
        self.coding   = coding
        ## I/O Param: High pass filter value. Range [0..15]. Step size = 4%
        self.highPass = highPass
        ## I/O Param: Low pass filter value. Range [0..15]. Step size = 4%
        self.lowPass = lowPass
   
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_FilterCalibration()
        _native.blf       = self.blf   
        _native.coding    = self.coding
        _native.highPass        = self.highPass
        _native.lowPass        = self.lowPass
        return _native

    def _setFromNative(self, _native):
        self.blf        = _native.blf   
        self.coding     = _native.coding
        self.highPass         = _native.highPass
        self.lowPass         = _native.lowPass

    ## Maps STUHFL ANSI-C API: Set_Gb29768_FilterCalibration()   \n
    ## Set Rx Filter calibration with predefined class members blf + coding + highPass + lowPass
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gb29768_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gb29768_FilterCalibration(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gb29768_FilterCalibration()   \n
    ## Get Rx Filter calibration 
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gb29768_FilterCalibration(STUHFL_T_ST25RU3993_FilterCalibration *fCal);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gb29768_FilterCalibration(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_ST25RU3993_Gen2_Timings     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_ST25RU3993_Gen2_Timings:
    ##
    ## @param T4Min: T4 minimum value in us. Default: T4Min = 0 .. Gen2: 2*3*Tari: 75us at TARI_12_50 
    ##
    def __init__(self, T4Min = 0):
        # "public" members
        ## I/O Param: T4 minimum value in us. Default: T4Min = 0 .. Gen2: 2*3*Tari: 75us at TARI_12_50 
        self.T4Min      = T4Min
    
    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_ST25RU3993_Gen2_Timings()
        _native.T4Min      = self.T4Min     
        return _native

    def _setFromNative(self, _native):
        self.T4Min      = _native.T4Min     

    ## Maps STUHFL ANSI-C API: Set_Gen2_Timings()   \n
    ## Set Gen2 Timing with predefined class members T4Min
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Set_Gen2_Timings(STUHFL_T_ST25RU3993_Gen2_Timings *gen2Timing);
    def commit(self):
        _native = self._toNative()
        retCode = STUHFL_native.Set_Gen2_Timings(_native)
        return retCode

    ## Maps STUHFL ANSI-C API: Get_Gen2_Timings()   \n
    ## Get Gen2 Timing with predefined class members T4Min
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Get_Gen2_Timings(STUHFL_T_ST25RU3993_Gen2_Timings *gen2Timing);
    def fetch(self):
        _native = self._toNative()
        retCode = STUHFL_native.Get_Gen2_Timings(_native)
        self._setFromNative(_native)
        return retCode

# endregion Configuration



# ---------------------------------------------------------------------------
# Gen2 
# ---------------------------------------------------------------------------
# region Gen2

#GEN2_SELECT_MODE
STUHFL_D_GEN2_SELECT_MODE_CLEAR_LIST             = 0
STUHFL_D_GEN2_SELECT_MODE_ADD2LIST               = 1
STUHFL_D_GEN2_SELECT_MODE_CLEAR_AND_ADD          = 2

#STUHFL_D_GEN2_SELECT_TARGET
STUHFL_D_GEN2_SELECT_TARGET_S0 = 0
STUHFL_D_GEN2_SELECT_TARGET_S1 = 1
STUHFL_D_GEN2_SELECT_TARGET_S2 = 2
STUHFL_D_GEN2_SELECT_TARGET_S3 = 3
STUHFL_D_GEN2_SELECT_TARGET_SL = 4

#GEN2_MEMORY_BANK
STUHFL_D_GEN2_MEMORY_BANK_RESERVED = 0
STUHFL_D_GEN2_MEMORY_BANK_EPC      = 1
STUHFL_D_GEN2_MEMORY_BANK_TID      = 2
STUHFL_D_GEN2_MEMORY_BANK_USER     = 3

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_Select     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_Select:
    ##
    ## @param mode: Select mode to be applied (CLEAR_LIST, ADD2LIST, CLEAR_AND_ADD). 
    ## @param target: indicates whether the select modifies a tag's SL flag or its inventoried flag. 
    ## @param action:  Elicit the tag behavior according to Gen2 Select specification. 
    ## @param memoryBank: Bank (File, EPC, TID, USER) on which apply the select. 
    ## @param mask: Selection mask. 
    ## @param maskBitLength: Mask length in bits. 
    ## @param maskBitPointer: Bit starting address to which mask is applied. 
    ## @param truncation: truncate enabling. 
    ##
    def __init__(self, mode = STUHFL_D_GEN2_SELECT_MODE_CLEAR_LIST, target = STUHFL_D_GEN2_SELECT_TARGET_S0, action = 0, memoryBank = STUHFL_D_GEN2_MEMORY_BANK_USER, mask = [], maskBitLength = 0, maskBitPointer = 0, truncation = False ):
        # "public" members
        ## I Param: Select mode to be applied (CLEAR_LIST, ADD2LIST, CLEAR_AND_ADD). 
        self.mode               = mode       
        ## I Param: indicates whether the select modifies a tag's SL flag or its inventoried flag. 
        self.target             = target     
        ## I Param: Elicit the tag behavior according to Gen2 Select specification. 
        self.action             = action     
        ## I Param: Bank (File, EPC, TID, USER) on which apply the select. 
        self.memoryBank            = memoryBank    
        ## I Param: Selection mask. 
        self.mask               = mask       
        ## I Param: Bit starting address to which mask is applied (bit address).
        self.maskBitPointer     = maskBitPointer
        ## I Param: Mask length in bits. 
        self.maskBitLength      = maskBitLength           # Mask Length in bits
        ## I Param: Truncate enabling. 
        self.truncation         = truncation 

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gen2_Select()
        _native.mode         = self.mode               
        _native.target       = self.target             
        _native.action       = self.action             
        _native.memoryBank      = self.memoryBank            
        _native.maskBitPointer  = self.maskBitPointer        
        _native.maskBitLength      = self.maskBitLength        
        _native.truncation   = self.truncation 
        for i, mask in enumerate(self.mask):
            _native.mask[i] = mask 
        return _native

    ## Maps STUHFL ANSI-C API: Gen2_Select()   \n
    ## Run Gen2 select with all predefined class members mode + target + action + memoryBank + mask + maskBitPointer + maskBitLength + truncation
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Select(STUHFL_T_Gen2_Select *gen2Select);
    def execute(self):
        if len(self.mask) > STUHFL_native.STUHFL_D_GEN2_MAX_SELECT_MASK_LENGTH:
            print('mask exceed max len of {} ..'.format(STUHFL_native.STUHFL_D_GEN2_MAX_SELECT_MASK_LENGTH))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_Select(_native)
        return retCode

#
class STUHFL_T_Read(ABC):
    ##
    ## @param wordPtr: Word address to which read data.
    ## @param memoryBank: Bank (File, EPC, TID, USER) to which read data. 
    ## @param numBytesToRead: Number of bytes to read. 
    ## @param pwd: Password. 
    ##
    def __init__(self, wordPtr = 0, memoryBank = STUHFL_D_GEN2_MEMORY_BANK_USER, numBytesToRead = 2, pwd = [0,0,0,0]):
        # "public" members
        ## I Param: Word address to which read data. 
        self.wordPtr    = wordPtr       
        ## I Param: Bank (File, EPC, TID, USER) to which read data. 
        self.memoryBank    = memoryBank       
        ## I Param: Number of bytes to read.
        self.numBytesToRead = numBytesToRead
        ## I Param: Password. 
        self.pwd        = pwd           
        ## O Param: Read data. 
        self.data       = []

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Read()
        _native.wordPtr    = self.wordPtr          
        _native.memoryBank    = self.memoryBank          
        _native.numBytesToRead = self.numBytesToRead       
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        _native.numReadBytes = 0
        return _native

    def _setFromNative(self, _native):
        self.wordPtr     = _native.wordPtr        
        self.memoryBank     = _native.memoryBank        
        self.numBytesToRead  = _native.numBytesToRead     
        self.pwd  = [_native.pwd[i]  for i in range(STUHFL_native.STUHFL_D_PASSWORD_LEN)]
        self.data = [_native.data[i] for i in range(_native.numReadBytes)]

    @abstractmethod
    def execute(self):
        return STUHFL_ERR_NONE

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_Read     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_Read(STUHFL_T_Read):
    ## Maps STUHFL ANSI-C API: Gen2_Read()   \n
    ## Run Gen2 read with predefined class members wordPtr + memoryBank + pwd + numBytesToRead and set read data into class member data
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Read(STUHFL_T_Gen2_Read *read);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_NB_C_VALUES))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_Read(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_Read    \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gb29768_Read(STUHFL_T_Read):
    ## Maps STUHFL ANSI-C API: Gb29768_Read()   \n
    ## Run Gb29768 read with predefined class members wordPtr + memoryBank + pwd + numBytesToRead and set read data into class member data
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Read(STUHFL_T_Gb29768_Read *read);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_NB_C_VALUES))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gb29768_Read(_native)
        self._setFromNative(_native)
        return retCode

#
class STUHFL_T_Write(ABC):
    ##
    ## @param wordPtr: Word address to which write data. 
    ## @param memoryBank: Bank (File, EPC, TID, USER) to which write data. 
    ## @param pwd: Password. 
    ## @param data: Data to be written (array of 2 bytes). 
    ##
    def __init__(self, wordPtr = 0, memoryBank = STUHFL_D_GEN2_MEMORY_BANK_USER, pwd = [0,0,0,0], data = [0,0]):
        # "public" members
        ## I Param: Word address to which write data. 
        self.wordPtr    = wordPtr       
        ## I Param: Bank (File, EPC, TID, USER) to which write data. 
        self.memoryBank    = memoryBank       
        ## I Param: Password. 
        self.pwd        = pwd           
        ## I Param: Data to be written (array of 2 bytes). 
        self.data       = data
        ## O Param: Tag reply. 
        self.tagReply   = 0             

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Write()
        _native.wordPtr    = self.wordPtr          
        _native.memoryBank    = self.memoryBank          
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        for i, data in enumerate(self.data):
            _native.data[i] = data 
        return _native

    def _setFromNative(self, _native):
        self.wordPtr    = _native.wordPtr          
        self.memoryBank    = _native.memoryBank          
        self.tagReply   = _native.tagReply
        self.pwd        = [_native.pwd[i]  for i in range(STUHFL_native.STUHFL_D_PASSWORD_LEN)]
        self.data       = [_native.data[i] for i in range(2)]

    @abstractmethod
    def execute(self):
        return STUHFL_ERR_NONE

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_Write     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_Write(STUHFL_T_Write):
    ## Maps STUHFL ANSI-C API: Gen2_Write()   \n
    ## Run Gen2 write with predefined class members wordPtr + memoryBank + pwd + data and set tag reply into class member tagReply
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Write(STUHFL_T_Gen2_Write *gen2Write);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        if len(self.data) != 2:
            print('Data must contain 2 bytes..')
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_Write(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Gb29768_Write     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gb29768_Write(STUHFL_T_Write):
    ## Maps STUHFL ANSI-C API: Gb29768_Write()   \n
    ## Run Gb29768 write with predefined class members wordPtr + memoryBank + pwd + data and set tag reply into class member tagReply
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Write(STUHFL_T_Gb29768_Write *gb29768Write);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        if len(self.data) != 2:
            print('Data must contain 2 bytes..')
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gb29768_Write(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_BlockWrite     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_BlockWrite:
    ##
    ## @param wordPtr: Word address to which write data.
    ## @param memoryBank: Bank (File, EPC, TID, USER) to which write data. 
    ## @param pwd: Password. 
    ## @param data: Data to be written (bytes array). 
    ##
    def __init__(self, wordPtr = 0, memoryBank = STUHFL_D_GEN2_MEMORY_BANK_USER, pwd = [0,0,0,0], data = [0,0]):
        # "public" members
        ## I Param: Word address to which write data. 
        self.wordPtr    = wordPtr       
        ## I Param: Bank (File, EPC, TID, USER) to which write data. 
        self.memoryBank    = memoryBank       
        ## I Param: Password. 
        self.pwd        = pwd           
        ## I Param: Data to be written (bytes array). 
        self.data       = data
        ## O Param: Tag reply. 
        self.tagReply   = 0             

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gen2_BlockWrite()
        _native.wordPtr    = self.wordPtr          
        _native.memoryBank    = self.memoryBank          
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        for i, data in enumerate(self.data):
            _native.data[i] = data 
        _native.numBytesToWrite = len(self.data)
        return _native

    def _setFromNative(self, _native):
        self.wordPtr    = _native.wordPtr          
        self.memoryBank    = _native.memoryBank          
        self.tagReply   = _native.tagReply
        self.pwd        = [_native.pwd[i]  for i in range(STUHFL_native.STUHFL_D_PASSWORD_LEN)]
        self.data       = [_native.data[i] for i in range(len(self.data))]

    ## Maps STUHFL ANSI-C API: Gen2_BlockWrite()   \n
    ## Block Write with predefined class members wordPtr + memoryBank + pwd + data and set tag reply into class member tagReply
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_BlockWrite(STUHFL_T_Gen2_BlockWrite *blockWrite);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        if len(self.data) > (STUHFL_native.STUHFL_D_MAX_BLOCKWRITE_DATA_LEN):
            print('max number of data({}) exceeded..'.format((STUHFL_native.STUHFL_D_MAX_BLOCKWRITE_DATA_LEN)))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_BlockWrite(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_Lock     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_Lock:
    ##
    ## @param mask: Mask and actions field.
    ## @param pwd: Password. 
    ##
    def __init__(self, mask = [0,0,0], pwd = [0,0,0,0]):
        # "public" members
        ## I Param: Mask and actions field. 
        self.mask       = mask      
        ## I Param: Password. 
        self.pwd        = pwd       
        ## O Param: Tag reply. 
        self.tagReply   = 0         

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gen2_Lock()
        for i, mask in enumerate(self.mask):
            _native.mask[i] = mask 
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        return _native

    def _setFromNative(self, _native):
        self.tagReply = _native.tagReply
        self.pwd        = [_native.pwd[i]  for i in range(STUHFL_native.STUHFL_D_PASSWORD_LEN)]
        self.mask       = [_native.mask[i] for i in range(len(self.mask))]

    ## Maps STUHFL ANSI-C API: Gen2_Lock()   \n
    ## Lock with predefined class members mask + pwd and set tag reply into class member tagReply
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Lock(STUHFL_T_Gen2_Lock *gen2Lock);
    def execute(self):
        if len(self.mask) != 3:
            print('MASK must contain 3 values..')
            return STUHFL_ERR_PARAM
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_Lock(_native)
        self._setFromNative(_native)
        return retCode

#
class STUHFL_T_Kill(ABC):
    def __init__(self, pwd = [0,0,0,0], recommission = 0):
        # "public" members
        ## I Param: Password. 
        self.pwd        = pwd       
        ## I Param: recommission. 
        self.recommission      = recommission
        ## O Param: Tag reply. 
        self.tagReply   = 0         

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Kill()
        _native.recommission       = self.recommission            
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        return _native

    def _setFromNative(self, _native):
        self.tagReply   = _native.tagReply
        self.recommission      = _native.recommission           
        self.pwd        = [_native.pwd[i]  for i in range(STUHFL_native.STUHFL_D_PASSWORD_LEN)]

    @abstractmethod
    def execute(self):
        return STUHFL_ERR_NONE

## Maps STUHFL ANSI-C structure: STUHFL_T_Kill for Gen2 tags     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_Kill(STUHFL_T_Kill):
    ## Maps STUHFL ANSI-C API: Gen2_Kill()   \n
    ## Run Gen2 kill with predefined class members pwd + recommission and set tag reply into class member tagReply
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_Kill(STUHFL_T_Kill *kill);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_Kill(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Kill for Gb29768 tags     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gb29768_Kill(STUHFL_T_Kill):
    ## Maps STUHFL ANSI-C API: Gb29768_Kill()   \n
    ## Run Gb29768 kill with predefined class members pwd + recommission and set tag reply into class member tagReply
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Kill(STUHFL_T_Kill *kill);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gb29768_Kill(_native)
        self._setFromNative(_native)
        return retCode

#GEN2_GENERIC_CMD
STUHFL_D_GEN2_GENERIC_CMD_CRC                   = 0x90
STUHFL_D_GEN2_GENERIC_CMD_CRC_EXPECT_HEAD       = 0x91
STUHFL_D_GEN2_GENERIC_CMD_NO_CRC                = 0x92

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_GenericCmd     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_GenericCmd:
    ##
    ## @param cmd: Generic command type
    ## @param noResponseTime: Tag response timeout. 
    ## @param expectedRcvDataBitLength: Size in bits of expected received data. NOTE: For the direct commands 0x90 and 0x91 (Tranmission with CRC) CRC is handled by HW and need not to be included into the expected bit count. The received CRC will also not replied to the host. When using command 0x92 handling of any data integrity checking must be done manually.
    ## @param sndDataBitLength: Size in bits of data sent to Tag. 
    ## @param appendRN16: Append tag handle to generic command. 
    ## @param sndData: Data being sent to Tag.
    ## @param pwd: Password. 
    ##
    def __init__(self, cmd = 0, noResponseTime = 0, expectedRcvDataBitLength = 0, sndDataBitLength = 0, appendRN16 = True, sndData = [], pwd = [0,0,0,0]):
        # "public" members
        ## I Param: Password. 
        self.pwd                   = pwd                    
        ## I Param: Generic command type. 
        self.cmd                   = cmd                    
        ## I Param: Tag response timeout. 
        self.noResponseTime        = noResponseTime         
        ## I Param: Size in bits of expected received data. NOTE: For the direct commands 0x90 and 0x91 (Tranmission with CRC) CRC is handled by HW and need not to be included into the expected bit count. The received CRC will also not replied to the host. When using command 0x92 handling of any data integrity checking must be done manually.
        self.expectedRcvDataBitLength = expectedRcvDataBitLength
        ## I Param: Size in bits of data sent to Tag. 
        self.sndDataBitLength         = sndDataBitLength          
        ## I Param: Append tag handle to generic command. 
        self.appendRN16            = appendRN16             
        ## I Param: Data being sent to Tag. 
        self.sndData               = sndData                
        ## O Param: Data received from Tag. 
        self.rcvData               = []

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gen2_GenericCmd()
        _native.cmd                   = self.cmd                           
        _native.noResponseTime        = self.noResponseTime                
        _native.expectedRcvDataBitLength = self.expectedRcvDataBitLength         
        _native.sndDataBitLength         = self.sndDataBitLength                 
        _native.appendRN16            = self.appendRN16  
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        for i, sndData in enumerate(self.sndData):
            _native.sndData[i] = sndData
        return _native

    def _setFromNative(self, _native):
        self.rcvData = [_native.rcvData[i] for i in range(_native.rcvDataLength)]

    ## Maps STUHFL ANSI-C API: Gen2_GenericCmd()   \n
    ## Run generic command with predefined class members pwd + cmd + noResponseTime + expectedRcvDataBitLength + sndDataBitLength + appendRN16 + sndData and set tag reply into class member rcvData
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_GenericCmd(STUHFL_T_Gen2_GenericCmd *generic);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        if len(self.sndData) > (STUHFL_native.STUHFL_D_GEN2_GENERIC_CMD_MAX_SND_DATA_BYTES):
            print('max number of data({}) exceeded..'.format(STUHFL_native.STUHFL_D_GEN2_GENERIC_CMD_MAX_SND_DATA_BYTES))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_GenericCmd(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Gen2_QueryMeasureRssi     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_QueryMeasureRssi:
    ##
    ## @param frequency: Frequency to which do measurement.
    ## @param measureCnt: Number of measures.
    ##
    def __init__(self, frequency = STUHFL_native.STUHFL_D_DEFAULT_FREQUENCY, measureCnt = 0):
        # "public" members
        ## I Param: Frequency to which do measurement. 
        self.frequency  = frequency     
        ## I Param: Frequency to which do measurement. 
        self.measureCnt = measureCnt
        ## O Param: AGC. 
        self.agc        = []
        ## O Param: RSSI log. 
        self.rssiLogI   = []
        ## O Param: RSSI log.         
        self.rssiLogQ   = []
        ## O Param: RSSI I Level. 
        self.rssiLinI   = []
        ## O Param: RSSI Q Level.         
        self.rssiLinQ   = []

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gen2_QueryMeasureRssi()
        _native.frequency  = self.frequency 
        _native.measureCnt = self.measureCnt
        return _native

    def _setFromNative(self, _native):
        self.agc      = [_native.agc     [i] for i in range(_native.measureCnt)]   
        self.rssiLogI = [_native.rssiLogI[i] for i in range(_native.measureCnt)]   
        self.rssiLogQ = [_native.rssiLogQ[i] for i in range(_native.measureCnt)]   
        self.rssiLinI = [_native.rssiLinI[i] for i in range(_native.measureCnt)]   
        self.rssiLinQ = [_native.rssiLinQ[i] for i in range(_native.measureCnt)]   

    ## Maps STUHFL ANSI-C API: Gen2_QueryMeasureRssi()   \n
    ## Run RSSI measure with predefined class members frequency + measureCnt and set result into class members agc + rssiLogI + rssiLogQ + rssiLinI + rssiLinQ
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gen2_QueryMeasureRssi(STUHFL_T_Gen2_QueryMeasureRssi *measureRssi);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gen2_QueryMeasureRssi(_native)
        self._setFromNative(_native)
        return retCode

# endregion Gen2



# ---------------------------------------------------------------------------
# GB29768
# ---------------------------------------------------------------------------
# region GB29768

#STUHFL_D_GB29768_SORT_MODE
STUHFL_D_GB29768_SORT_MODE_CLEAR_LIST             = 0
STUHFL_D_GB29768_SORT_MODE_ADD2LIST               = 1
STUHFL_D_GB29768_SORT_MODE_CLEAR_AND_ADD          = 2

#STUHFL_D_GB29768_SORT_TARGET
STUHFL_D_GB29768_SORT_TARGET_S0 = 0
STUHFL_D_GB29768_SORT_TARGET_S1 = 1
STUHFL_D_GB29768_SORT_TARGET_S2 = 2
STUHFL_D_GB29768_SORT_TARGET_S3 = 3
STUHFL_D_GB29768_SORT_TARGET_MATCHINGFLAG = 4

#GB29768_AREA
STUHFL_D_GB29768_AREA_TAGINFO  = 0x00
STUHFL_D_GB29768_AREA_CODING   = 0x10
STUHFL_D_GB29768_AREA_SECURITY = 0x20
STUHFL_D_GB29768_AREA_USER     = 0x30

#GB29768_RULE
STUHFL_D_GB29768_RULE_MATCH1_ELSE_0 = 0x00
STUHFL_D_GB29768_RULE_MATCHX_ELSE_0 = 0x01
STUHFL_D_GB29768_RULE_MATCH1_ELSE_X = 0x02
STUHFL_D_GB29768_RULE_MATCH0_ELSE_1 = 0x03

## Maps STUHFL ANSI-C structure: STUHFL_T_Gb29768_Sort     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gb29768_Sort:
    ##
    ## @param mode: Select mode to be applied (CLEAR_LIST, ADD2LIST, CLEAR_AND_ADD). 
    ## @param target: indicates whether the select modifies a tag's match flag or its inventoried flag. 
    ## @param rule: Elicit the tag behavior according to Gb29768 Sort specification. Nota: the rule STUHFL_D_GB29768_RULE_MATCH0_ELSE_1 (0x03) is to be used to invert selection. 
    ## @param memoryBank: Bank (TagInfo, Coding, Security, User) on which apply the sort. 
    ## @param mask: Selection mask.
    ## @param maskBitPointer: Bit starting address to which mask is applied (bit address). 
    ## @param maskBitLength: Mask length (in bits). 
    ##
    def __init__(self, mode = STUHFL_D_GB29768_SORT_MODE_CLEAR_LIST, target = STUHFL_D_GB29768_SORT_TARGET_S0, rule = 0, memoryBank = STUHFL_D_GB29768_AREA_USER, mask = [], maskBitPointer = 0, maskBitLength = 0 ):
        # "public" members
        ## I Param: Select mode to be applied (CLEAR_LIST, ADD2LIST, CLEAR_AND_ADD). 
        self.mode           = mode          
        ## I Param: indicates whether the select modifies a tag's match flag or its inventoried flag. 
        self.target         = target        
        ## I Param: Elicit the tag behavior according to Gb29768 Sort specification. Nota: the rule STUHFL_D_GB29768_RULE_MATCH0_ELSE_1 (0x03) is to be used to invert selection. 
        self.rule           = rule          
        ## I Param: Bank (TagInfo, Coding, Security, User) on which apply the sort. 
        self.memoryBank    = memoryBank
        ## I Param: Selection mask. 
        self.mask           = mask          
        ## I Param: Bit starting address to which mask is applied (bit address). 
        self.maskBitPointer     = maskBitPointer    
        ## I Param: Mask length (in bits). 
        self.maskBitLength      = maskBitLength     

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gb29768_Sort()
        _native.mode         = self.mode              
        _native.target       = self.target            
        _native.rule         = self.rule              
        _native.memoryBank  = self.memoryBank                  
        _native.maskBitPointer   = self.maskBitPointer        
        _native.maskBitLength    = self.maskBitLength                     
        for i, mask in enumerate(self.mask):
            _native.mask[i] = mask 
        return _native

    ## Maps STUHFL ANSI-C API: Gb29768_Sort()   \n
    ## Run Gb29768 sort with predefined class members mode + target + rule + memoryBank + mask + maskBitPointer + maskBitLength
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Sort(STUHFL_T_Gb29768_Sort *gb29768Sort);
    def execute(self):
        if len(self.mask) > STUHFL_native.STUHFL_D_GB29768_MAX_SORT_MASK_LENGTH:
            print('mask exceed max len of {} ..'.format(STUHFL_native.STUHFL_D_GB29768_MAX_SORT_MASK_LENGTH))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gb29768_Sort(_native)
        return retCode

#GB29768_CONFIGURATION
STUHFL_D_GB29768_CONFIGURATION_ATTRIBUTE    = 0
STUHFL_D_GB29768_CONFIGURATION_SECURITYMODE = 1

#GB29768_ACTION_ATTRIBUTE
STUHFL_D_GB29768_ACTION_ATTRIBUTE_READWRITE     = 0
STUHFL_D_GB29768_ACTION_ATTRIBUTE_READUNWRITE   = 1
STUHFL_D_GB29768_ACTION_ATTRIBUTE_UNREADWRITE   = 2
STUHFL_D_GB29768_ACTION_ATTRIBUTE_UNREADUNWRITE = 3

#GB29768_ACTION_SECMODE
STUHFL_D_GB29768_ACTION_SECMODE_AUTH_RESERVED       = 0
STUHFL_D_GB29768_ACTION_SECMODE_AUTH_NOAUTH         = 1
STUHFL_D_GB29768_ACTION_SECMODE_AUTH_AUTH_NOSECCOMM = 2
STUHFL_D_GB29768_ACTION_SECMODE_AUTH_AUTH_SECCOMM   = 3    

## Maps STUHFL ANSI-C structure: STUHFL_T_Gb29768_Lock     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gb29768_Lock:
    ##
    ## @param memoryBank: Bank (TagInfo, Coding, Security, User) on which apply the lock. 
    ## @param configuration: Configure attribute and security mode of storage area. 
    ## @param action: Define how the lock operation is performed. 
    ## @param pwd: Password. 
    ##
    def __init__(self, memoryBank = STUHFL_D_GB29768_AREA_TAGINFO, configuration = STUHFL_D_GB29768_CONFIGURATION_ATTRIBUTE, action = STUHFL_D_GB29768_ACTION_ATTRIBUTE_READWRITE, pwd = [0,0,0,0]):
        # "public" members
        ## I Param: Bank (TagInfo, Coding, Security, User) on which apply the lock. 
        self.memoryBank    = memoryBank       
        ## I Param: Configure attribute and security mode of storage area.   
        self.configuration  = configuration     
        ## I Param: Define how the lock operation is performed. 
        self.action         = action            
        ## I Param: Password. 
        self.pwd            = pwd               

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gb29768_Lock()
        _native.memoryBank   = self.memoryBank         
        _native.configuration = self.configuration       
        _native.action        = self.action             
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        return _native

    def _setFromNative(self, _native):
        self.memoryBank    = _native.memoryBank   
        self.configuration  = _native.configuration       
        self.action         = _native.action      
        self.pwd            = [_native.pwd[i]  for i in range(STUHFL_native.STUHFL_D_PASSWORD_LEN)]

    ## Maps STUHFL ANSI-C API: Gb29768_Lock()   \n
    ## Run Gb29768 Lock with predefined class members memoryBank + configuration + action + pwd
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Lock(STUHFL_T_Gb29768_Lock *gb29768Lock);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_NB_C_VALUES))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gb29768_Lock(_native)
        self._setFromNative(_native)
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Gb29768_Erase     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gb29768_Erase:
    ##
    ## @param memoryBank: Bank (TagInfo, Coding, Security, User) on which apply the erase. 
    ## @param numBytesToErase: Number of bytes to erase. 
    ## @param bytePtr:     Byte address to which erase data. 
    ## @param pwd:         Password. 
    ##
    def __init__(self, memoryBank = STUHFL_D_GB29768_AREA_TAGINFO, numBytesToErase = 0, bytePtr = 0, pwd = [0,0,0,0]):
        # "public" members
        ## I Param: Bank (TagInfo, Coding, Security, User) on which apply the erase. 
        self.memoryBank   = memoryBank    
        ## I Param: Number of bytes to erase. 
        self.numBytesToErase   = numBytesToErase
        ## I Param: Byte start address within bank for data to be erased.
        self.bytePtr       = bytePtr        
        ## I Param: Password. 
        self.pwd           = pwd            

    # Internal methods
    def _toNative(self):
        _native = STUHFL_native.STUHFL_T_Gb29768_Erase()
        _native.memoryBank = self.memoryBank   
        _native.numBytesToErase = self.numBytesToErase   
        _native.bytePtr     = self.bytePtr       
        for i, pwd in enumerate(self.pwd):
            _native.pwd[i] = pwd 
        return _native

    def _setFromNative(self, _native):
        self.memoryBank    = _native.memoryBank   
        self.numBytesToErase    = _native.numBytesToErase       
        self.bytePtr        = _native.bytePtr      
        self.pwd            = [_native.pwd[i]  for i in range(STUHFL_native.STUHFL_D_PASSWORD_LEN)]

    ## Maps STUHFL ANSI-C API: Gb29768_Erase()   \n
    ## Run Gb29768 Erase with predefined class members memoryBank + numBytesToErase + bytePtr + pwd
    ##@return error code
    ##
    #STUHFL_DLL_API STUHFL_T_RET_CODE CALL_CONV Gb29768_Erase(STUHFL_T_Gb29768_Erase *gb29768Erase);
    def execute(self):
        if len(self.pwd) != STUHFL_native.STUHFL_D_PASSWORD_LEN:
            print('PWD must contain {} values..'.format(STUHFL_native.STUHFL_D_PASSWORD_LEN))
            return STUHFL_ERR_PARAM
        _native = self._toNative()
        retCode = STUHFL_native.Gb29768_Erase(_native)
        self._setFromNative(_native)
        return retCode

# endregion GB29768



# ---------------------------------------------------------------------------
# Inventory Runner 
# ---------------------------------------------------------------------------
# region Inventory Runner

#RSSI_MODE
STUHFL_D_RSSI_MODE_REALTIME      = 0x0
STUHFL_D_RSSI_MODE_PILOT         = 0x4
STUHFL_D_RSSI_MODE_SECOND_BYTE   = 0x6
STUHFL_D_RSSI_MODE_PEAK          = 0x8

#INVENTORYREPORT_OPTION
STUHFL_D_INVENTORYREPORT_OPTION_NONE      = 0x00
STUHFL_D_INVENTORYREPORT_OPTION_RESERVED  = 0x01
STUHFL_D_INVENTORYREPORT_OPTION_HEARTBEAT = 0x02

## Maps STUHFL ANSI-C structure: STUHFL_T_InventoryTag     \n
##
class STUHFL_T_InventoryTag:
    def __init__(self, timestamp=0, antenna=STUHFL_D_ANTENNA_1, agc=0, rssiLogI=0, rssiLogQ=0, rssiLinI=0, rssiLinQ=0, pc=[0,0], xpc=[], epc=[], tid=[]):
        ## O Param: Tag detection time stamp. 
        self.timestamp   = timestamp       
        ## O Param: Antenna at which Tag was detected. 
        self.antenna     = antenna         
        ## O Param: AGC measured when TAG found.
        self.agc         = agc             
        ## O Param: I part of Tag logarithmic RSSI.
        self.rssiLogI    = rssiLogI        
        ## O Param: Q part of Tag logarithmic RSSI.
        self.rssiLogQ    = rssiLogQ        
        ## O Param: I part of Tag linear RSSI.
        self.rssiLinI    = rssiLinI        
        ## O Param: Q part of Tag linear RSSI.
        self.rssiLinQ    = rssiLinQ        
        ## O Param: Tag PC. 
        self.pc          = pc              
        ## O Param: Tag XPC. 
        self.xpc         = xpc             
        ## O Param: Tag EPC. 
        self.epc         = epc             
        ## O Param: Tag TID. 
        self.tid         = tid             

#TUNING_STATUS
STUHFL_D_TUNING_STATUS_UNTUNED = 0
STUHFL_D_TUNING_STATUS_TUNING = 1
STUHFL_D_TUNING_STATUS_TUNED = 2

## Maps STUHFL ANSI-C structure: STUHFL_T_InventoryStatistics     \n
##
class STUHFL_T_InventoryStatistics:
    def __init__(self, timestamp=0, roundCnt=0, tuningStatus=STUHFL_D_TUNING_STATUS_UNTUNED, rssiLogMean=0, sensitivity=0, Q=0, frequency=0, adc=0, tagCnt=0, emptySlotCnt=0, collisionCnt=0, skipCnt=0, preambleErrCnt=0, crcErrCnt=0, headerErrCnt=0, rxCountErrCnt=0):
        ## O Param: timestamp of last statistics update. 
        self.timestamp       = timestamp            
        ## O Param: Inventory rounds already done. 
        self.roundCnt        = roundCnt             
        ## O Param: Reader tuning status. 
        self.tuningStatus    = tuningStatus
        ## O Param: RSSI log mean value. Measurement is updated with every found TAG 
        self.rssiLogMean     = rssiLogMean          
        ## O Param: Reader sensitivity. 
        self.sensitivity     = sensitivity          
        ## O Param: Current Q, may vary if adaptive Q is enabled.
        self.Q               = Q                    
        ## O Param: Current used frequency. 
        self.frequency       = frequency            
        ## O Param: ADC value. Measured after each inventory round. 
        self.adc             = adc                  
        ## O Param: Number of detected tags. 
        self.tagCnt          = tagCnt               
        ## O Param: Number of empty slots. 
        self.emptySlotCnt    = emptySlotCnt
        ## O Param: Number of collisions. 
        self.collisionCnt    = collisionCnt
        ## O Param: Number of skipped tags due to failed follow command (eg.: subsequent ReadTID after Query). 
        self.skipCnt         = skipCnt              
        ## O Param: Number of Preamble errors. 
        self.preambleErrCnt  = preambleErrCnt       
        ## O Param: Number of CRC errors. 
        self.crcErrCnt       = crcErrCnt            
        ## O Param: Number of Header errors. 
        self.headerErrCnt    = headerErrCnt         
        ## O Param: Number of RX count errors. 
        self.rxCountErrCnt   = rxCountErrCnt   

## Maps STUHFL ANSI-C structure: STUHFL_T_InventoryData     \n
##
class STUHFL_T_InventoryData:
    def __init__(self, statistics = STUHFL_T_InventoryStatistics(), tagList=[STUHFL_T_InventoryTag()]):
        ## O Param: Inventory statistics. 
        self.statistics     = statistics
        ## O Param: Detected tags list. Tag list memory must be allocated by application
        self.tagList        = tagList

## Class dedicated to Inventory callbacks     \n
##
class ICycleData(ABC):
    ##
    ## @param tagListSizeMax: tagList size. Max number of tags to be stored during inventory. If more tags found, exceeding ones will overwrite last list entry. 
    ##
    def __init__(self, tagListSizeMax=1024):
        # callback type defines
        self.cycleCallback_type = ctypes.CFUNCTYPE(c_uint16, POINTER(STUHFL_native.STUHFL_T_InventoryData))
        self.finishedCallback_type = ctypes.CFUNCTYPE(c_uint16, POINTER(STUHFL_native.STUHFL_T_InventoryData))

        ## "private" members for native argument access
        self._invData = STUHFL_native.STUHFL_T_InventoryData()
        ## O Param: Detected tags list. 
        self._invData.tagList = ctypes.cast((STUHFL_native.STUHFL_T_InventoryTag * tagListSizeMax)(), ctypes.POINTER(STUHFL_native.STUHFL_T_InventoryTag))
        ## I Param: tagList size. Max number of tags to be stored during inventory. If more tags found, exceeding ones will overwrite last list entry. 
        self._invData.tagListSizeMax = tagListSizeMax
        ## O Param: Detected tags number. 
        self._invData.tagListSize = 0

    def __StatisticsFromNative(self, _stats):
        return STUHFL_T_InventoryStatistics(_stats.timestamp, _stats.roundCnt, _stats.tuningStatus, _stats.rssiLogMean, _stats.sensitivity, _stats.Q, _stats.frequency, _stats.adc, _stats.tagCnt, _stats.emptySlotCnt, _stats.collisionCnt, _stats.skipCnt, _stats.preambleErrCnt, _stats.crcErrCnt, _stats.headerErrCnt, _stats.rxCountErrCnt)

    def __DataFromNative(self, _tagList, _listSize):
        return [STUHFL_T_InventoryTag(_tagList[i].timestamp, _tagList[i].antenna, _tagList[i].agc, _tagList[i].rssiLogI, _tagList[i].rssiLogQ, _tagList[i].rssiLinI, _tagList[i].rssiLinQ, [_tagList[i].pc[j] for j in range(2)], [_tagList[i].xpc.data[j] for j in range(_tagList[i].xpc.length)], [_tagList[i].epc.data[j] for j in range(_tagList[i].epc.length)], [_tagList[i].tid.data[j] for j in range(_tagList[i].tid.length)])  for i in range(_listSize)]

    def inventoryCycleCallback(self, _native):
        invData = STUHFL_T_InventoryData(self.__StatisticsFromNative(_native.contents.statistics), self.__DataFromNative(_native.contents.tagList, _native.contents.tagListSize))
        retCode = self.cycleCallback(invData)
        #todo: desallocate _native
        return retCode

    def inventoryFinishedCallback(self, _native):
        invData = STUHFL_T_InventoryData(self.__StatisticsFromNative(_native.contents.statistics), self.__DataFromNative(_native.contents.tagList, _native.contents.tagListSize))
        retCode = self.finishedCallback(invData)
        #todo: desallocate _native
        return retCode

    # Implementation of cycleCallback. 
    # Called when tags are found (either when internal tag buffer is full or after a user-defined timeout)
    # argument invData is type of STUHFL_T_InventoryData .. inventory statistics and collected tag list
    # NOTE: must return 
    @abstractmethod
    def cycleCallback(self, invData):
        return STUHFL_ERR_NONE

    # Implementation of finishedCallback. 
    # Called when inventory runner has terminated
    # argument invData is type of STUHFL_T_InventoryData .. inventory statistics and collected tag list
    @abstractmethod
    def finishedCallback(self, invData):
        return STUHFL_ERR_NONE

## Default Inventory callbacks class    \n
##
class defaultCycleData(ICycleData):
    def cycleCallback(self, data):
        # Nothing to do as start() method is not used in demoBasic
        return STUHFL.STUHFL_ERR_NONE

    def finishedCallback(self, data):
        # Nothing to do as start() method is not used in demoBasic
        return STUHFL.STUHFL_ERR_NONE

## Maps STUHFL ANSI-C structure: STUHFL_T_Inventory     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Inventory(ABC):
    ##
    ## @param cycleData: Cycle data + callbacks.
    ## @param rssiMode: RSSI mode. This defines what RSSI value is sent to the host along with the tag data.
    ## @param inventoryDelay: additional delay that can be added for the each inventory round. 
    ## @param options: Defines Inventory data report scheme (Round/Slot, HeartBeat). 
    ## @param roundCnt: Inventory scan duration (in rounds). Set to 0 for infinity scanning. 
    ##
    def __init__(self, cycleData=defaultCycleData(), rssiMode = STUHFL_D_RSSI_MODE_SECOND_BYTE, inventoryDelay = 0, options = STUHFL_D_INVENTORYREPORT_OPTION_NONE, roundCnt = 1):
        # "public" members
        #STUHFL_T_InventoryOption              
        ## I Param: RSSI mode. This defines what RSSI value is sent to the host along with the tag data.
        self.rssiMode       = rssiMode
        ## I Param: additional delay that can be added for the each inventory round.
        self.inventoryDelay = inventoryDelay
        ## I Param: Defines Inventory data report scheme.
        self.options   = options
        ## I Param: Inventory scan duration (in rounds). Set to 0 for infinity scanning. 
        self.roundCnt       = roundCnt

        ## I Param: Cycle data + callbacks. 
        self.cycleData      = cycleData

        #STUHFL_T_InventoryData                                
        ## O Param: Inventory statistics. 
        self.statistics     = STUHFL_T_InventoryStatistics()
        ## O Param: Detected tags list. 
        self.tagList        = []

    # Internal methods
    def _toNativeOption(self):
        _native = STUHFL_native.STUHFL_T_InventoryOption()
        _native.rssiMode = self.rssiMode
        _native.inventoryDelay = self.inventoryDelay
        _native.options = self.options
        _native.roundCnt = self.roundCnt
        return _native

    def _setFromNativeData(self, _native):
        self.statistics = STUHFL_T_InventoryStatistics(_native.statistics.timestamp, _native.statistics.roundCnt, _native.statistics.tuningStatus, _native.statistics.rssiLogMean, _native.statistics.sensitivity, _native.statistics.Q, _native.statistics.frequency, _native.statistics.adc, _native.statistics.tagCnt, _native.statistics.emptySlotCnt, _native.statistics.collisionCnt, _native.statistics.skipCnt, _native.statistics.preambleErrCnt, _native.statistics.crcErrCnt, _native.statistics.headerErrCnt, _native.statistics.rxCountErrCnt)
        self.tagList = [STUHFL_T_InventoryTag(_native.tagList[i].timestamp, _native.tagList[i].antenna, _native.tagList[i].agc, _native.tagList[i].rssiLogI, _native.tagList[i].rssiLogQ, _native.tagList[i].rssiLinI, _native.tagList[i].rssiLinQ, [_native.tagList[i].pc[j] for j in range(2)], [_native.tagList[i].xpc.data[j] for j in range(_native.tagList[i].xpc.length)], [_native.tagList[i].epc.data[j] for j in range(_native.tagList[i].epc.length)], [_native.tagList[i].tid.data[j] for j in range(_native.tagList[i].tid.length)])  for i in range(_native.tagListSize)]

    @abstractmethod
    def execute(self):
        return STUHFL_ERR_NONE

    ## Maps STUHFL ANSI-C API: Inventory_RunnerStart()   \n
    ## Run Inventory with predefined class members rssiMode + roundCnt + inventoryDelay + options + tagListSizeMax
    ##@param roundCnt: Number of rounds (infinite if 0).
    ##@return error code
    ##
    def start(self, roundCnt = None):
        if roundCnt is not None:
            self.roundCnt = roundCnt
        _nativeOption = self._toNativeOption()
        retCode = STUHFL_native.Inventory_RunnerStart(_nativeOption, self.cycleData.cycleCallback_type(self.cycleData.inventoryCycleCallback), self.cycleData.finishedCallback_type(self.cycleData.inventoryFinishedCallback), self.cycleData._invData)
        return retCode

    ##  Maps STUHFL ANSI-C API: Inventory_RunnerStop()   \n
    ## Run Inventory stop
    ## 
    def stop(self):
        retCode = STUHFL_native.Inventory_RunnerStop()
        return retCode

## Maps STUHFL ANSI-C structure: STUHFL_T_Inventory for Gen2 tags     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gen2_Inventory(STUHFL_T_Inventory):
    ## Maps STUHFL ANSI-C API: Gen2_Inventory()   \n
    ## Run Gen2 Inventory with predefined class members rssiMode + roundCnt + inventoryDelay + options + tagListSizeMax
    ##@return error code
    ##
    def execute(self):
        _nativeOption = self._toNativeOption()
        retCode = STUHFL_native.Gen2_Inventory(_nativeOption, self.cycleData._invData);
        self._setFromNativeData(self.cycleData._invData)
        return retCode;

## Maps STUHFL ANSI-C structure: STUHFL_T_Inventory for Gb29768 tags     \n
## and maps all related functions through dedicated methods 
##
class STUHFL_T_Gb29768_Inventory(STUHFL_T_Inventory):
    ## Maps STUHFL ANSI-C API: Gb29768_Inventory()   \n
    ## Run Gb29768 Inventory with predefined class members rssiMode + roundCnt + inventoryDelay + options + tagListSizeMax
    ##@return error code
    ##
    def execute(self):
        _nativeOption = self._toNativeOption()
        retCode = STUHFL_native.Gb29768_Inventory(_nativeOption, self.cycleData._invData);
        self._setFromNativeData(self.cycleData._invData)
        return retCode;

# endregion Inventory Runner
