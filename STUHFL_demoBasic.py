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
from os import system, name 

import STUHFL

import STUHFL_demoHelpers
import STUHFL_demoInventoryRunner       # demo_SetupGen2Config() & tuneChannelList()


##@brief      Demonstrates how to retrieve STUHFL LIB & HW/SW versions
##            as well as the STUHFL HW/SW Informations
##
def demo_GetVersion():
#    STUHFL_demoHelpers.clear()    

    print("\n************************************")
    print("*    GET VERSION DEMO")

    # LibVersion
    libVersion = STUHFL.STUHFL_T_VersionLib()
    libVersion.fetch()
    print('LIB:', *libVersion.version, sep = ".")  

    # BoardVersion
    boardVersion = STUHFL.STUHFL_T_VersionBoard()
    boardVersion.fetch()
    print('Board SW:', *boardVersion.swVersion, sep = ".")  
    print('Board HW:', *boardVersion.hwVersion, sep = ".")  

    # BoardInfo
    boardVersionInfo = STUHFL.STUHFL_T_VersionInfo()
    boardVersionInfo.fetch()
    print(boardVersionInfo.swVersionInfo)
    print(boardVersionInfo.hwVersionInfo)
    return

##@brief      Demonstrates how to Read registers through a single access or multiple accesses.
##            - Reads all registers one by one.
##            - Reads all registers at once.
##
def demo_ReadRegisters():
#    STUHFL_demoHelpers.clear()    

    print("\n************************************")
    print("*    READ REGISTERS DEMO")

    nbRegisters = 8

    # Read register one by one
    print("Reading {} first registers one by one".format(nbRegisters))
    reg = STUHFL.STUHFL_T_ST25RU3993_Register()
    for addr in range(nbRegisters):
        reg.addr = addr
        reg.fetch()
        print('RegAddr: {}, RegData: {}'.format(hex(reg.addr), hex(reg.data))) 
    print("-----------------------------------------------------------------------------")

    # Read a single register
    print("Reading a single register")
    reg.fetch(0x2a)
    print('RegAddr: {}, RegData: {}'.format(hex(reg.addr), hex(reg.data))) 
    print("-----------------------------------------------------------------------------")

    # Read all registers at once
    print("Reading {} first registers at once".format(nbRegisters))
    for addr in range(nbRegisters):
        reg.multi.append(reg.Item(addr))
    reg.fetchmultiple()                  # Get all allocated regs
    for item in reg.multi:
        print('RegAddr: {}, RegData: {}'.format(hex(item.addr), hex(item.data)))
    print("-----------------------------------------------------------------------------")
    return

##@brief      Demonstrates how to Write registers through a single access or multiple accesses.
##            - Write one single register.
##            - Write multiple registers at once.
##
def demo_WriteRegisters():
#    STUHFL_demoHelpers.clear()    

    print("\n************************************")
    print("*    WRITE REGISTERS DEMO")

    nbRegisters = 5

    # Save registers before update
    saveReg = STUHFL.STUHFL_T_ST25RU3993_Register()
    for addr in range(nbRegisters):
        saveReg.multi.append(saveReg.Item(0x03 + addr))
    saveReg.fetchmultiple()

    print("Writing register: 0x03 = 0xCD")
    reg = STUHFL.STUHFL_T_ST25RU3993_Register()
    reg.addr = 0x03
    reg.data = 0xCD
    reg.commit()
    print("Writing registers: 0x04 to {} (resp. {} to {})".format(hex(0x03+nbRegisters-1), hex(0xBA), hex(0xBA-nbRegisters+2)))
    reg.multi = []
    for addr in range(nbRegisters-1):
        reg.multi.append(reg.Item(0x03 + 1 + addr, 0xBA - addr))
    reg.commitmultiple()

    # Reading registers: 0x03-0x08
    reg.multi = []
    for addr in range(nbRegisters):
        reg.multi.append(reg.Item(0x03 + addr))
    reg.fetchmultiple()
    for item in reg.multi:
        print('RegAddr: {}, RegData: {}'.format(hex(item.addr), hex(item.data)))
    print("-----------------------------------------------------------------------------")

    # Restore registers
    print("Restoring registers: 0x03 to {}".format(hex(0x03+nbRegisters-1)))
    saveReg.commitmultiple()
    saveReg.fetchmultiple()
    for item in saveReg.multi:
        print('RegAddr: {}, RegData: {}'.format(hex(item.addr), hex(item.data)))
    print("-----------------------------------------------------------------------------")
    return

##@brief      Demonstrates how to run a Gen2 Read command.
##            First inventories all available tags in the field,
##            then reads 8 bytes on the first inventoried tag.
##            The read is started from first word in User memory bank.
##
def demo_Gen2Read():
#    STUHFL_demoHelpers.clear()    

    print("\n************************************")
    print("*    READ TAG DEMO")

    singleTag = False
    STUHFL_demoInventoryRunner.demo_SetupGen2Config(singleTag, True, STUHFL.STUHFL_D_ANTENNA_1, STUHFL.STUHFL_D_TUNING_ALGO_MEDIUM)

    inventory = STUHFL.STUHFL_T_Gen2_Inventory()
    inventory.rssiMode = STUHFL.STUHFL_D_RSSI_MODE_SECOND_BYTE
    inventory.inventoryDelay = 0
    retCode = inventory.execute()

    if(len(inventory.tagList) != 0):
        print("Found {} tags, selecting first found tag:".format(len(inventory.tagList)))
        demo_Gen2Select(inventory.tagList[0].epc)

        readData = STUHFL.STUHFL_T_Gen2_Read()
        readData.memoryBank = STUHFL.STUHFL_D_GEN2_MEMORY_BANK_USER
        readData.wordPtr = 0
        readData.numBytesToRead = 8
        readData.pwd  = [0  for i in range(STUHFL.STUHFL_D_PASSWORD_LEN)]
        retCode = readData.execute()

        if (retCode == STUHFL.STUHFL_ERR_NONE):
            print("--- Reading 8 bytes ---")
            if(len(readData.data) != 0):
                for i, val in enumerate(readData.data):
                    print("{:02x}".format(val), end='')
            print("")
        else:
            print("Tag cannot be read ({})".format(retCode))
    else:
        print("No Tag ({})".format(retCode))

##@brief      Demonstrates how to run a Gen2 Write command.
##            First inventories all available tags in the field,
##            saves the 2 first bytes in USER memory,
##            writes ABCD in the 2 first bytes of USER memory
##            writes back initial data to USER memory
##            The read is started from first word in User memory bank.
##
def demo_Gen2Write():
#    STUHFL_demoHelpers.clear()    

    print("\n************************************")
    print("*    WRITE TAG DEMO")

    singleTag = False
    STUHFL_demoInventoryRunner.demo_SetupGen2Config(singleTag, True, STUHFL.STUHFL_D_ANTENNA_1, STUHFL.STUHFL_D_TUNING_ALGO_MEDIUM)

    inventory = STUHFL.STUHFL_T_Gen2_Inventory()
    inventory.rssiMode = STUHFL.STUHFL_D_RSSI_MODE_SECOND_BYTE
    inventory.inventoryDelay = 0
    retCode = inventory.execute()

    if(len(inventory.tagList) != 0):
        print("Found {} tags, selecting first found tag:".format(len(inventory.tagList)))
        demo_Gen2Select(inventory.tagList[0].epc)

        orgReadData = STUHFL.STUHFL_T_Gen2_Read()
        orgReadData.memoryBank = STUHFL.STUHFL_D_GEN2_MEMORY_BANK_USER
        orgReadData.wordPtr = 0
        orgReadData.numBytesToRead = 2
        orgReadData.pwd  = [0  for i in range(STUHFL.STUHFL_D_PASSWORD_LEN)]
        retCode = orgReadData.execute()
        if (retCode != STUHFL.STUHFL_ERR_NONE):
            print("Tag cannot be read ({}), exiting demo".format(retCode))
            return        

        writeData = STUHFL.STUHFL_T_Gen2_Write()
        writeData.wordPtr   = 0   
        writeData.memoryBank   = STUHFL.STUHFL_D_GEN2_MEMORY_BANK_USER   
        writeData.pwd       = [0  for i in range(STUHFL.STUHFL_D_PASSWORD_LEN)]
        writeData.data      = [0xAB, 0xCD]
        retCode = writeData.execute()
        if (retCode != STUHFL.STUHFL_ERR_NONE):
            print("Tag cannot be written ({}), exiting demo".format(retCode))
            return

        print("--- Wrote {:02x}{:02x} @ {} in Bank {}:".format(writeData.data[0], writeData.data[1], writeData.wordPtr, writeData.memoryBank))

        readData = STUHFL.STUHFL_T_Gen2_Read()
        readData.memoryBank = STUHFL.STUHFL_D_GEN2_MEMORY_BANK_USER
        readData.wordPtr = 0
        readData.numBytesToRead = 8
        readData.pwd  = [0  for i in range(STUHFL.STUHFL_D_PASSWORD_LEN)]
        retCode = readData.execute()
        if (retCode == STUHFL.STUHFL_ERR_NONE):
            if(len(readData.data) != 0):
                for i, val in enumerate(readData.data):
                    print("{:02x}".format(val), end='')
            print("")
        else:
            print("\tCannot read data")  

        print("--- Writing back original data:")
        writeData = STUHFL.STUHFL_T_Gen2_Write()
        writeData.wordPtr   = 0   
        writeData.memoryBank   = STUHFL.STUHFL_D_GEN2_MEMORY_BANK_USER   
        writeData.pwd       = [0  for i in range(STUHFL.STUHFL_D_PASSWORD_LEN)]
        writeData.data      = orgReadData.data
        retCode = writeData.execute()            
        if (retCode != STUHFL.STUHFL_ERR_NONE):
            print("\tTag cannot be written ({}), exiting demo".format(retCode))
            return

        readData.memoryBank = STUHFL.STUHFL_D_GEN2_MEMORY_BANK_USER
        readData.wordPtr = 0
        readData.numBytesToRead = 8
        readData.pwd  = [0  for i in range(STUHFL.STUHFL_D_PASSWORD_LEN)]
        retCode = readData.execute()
        if (retCode == STUHFL.STUHFL_ERR_NONE):
            if(len(readData.data) != 0):
                for i, val in enumerate(readData.data):
                    print("{:02x}".format(val), end='')
            print("")
        else:
            print("\tCannot read data")  

    else:
        print("No Tag ({})".format(retCode))

##@brief      Demonstrates how to run a Gen2 Generic Command.
##            First inventories all available tags in the field,
##            then reads nbWords words on the first inventoried tag through a generic command emulating Gen2 Read command.
##            The read is started from first word in User memory bank.
##
##@param[in]  nbWords: Number of words to read on tag
##
def demo_Gen2GenericCommand(nbWords):
#    STUHFL_demoHelpers.clear()    

    print("\n************************************")
    print("*    GEN2 GENERIC COMMAND DEMO")

    singleTag = False
    STUHFL_demoInventoryRunner.demo_SetupGen2Config(singleTag, True, STUHFL.STUHFL_D_ANTENNA_1, STUHFL.STUHFL_D_TUNING_ALGO_MEDIUM)

    inventory = STUHFL.STUHFL_T_Gen2_Inventory()
    inventory.rssiMode = STUHFL.STUHFL_D_RSSI_MODE_SECOND_BYTE
    inventory.inventoryDelay = 0
    retCode = inventory.execute()

    if(len(inventory.tagList) != 0):
        print("Found {} tags, selecting first found tag:".format(len(inventory.tagList)))
        demo_Gen2Select(inventory.tagList[0].epc)

        genericCmd =  STUHFL.STUHFL_T_Gen2_GenericCmd()
        genericCmd.cmd = STUHFL.STUHFL_D_GEN2_GENERIC_CMD_CRC_EXPECT_HEAD
        genericCmd.noResponseTime = 0xFF
        genericCmd.appendRN16 = True
        genericCmd.sndDataBitLength = 26
        genericCmd.sndData.append(0xC2)
        genericCmd.sndData.append(0xC0)
        genericCmd.sndData.append(nbWords >> 2)
        genericCmd.sndData.append(nbWords << 6)
        genericCmd.expectedRcvDataBitLength = nbWords*16 + 16
        retCode = genericCmd.execute()

        if (retCode == STUHFL.STUHFL_ERR_NONE):
            print("--- Rcv data ---")
            if(len(genericCmd.rcvData) != 0):
                for i, val in enumerate(genericCmd.rcvData):
                    print("{:02x}".format(val), end='')
            print("")
        else:
            print("Tag cannot be accessed ({})".format(retCode))
    else:
        print("No Tag ({})".format(retCode))

##@brief      Demonstrates how to Power ON/OFF the antenna.
##
def demo_Power():
#    STUHFL_demoHelpers.clear()    

    print("\n************************************")
    print("*    POWER MANAGEMENT DEMO")

    pwr = STUHFL.STUHFL_T_ST25RU3993_AntennaPower()
    # turn on power
    pwr.mode = STUHFL.STUHFL_D_ANTENNA_POWER_MODE_ON
    pwr.commit()
    time.sleep(1)
    pwr.mode = STUHFL.STUHFL_D_ANTENNA_POWER_MODE_OFF
    pwr.commit()
    return

##@brief      Demonstrates how to setup a Gen2 Select on a given tag EPC
##
##@param[in]  epc: Tag EPC to which apply the select
##
def demo_Gen2Select(epc):
    if(len(epc) != 0):
        print("\tSelecting on TAG EPC: ", end='')
        for j, val in enumerate(epc):
            print("{:02x}".format(val), end='')
        print("")

        selData = STUHFL.STUHFL_T_Gen2_Select()
        selData.mode = STUHFL.STUHFL_D_GEN2_SELECT_MODE_CLEAR_AND_ADD
        selData.target = STUHFL.STUHFL_D_GEN2_SELECT_TARGET_SL
        selData.action = 0
        selData.memoryBank = STUHFL.STUHFL_D_GEN2_MEMORY_BANK_EPC
        selData.maskBitPointer = 0x00000020
        selData.mask = epc
        selData.maskBitLength = len(epc) * 8
        selData.truncation = False
        selData.execute()

    
    
    
    
    