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
from os import system, name 

import STUHFL

import STUHFL_demoHelpers

##@brief      Demonstrates how to Inventory all Gen2 tags in the field.
##
def demo_Gen2Inventory():
    print("\n************************************")
    print("*    GEN2 INVENTORY DEMO")

    singleTag = False
    demo_SetupGen2Config(singleTag, True, STUHFL.STUHFL_D_ANTENNA_1, STUHFL.STUHFL_D_TUNING_ALGO_MEDIUM)

    inventory = STUHFL.STUHFL_T_Gen2_Inventory()   # will use default CycleData (1024 max tags + default callbacks)
    inventory.rssiMode = STUHFL.STUHFL_D_RSSI_MODE_SECOND_BYTE
    inventory.options = STUHFL.STUHFL_D_INVENTORYREPORT_OPTION_NONE
    inventory.inventoryDelay = 0
    retCode = inventory.execute()

    if(len(inventory.tagList) != 0):
        print("\n--- Gen2_Inventory Option ---");
        print("\trssiMode    : {}".format(inventory.rssiMode))
        print("\treportMode  : {}".format(inventory.options))
        print("");

        print("--- Round Info ---");
        print("\ttuningStatus: {}".format(inventory.statistics.tuningStatus))
        print("\troundCnt    : {}".format(inventory.statistics.roundCnt))
        print("\tsensitivity : {}".format(inventory.statistics.sensitivity))
        print("\tQ           : {}".format(inventory.statistics.Q))
        print("\tadc         : {}".format(inventory.statistics.adc))
        print("\tfrequency   : {}".format(inventory.statistics.frequency))
        print("\ttagCnt      : {}".format(inventory.statistics.tagCnt))
        print("\tempty Slots : {}".format(inventory.statistics.emptySlotCnt))
        print("\tcollisions  : {}".format(inventory.statistics.collisionCnt))
        print("\tpreampleErr : {}".format(inventory.statistics.preambleErrCnt))
        print("\tcrcErr      : {}".format(inventory.statistics.crcErrCnt))
        print("")

        # print transponder information for TagList
        print("--- {} Tags ---".format(len(inventory.tagList)))
        for i, tag in enumerate(inventory.tagList):
            print("\t------")
            print("\tagc         : {}".format(tag.agc))
            print("\trssiLogI    : {}".format(tag.rssiLogI))
            print("\trssiLogQ    : {}".format(tag.rssiLogQ))
            print("\trssiLinI    : {}".format(tag.rssiLinI))
            print("\trssiLinQ    : {}".format(tag.rssiLinQ))
            print("\tpc          : ", end='')
            for j, val in enumerate(tag.pc):
                print("{:02x}".format(val), end='')
            if(len(tag.epc) != 0):
                print("\n\tepc ({})     : ".format(len(tag.epc)), end='')
                for j, val in enumerate(tag.epc):
                    print("{:02x}".format(val), end='')
            if(len(tag.tid) != 0):
                print("\n\ttid ({})     : ".format(len(tag.tid)), end='')
                for j, val in enumerate(tag.tid):
                    print("{:02x}".format(val), end='')
            print("")
        print("")

##@brief      Demonstrates how to apply on the run a callback on each inventoried tag.
##            Define a Cycle Callback which outputs EPC of each found tag.
##            Define a Cycle Callback which informs of inventory end.
##            Launch Inventory for a given number of rounds (infinite if 0: stop() method must then be used in callback to end inventory).
##
##@param[in]  rounds: Number of inventory rounds (infinite if 0: stop() method must then be used in callback to end inventory).
##
def demo_InventoryRunner(rounds):
    print("\n************************************")
    print("*    INVENTORY RUNNER DEMO")

    singleTag = False
    demo_SetupGen2Config(singleTag, True, STUHFL.STUHFL_D_ANTENNA_1, STUHFL.STUHFL_D_TUNING_ALGO_MEDIUM)

    cycleData = CycleData(1024)     # Define callbacks + set max 1024 tags inventoried at once
    inventory = STUHFL.STUHFL_T_Gen2_Inventory(cycleData)
    inventory.options = STUHFL.STUHFL_D_INVENTORYREPORT_OPTION_HEARTBEAT
    inventory.start(rounds)

#
class CycleData(STUHFL.ICycleData):
    def cycleCallback(self, data):
#        STUHFL_demoHelpers.clear()    

        # print statistics
        print('\nTimestamp: {}, RoundCnt: {} => {} Tags:'.format(data.statistics.timestamp, data.statistics.roundCnt, len(data.tagList))) 

        # print EPC list
        for i, tag in enumerate(data.tagList):
            if(len(tag.epc) != 0):
                print("\t", end='')
                for j, val in enumerate(tag.epc):
                    print("{:02x}".format(val), end='')
                print("")

        return STUHFL.STUHFL_ERR_NONE

    def finishedCallback(self, data):
        #clear()
        # print statistics summary
        print('\n**** Summary ****\n\tTimestamp: {}, RoundCnt: {}\n'.format(data.statistics.timestamp, data.statistics.roundCnt)) 
        print('\tTAGs total: {}\n\tEmptySlotCnt: {}\n\tCollisionCnt: {}\n'.format(data.statistics.tagCnt, data.statistics.emptySlotCnt, data.statistics.collisionCnt)) 

        return STUHFL.STUHFL_ERR_NONE

##@brief      Demonstrates typical Gen2 setup.
##
##@param[in]  singleTag: true if a single tag is expected to be found
##@param[in]  freqHopping: true if a frequency hopping has to be done (EUROPE frequencies), use single default frequency otherwise
##@param[in]  antenna: targeted antenna
##@param[in]  tuningAlgo: tuning algorithm to be applied (NONE/FAST/MEDIUM/SLOW)
##
def demo_SetupGen2Config(singleTag, freqHopping, antenna, tuningAlgo):
    txRxCfg = STUHFL.STUHFL_T_ST25RU3993_TxRxCfg()
    txRxCfg.fetch();
    txRxCfg.rxSensitivity = 3;
    txRxCfg.txOutputLevel = -2;
    txRxCfg.usedAntenna = antenna;
    txRxCfg.alternateAntennaInterval = 1;
    txRxCfg.commit();

    invGen2Cfg = STUHFL.STUHFL_T_ST25RU3993_Gen2_InventoryCfg()
    invGen2Cfg.fetch();
    invGen2Cfg.inventoryOption.fast = True;
    invGen2Cfg.inventoryOption.autoAck = False;
    invGen2Cfg.antiCollision.startQ = 0 if singleTag else 4
    invGen2Cfg.antiCollision.adaptiveQ = False if singleTag else True
    invGen2Cfg.adaptiveSensitivity.enable = True;
    invGen2Cfg.queryParams.toggleTarget = True;
    invGen2Cfg.queryParams.targetDepletionMode = True;
    invGen2Cfg.commit();

    gen2ProtocolCfg = STUHFL.STUHFL_T_ST25RU3993_Gen2_ProtocolCfg()
    gen2ProtocolCfg.fetch();
    gen2ProtocolCfg.tari = STUHFL.STUHFL_D_GEN2_TARI_25_00;
    gen2ProtocolCfg.blf = STUHFL.STUHFL_D_GEN2_BLF_256;
    gen2ProtocolCfg.coding = STUHFL.STUHFL_D_GEN2_CODING_MILLER8;
    gen2ProtocolCfg.trext = STUHFL.STUHFL_D_TREXT_ON;
    gen2ProtocolCfg.commit();

    freqLBT = STUHFL.STUHFL_T_ST25RU3993_FreqLBT()
    freqLBT.fetch();
    freqLBT.listeningTime = 0;
    freqLBT.idleTime = 0;
    freqLBT.rssiLogThreshold = 38;
    freqLBT.skipLBTcheck = True;
    freqLBT.commit();

    if (freqHopping):
        channelList = STUHFL.STUHFL_T_ST25RU3993_ChannelList(STUHFL.STUHFL_D_PROFILE_EUROPE)
    else:
        channelList = STUHFL.STUHFL_T_ST25RU3993_ChannelList()
        channelList.numFrequencies = 1;
        channelList.itemList[0].frequency = STUHFL.STUHFL_D_DEFAULT_FREQUENCY;        
    channelList.antenna = antenna;
    channelList.persistent = False;
    channelList.channelListIdx = 0;
    channelList.commit()

    freqHop = STUHFL.STUHFL_T_ST25RU3993_FreqHop()
    freqHop.maxSendingTime = 400;
    freqHop.minSendingTime = 400;
    freqHop.mode = STUHFL.STUHFL_D_FREQUENCY_HOP_MODE_IGNORE_MIN;
    freqHop.commit();

    gen2Select = STUHFL.STUHFL_T_Gen2_Select()
    gen2Select.mode = STUHFL.STUHFL_D_GEN2_SELECT_MODE_CLEAR_LIST
    gen2Select.execute()
   
    # Eventually Tune the channel lists
    demo_TuneChannelList(tuningAlgo);

    return

##@brief      Demonstrates frequencies tuning.
##            Tune all frequencies defined within demo_SetupGen2Config()
##
##@param[in]  tuningAlgo: tuning algorithm to be applied (NONE/FAST/MEDIUM/SLOW)
##
def demo_TuneChannelList(tuningAlgo):
    if (tuningAlgo == STUHFL.STUHFL_D_TUNING_ALGO_NONE):
        return

    txRxCfg = STUHFL.STUHFL_T_ST25RU3993_TxRxCfg()
    txRxCfg.fetch()
    print("Tuning: ANTENNA_{}, Algo: {}".format(txRxCfg.usedAntenna, tuningAlgo))

    channelList = STUHFL.STUHFL_T_ST25RU3993_ChannelList()
    channelList.persistent = False
    channelList.antenna = txRxCfg.usedAntenna
    channelList.fetch()       # Retrieve ChannelLists already configured in FW

    channelList.falsePositiveDetection = True
    channelList.persistent = False
    channelList.algorithm = tuningAlgo
    channelList.tune()      # Tune all Channels

    # Prints all ChannelList
    channelList.fetch()
    for element in channelList.itemList :
        print('\tFreq: {}, cin:{}, clen:{}, cout:{}'. format(element.frequency, element.caps.cin, element.caps.clen, element.caps.cout))

    return