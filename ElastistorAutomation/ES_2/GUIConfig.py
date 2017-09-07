#-------------------------------------------------------------------------------
# Name:        GUIConfig
# Purpose:     To read all the user config parameters.
# Author:      Sudarshan
# Created:     18/08/2017
# Copyright:   (c) Cloudbyte 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os

class GuiConfig(object):
     testsetloc = os.getcwd() + os.path.sep + "TestSet.yml"
     dict = {}
     dict['sol_name'] = "CBAutomation"
     dict['testEnv'] = 'icoeqa'
     dict['testsetloc'] = testsetloc
     dict['testtype'] = 'Regression'
     scmpath = os.getcwd()
     url = "https://20.10.31.10/client/index.jsp"
     username = "admin"
     password = "test"
     SiteName = "CB"
     Location = "Bangalore"
     HaGroupName = "CB_HAG"
     HaG_IP1 = "20.10.31.50"
     HaG_IP2 = "20.10.31.51"
     NodeName = "CB_Node"
     AccountName = "CBUser"
     mailid = "cb.ec@cb.com"
     userpwd = "Test1234"
     Pool1 = "Pool1"
     Pool2 = "Pool2"
     VSM1Name = "VSM1"
     VSM1Ip = "16.10.31.200"
     VSM2Name = "VSM2"
     VSM2Ip = "16.10.31.201"
     DRName = "TestDR"
     BKPIP = "16.10.31.250"
     Node1_IP = "20.10.31.30"
     Node2_IP = "20.10.31.31"
     node_username = "root"
     node_password = "test"
     Disk_Enclosure_Name = "ElastistorJbod"
     VLAN_ID = "16"
     VLAN_Interface = "igb0(active)"
     BackupVSMIP = "16.10.31.203"
     NFSClientIP = "16.10.92.50"
     CFSClientIP = "20.10.31.50"
     hostIP = "20.10.31.21"
     DevmanIP = "20.10.31.10"
     interface = "igb0(active)"
     apikey = "bovIsLbI1zaSvlOaUR_UCRRDBTH7_eHD4S1j6Ea2fEFdN6o5rD11rzfUDEaUG6Obid1VBjgmXEybP0bHZhQKsQ"
     responce = "json"
     IPMIIP_Node1 = "20.10.26.39"
     DR_Resume = "F:\\CB_Automation\\WebFramework\\SCM\\DRTestSet.yml"
     UngracefullHA = "F:\\CB_Automation\\WebFramework\\SCM\\UngracefullHA.yml"
     TestSet = "F:\\CB_Automation\\WebFramework\\SCM\\TestSet.yml"

###############################################################
     R1 = " Mirrored "
     R5 = " Raid - Single Parity "
     R6 = " Raid - Double Parity "
     R7 = " Raid - Triple Parity "
     R0 = " Striped "
###############################################################





