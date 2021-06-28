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

#Define relative path to wrapper directory
PATHTOWRAPPER = "..\..\..\..\Middleware\wrapper\python"


#Check Python wrapper and related DLL can be reached
if not os.path.isdir(os.getcwd() + "\\" + PATHTOWRAPPER):
    print ("""
********************* CAUTION **********************************
Following PATH does not exists !!!
{}

Please edit ...\Applications\STUHFL_demo_wrapper\STUHFL_demo_py\STUHFL_demo_py\STUHFL_demo.py
and update path to Middleware Python wrapper (variable: 'PATHTOWRAPPER', line 6)
****************************************************************
""".format(os.getcwd() + "\\" + PATHTOWRAPPER))
    sys.exit()
os.environ['PATH'] += ";" + os.getcwd() + "\\" + PATHTOWRAPPER
sys.path.append(PATHTOWRAPPER)


import STUHFL

import STUHFL_demoHelpers
import STUHFL_demoBasic
import STUHFL_demoInventoryRunner

libVersion = STUHFL.STUHFL_T_VersionLib()
libVersion.fetch()
print("Welcome to the ST-UHF-L demo \nSTUHFL version", *libVersion.version, sep = ".")

# Connect/Disconnect
comPort = 'COM{}'
for i in range(100):
    port = comPort.format(i)
    ret = STUHFL.Connect(port)
    if ret == 0:
        # runs boardVersion.fetch() to ensure communication with FW is established
        boardVersion = STUHFL.STUHFL_T_VersionBoard()
        if boardVersion.fetch() == STUHFL.STUHFL_ERR_NONE:
            print('\nUsing ComPort: {}'.format(port)) 
            break
        else:
            STUHFL.Disconnect()
        

STUHFL_demoBasic.demo_GetVersion()

STUHFL_demoBasic.demo_Power()

STUHFL_demoBasic.demo_ReadRegisters()
STUHFL_demoBasic.demo_WriteRegisters()

STUHFL_demoInventoryRunner.demo_InventoryRunner(500)    # 500 Rounds
STUHFL_demoInventoryRunner.demo_Gen2Inventory()

STUHFL_demoBasic.demo_Gen2GenericCommand(3)

STUHFL_demoBasic.demo_Gen2Read()
STUHFL_demoBasic.demo_Gen2Write()



#while 1:
#    pass
