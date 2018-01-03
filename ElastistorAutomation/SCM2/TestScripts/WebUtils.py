#------------------------------------------------------------------------------
#!/usr/bin/env python
#title           :WebUtils.py
#description     :These methods will help to perform regular actions is Elasticenter.
#note            :These methods are written using EC of 2.0 build.
#author          :Sudarshan Darga
#date            :2017/07/26
#version         :1
#usage           :python WebUtils.py
#notes           :
#python_version  :2.7.12
#==============================================================================

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
from selenium.common.exceptions import NoAlertPresentException, WebDriverException, NoSuchElementException
import time, pyautogui, sys, Logging, os
from SCM2.GUIConfig import GuiConfig as const
from selenium.webdriver.support.ui import Select

class WebUtils():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.filename = os.path.abspath(__file__)
        self.log = Logging.getLogger(self.filename, 'Elastistor')
        self.log.info("Elastistor Automation Suite")
        pyautogui.FAILSAFE = False

    def login_EC(self, url, username, password):
        '''Arguments:
        Author: Sudarshan
                url = url to reach EC
                username = "username to login"
                password = "password to login" '''
        try:
            self.driver.implicitly_wait(2)
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            time.sleep(5)
            self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[3]/form/div[1]/input").send_keys(username)
            self.driver.implicitly_wait(5)
            time.sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[3]/form/div[2]/input").send_keys(password)
            self.driver.implicitly_wait(5)
            time.sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[3]/form/div[3]/button").click()
            self.log.info("Logged into EC successfully")
        except NoSuchElementException as e1:
            self.log.error("While logging to EC "), str(e1)
            sys.exit(1)

    def Addsite(self,n,sitename,location):
        '''Arguments:
        Author: Sudarshan
                n = number of sites to creatginsite"
                location = "name of the location" '''
        count = 0
        while count < n:
            count = count+1
            try:
                self.driver.implicitly_wait(100)
                site = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[9]")
                self.driver.execute_script("$(arguments[0]).click();", site)
                addsite = self.driver.find_element_by_xpath(".//*[@class='content-nodata']/div/button")
                self.driver.execute_script("$(arguments[0]).click();", addsite)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(sitename + str(count))
                self.driver.find_element_by_xpath(".//*[@id='location']").send_keys(location + str(count))
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                time.sleep(5)
                self.driver.implicitly_wait(30)
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Successfully Added Site : %s" % sitename + str(count)
                if message == expected_msg:
                    print "Info:Successfully Added Site: %s" % sitename + str(count)
                    self.log.info("Successfully Added Site: %s" % sitename + str(count))
                else:
                    print "Warning: Unable to view log msg"
                    self.log.warning("Unable to view log msg")
            except NoSuchElementException as e:
                self.log.error("Failed to Add Site"), str(e)
                sys.exit(1)

    def Add_HA_Group(self,n,haname,ip1,ip2):
        '''Arguments:
        Author: Sudarshan
                n = number of HA Groups to create
                name = "name of the HA Group"
                ip1,ip2 = Range of IP's to create HA '''
        count = 0
        while count < n:
            count = count+1
            try:
                self.driver.implicitly_wait(100)
                hag = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[8]")
                self.driver.execute_script("$(arguments[0]).click();", hag)
                myelement = self.driver.find_element_by_xpath(".//*[@class='cb-menu']")
                if myelement.is_displayed():
                    myelement.click()
                else:
                    print ("Action items")
                addhag = self.driver.find_element_by_xpath(".//*[@class='action add reduced-hide']/a")
                self.driver.execute_script("$(arguments[0]).click();", addhag)
                time.sleep(10)
                self.driver.find_element_by_xpath(".//*[@title='Select a Site']/select").click()
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath(".//*[@title='Select a Site']/select/option[%s]" %count).click()
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(haname+str(count))
                self.driver.find_element_by_xpath(".//*[@class='range-item range first'][1]/input").send_keys(ip1)
                self.driver.find_element_by_xpath(".//*[@class='range-item range last'][1]/input").send_keys(ip2)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                time.sleep(5)
                self.driver.implicitly_wait(30)
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Successfully Added HA Group : %s" % haname + str(count)
                if message == expected_msg:
                    self.log.info("Info: Successfully Added HA Group: %s" % haname + str(count))
                else:
                    self.log.error("Unable to view log msg")
            except NoSuchElementException as e2:
                self.log.error("Failed to add HA Group", str(e2))
                sys.exit(1)


    def Add_Node(self,n,name):
        '''Arguments:
        Author: Sudarshan
                n = number of Nodes to create
                name = "name of the node"
                '''
        count = 0
        while count < n:
            count = count + 1
            print count
            try:
                time.sleep(5)
                self.driver.implicitly_wait(100)
                node = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[7]")
                self.driver.execute_script("$(arguments[0]).click();", node)
                myelement = self.driver.find_element_by_xpath(".//*[@class='cb-menu']")
                if myelement.is_displayed():
                    myelement.click()
                else:
                    print ("Action items")
                addnode = self.driver.find_element_by_xpath(".//*[@class='action add reduced-hide']/a")
                self.driver.execute_script("$(arguments[0]).click();", addnode)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name + str(count))
                self.driver.find_element_by_xpath(".//*[@title='IP address of the Node']/select").click()
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath(".//*[@title='IP address of the Node']/select/option[1]").click()
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                time.sleep(5)
                self.driver.implicitly_wait(300)
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Successfully Added Node : %s" % name + str(count)
                if message == expected_msg:
                    self.log.info("Successfully Added Node: %s" % name + str(count))
                else:
                    self.log.warning("Unable to view log msg")
                time.sleep(5)

            except NoSuchElementException as e3:
                self.log.error("Failed to Add Node", str(e3))
                sys.exit(1)

    def Add_Account(self,name):
        '''Arguments:
        Author: Sudarshan
                name = name of the account to create
                mailid = mailid of the user
                password = password for the user'''
        try:
            self.driver.implicitly_wait(100)
            account = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[2]")
            self.driver.execute_script("$(arguments[0]).click();", account)
            myelement = self.driver.find_element_by_xpath(".//*[@class='cb-menu']")
            if myelement.is_displayed():
                myelement.click()
            else:
                print ("Action items")
            addaccount = self.driver.find_element_by_xpath(".//*[@class='action add reduced-hide']/a")
            self.driver.execute_script("$(arguments[0]).click();", addaccount)
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name)
            self.driver.implicitly_wait(10)
            '''ele = "Select an Administrator type to which the task has to be delegated"
            self.driver.find_element_by_xpath(".//*[@title='%s']/select/option[3]" % ele).click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='admin']").send_keys(mailid)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='password']").send_keys(password)
            self.driver.implicitly_wait(10)'''
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            self.driver.implicitly_wait(5)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully Added Account : %s" %name
            if message == expected_msg:
                self.log.info("Successfully Added Account")
            else:
                self.log.error("Failed to create account")
        except NoSuchElementException as ac1:
            self.log.error("Exception: While adding account")
            print str(ac1)
            sys.exit(1)

    def Add_VLAN(self,id,interface):
        '''Arguments:
        Author: Sudarshan
                id = VLAN id
                interface = interface name along with state to configure VLAN'''
        try:
            time.sleep(5)
            self.driver.implicitly_wait(100)
            hag = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[8]")
            self.driver.execute_script("$(arguments[0]).click();", hag)
            selecthag = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span")
            self.driver.execute_script("$(arguments[0]).click();", selecthag)
            time.sleep(5)
            myelement = self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i")
            if myelement.is_displayed():
                self.driver.execute_script("$(arguments[0]).click();", myelement)
            else:
                print ("Action items")
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='tasks']/li[4]/a/span").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            pyautogui.click(1236,160)
            time.sleep(2)
            self.driver.implicitly_wait(10)
            pyautogui.click(1167,208)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='tag']").send_keys(id)
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.implicitly_wait(10)
            ele = "Select the Physical or LAGG Interface on which the VLAN should be created."
            self.driver.find_element_by_xpath(".//*[@title='%s']/select/option[text()='%s']" % (ele,interface)).click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.find_element_by_xpath("html/body/div[4]/div[3]/div/button[1]").click()
            time.sleep(5)
        except Exception as e:
            self.log.error("Exception occured while creating lagg"), str(e)
            sys.exit(1)

    def Configure_DA(self,name,no_of_disks):
        '''Arguments:
        Author: Sudarshan
                name = name for the disk array to configure
                no_of_disks = number of disk in the array'''
        try:
            self.driver.implicitly_wait(300)
            node = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[7]")
            self.driver.execute_script("$(arguments[0]).click();", node)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr/td[1]/span").click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
            self.driver.implicitly_wait(10)
            pyautogui.click(386,681)
            time.sleep(10)
            pyautogui.click(359,419)
            time.sleep(10)
            self.driver.find_element_by_xpath(".//*[@id='name']").clear()
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name)
            self.driver.find_element_by_xpath(".//*[@id='cols']").clear()
            self.driver.find_element_by_xpath(".//*[@id='cols']").send_keys(no_of_disks)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            time.sleep(3)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            time.sleep(5)
            self.driver.implicitly_wait(300)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully Added Disk Array : %s" % name
            if message == expected_msg:
                self.log.info("Successfully Added Disk Array : %s" % name)
            else:
                self.log.error("Unable to view log msg for DA creation")

        except NoSuchElementException as DA1:
            self.log.error("Exception Occured while configuring DA"), str(DA1)
            sys.exit(1)

    def Activate_DR(self,backupip):
        ''' Arguments:
        Author: Sudarshan
            backupip: IP for backup vsm'''
        try:
            self.driver.implicitly_wait(300)
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]").click()
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[1]").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[2]/td[1]").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='dashboard-widget']/div/div[1]/div[2]/ul/li[1]/a/i").click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div[1]/a").click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='mainselection']/select").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                ".//*[@id='mainselection']/select/option[text()='vlan16(active)']").click()
            time.sleep(2)
            self.driver.implicitly_wait(100)
            self.driver.find_element_by_xpath(".//*[@id='ipaddress']").clear()
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='ipaddress']").send_keys(backupip)
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div/a[2]").click()
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "DR VSM network configuration is updated successfully."
            if message == expected_msg:
                print ("DR VSM network configuration is updated successfully.")
            else:
                print ("Unable to view log msg")
            print ("Backup Ip assigned successfully")
            time.sleep(20)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[1]").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[2]/td[1]").click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
            self.driver.find_element_by_xpath(".//*[@class='widget action-tasks']/div/div/ul[2]/li[1]/a").click()
            self.driver.implicitly_wait(100)
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]/span").click()
            time.sleep(30)
            self.driver.implicitly_wait(200)
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[1]/span").click()
            self.log.info("Activation is success, remount the volumes and use.")
            time.sleep(60)
        except Exception as t:
            self.log.error("Exception occured while activating DR", str(t))
            return False

    def Add_Pools(self,n,nodename,name,raid,no_of_disks):
        '''Arguments:
        Author: Sudarshan
                n = number of Pools to create
                name = "name of the pool"
                raid = Raid Group to create
                        Enter 1 to create Mirrored
                              2 to create Raid Single Parity
                              3 to create Raid Double Parity
                              4 to create Raid Triple Parity
                              5 to create Striped
                no_of_disks = No. of disks to create a raid'''
        count = 0
        while count < n:
            count = count + 1
            try:
                self.driver.implicitly_wait(100)
                pool = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[6]")
                self.driver.execute_script("$(arguments[0]).click();", pool)
                self.driver.implicitly_wait(10)
                time.sleep(5)
                myelement = self.driver.find_element_by_xpath(".//*[@id='browser']/div[1]/div/div/div[1]/div[3]/span/i")
                if myelement.is_displayed():
                    myelement.click()
                else:
                    print ("Action items")
                addpool = self.driver.find_element_by_xpath(".//*[@class='action add reduced-hide']/a")
                self.driver.execute_script("$(arguments[0]).click();", addpool)
                time.sleep(2)
                self.driver.find_element_by_xpath(".//*[@title='Select a Node']/select/option[text()='%s']"% nodename).click()
                time.sleep(2)
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath(".//*[@class='select-pool-group field']/div/select/option[text()='%s']"% raid).click()
                self.driver.implicitly_wait(5)
                count1 = 0
                while count1 < no_of_disks:
                    count1 = count1+1
                    print count1
                    try:
                        xpath = ".//*[@class='cb-jbod editable graph-info']/table/tbody/tr[%s]/td[5]/input" % count1
                        print xpath
                        ele = self.driver.find_element_by_xpath(xpath).click()
                        time.sleep(1)
                    except NoSuchElementException as d:
                        self.log.error("Exception:Selecting Disks", str(d))
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                self.driver.implicitly_wait(300)
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Successfully added the Pool : %s" % name + str(count)
                if message == expected_msg:
                    self.log.info("Successfully Added Pool: %s" % name + str(count))
                else:
                    self.log.warning("Unable to view pools log msg")

            except NoSuchElementException as e2:
                self.log.error("Failed to Add Pool", str(e2))
                sys.exit(1)


    def Add_VSMS(self, name, poolnumber, capacity, ip):
        '''Arguments:
        Author: Sudarshan
                name = name of the VSM
                Capacity = "Size of the VSM"
                ip =  IP for the VSM'''
        try:
            time.sleep(5)
            self.driver.implicitly_wait(100)
            pools = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[6]")
            self.driver.execute_script("$(arguments[0]).click();", pools)
            selectpool = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[%s]/td[1]/span['%s']" % (poolnumber,poolnumber))
            self.driver.execute_script("$(arguments[0]).click();", selectpool)
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@class='add add-vsm']/a/i").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").clear()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").send_keys(capacity)
            #self.driver.find_element_by_xpath(".//*[@id='units']/option[%s]" % MGT).click()
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@title='Network Interface on the Node that the VSM should use']/select/option[1]").click()
            self.driver.find_element_by_xpath(".//*[@id='address']").send_keys(ip)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            self.driver.implicitly_wait(300)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully added the VSM : %s" % name
            if message == expected_msg:
                self.log.info("Successfully Added VSM: %s" % name)
            else:
                self.log.warning("Unable to view log msg")
        except NoSuchElementException as e4:
            self.log.error("Failed to Add VSM"), str(e4)
            sys.exit(1)


    def Add_NCFS_Volume(self,vsmnumber, name, capacity, protocol, clientip):
        '''Arguments:
        Author:Sudarshan
                vsmnumber: Number of the VSM on which volumes need to be created
                protocol = NFS or CFS protocol volumes to create
                name = "name of the volume"
                capacity = "Size of the volume" '''
        try:
            self.driver.implicitly_wait(100)
            vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
            self.driver.execute_script("$(arguments[0]).click();", vsm)
            selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[%s]/td[1]/span['%s']" %(vsmnumber, vsmnumber))
            self.driver.execute_script("$(arguments[0]).click();", selectvsm)
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='add add-volume']/a/i").click()
            self.driver.implicitly_wait(5)
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").clear()
            time.sleep(2)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").send_keys(capacity)
            self.driver.find_element_by_xpath(".//*[@id='iopsValue']").clear()
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@id='iopsValue']").send_keys("200")
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@class='protocols-items']/div[3]/input").click()
            time.sleep(5)
            self.driver.implicitly_wait(60)
            if protocol == "NFS":
                self.driver.find_element_by_xpath(".//*[@class='protocols-items']/div[3]/div/div[1]/input").click()
                time.sleep(2)
                self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Successfully Added Volume : %s" % name
                if message == expected_msg:
                    self.log.info("Successfully Added Volume: %s" % name)
                else:
                    self.log.warning("Unable to view log msg")
                time.sleep(5)
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@class='widget volumeAccessible']/div[2]/div/div/div[text()='add an NFS client to the Storage Volume.']").click()
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@id='authnetwork']").send_keys(clientip)
                time.sleep(2)
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[1]").click()
                time.sleep(2)
                self.driver.implicitly_wait(100)
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Authorized NFS clients have been added"
                if message == expected_msg:
                    self.log.info("Authorized NFS clients have been added")
                else:
                    self.log.warning("Unable to view log msg")
            elif protocol == "CFS":
                self.driver.find_element_by_xpath(".//*[@class='protocols-items']/div[3]/div/div[2]/input").click()
                time.sleep(2)
                self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Successfully Added Volume : %s" % name
                if message == expected_msg:
                    self.log.info("Successfully Added Volume: %s" % name)
                else:
                    self.log.warning("Unable to view log msg")
                time.sleep(5)
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@class='cifs']/a/span").click()
                self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div[1]/a").click()
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@id='hostsallow']").send_keys(clientip)
                time.sleep(2)
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div/a[2]").click()
                time.sleep(2)
                self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]").click()
                time.sleep(2)
                self.driver.implicitly_wait(100)
                message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
                expected_msg = "Storage Volume properties have been modified"
                if message == expected_msg:
                    self.log.info("Storage Volume properties have been modified")
                else:
                    self.log.warning("Unable to view log msg")
            else:
                print "Please select NFS or CFS protocol"

        except NoSuchElementException as vol1:
            self.log.error("Exception while adding volume"), str(vol1)
            sys.exit(1)

    def Add_iSCSI_FC_Volume(self,n, name, capacity):
        '''Arguments:
        Author:Sudarshan :
                n = Enter 1 to create iSCSI volume, 2 to create FC volume
                name = "name of the volume"
                capacity = "Size of the volume" '''
        try:
            self.driver.implicitly_wait(100)
            vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
            self.driver.execute_script("$(arguments[0]).click();", vsm)
            selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span")
            self.driver.execute_script("$(arguments[0]).click();", selectvsm)
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='add add-volume']/a/i").click()
            self.driver.implicitly_wait(5)
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").clear()
            time.sleep(2)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").send_keys(capacity)
            self.driver.find_element_by_xpath(".//*[@id='iopsValue']").clear()
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@id='iopsValue']").send_keys("200")
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@class='protocols-items']/div[%s]/input" %n).click()
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully Added Volume : %s" % name
            if message == expected_msg:
                self.log.info("Successfully Added Volume: %s" % name)
            else:
                self.log.warning("Unable to view log msg")
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='iscsi']/a/span").click()
            self.driver.find_element_by_xpath(".//*[@id='edit']/i").click()
            self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div[1]/a").click()
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='initiatorgroups']/label[2]/div/select/option[1]").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div/a[2]").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]").click()
            time.sleep(2)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Storage Volume properties have been modified"
            if message == expected_msg:
                self.log.info("Storage Volume properties have been modified")
            else:
                self.log.warning("Unable to view log msg")
        except NoSuchElementException as vol1:
            self.log.error("Exception occured: While creating iSCSI volume"), str(vol1)
            sys.exit(1)

    def Create_DR(self, name, bkp_ip):
        '''Arg:uments:
        Author: Swarnalatha
                name = name for the DR
                bkp_ip= Ip for backup vsm
        '''
        try:
            self.driver.implicitly_wait(100)
            vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
            self.driver.execute_script("$(arguments[0]).click();", vsm)
            selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span")
            self.driver.execute_script("$(arguments[0]).click();", selectvsm)
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
            self.driver.find_element_by_xpath(".//*[@class='widget action-tasks']/div/div/ul[2]/li/a/span").click()
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
            pyautogui.click(422, 435)
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            myele = self.driver.find_element_by_xpath(".//*[@id='address']")
            if myele.is_displayed():
                myele.send_keys(bkp_ip)
            else:
                print "Done"
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='cron month']/span[1]/span").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@class='cron-period']/div/ul/li[1]").click()
            self.driver.implicitly_wait(90)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            time.sleep(60)
        except NoSuchElementException as e:
            self.log.error("Exception occured while creating DR"), str(e)
            return False

    def DR_Enable_Disable(self,state):
        '''Arguments:
        Author: Swarnalatha
        state: Enter Enable or Disable to do specific action'''
        try:
            self.driver.implicitly_wait(100)
            if state == "Enable":
                vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
                self.driver.execute_script("$(arguments[0]).click();", vsm)
                selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[2]")
                self.driver.execute_script("$(arguments[0]).click();", selectvsm)
                time.sleep(5)
                self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
                self.driver.find_element_by_xpath(".//*[@class='widget action-tasks']/div/div/ul[2]/li[2]/a/span").click()
                self.driver.implicitly_wait(10)
                time.sleep(10)
                self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[1]/span").click()
                time.sleep(20)
            elif state == "Disable":
                vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
                self.driver.execute_script("$(arguments[0]).click();", vsm)
                selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[2]")
                self.driver.execute_script("$(arguments[0]).click();", selectvsm)
                time.sleep(5)
                self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
                self.driver.find_element_by_xpath(".//*[@class='widget action-tasks']/div/div/ul[2]/li[2]/a/span").click()
                self.driver.implicitly_wait(10)
                time.sleep(10)
                self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]/span").click()
                time.sleep(20)
            else:
                print ("Invalid Input Given")
        except NoSuchElementException as Enb:
            print("Exception occured during Enable/Disable DR"),str(Enb)
            return False


    def Enable_Flash(self):
        self.driver.get("about:addons")
        pyautogui.click(92, 253)
        time.sleep(2)
        pyautogui.click(1213, 398)
        time.sleep(1)
        pyautogui.click(1230, 452)
        time.sleep(5)

    def deleteDR(self):
        '''Author:Swarnalatha'''
        try:
            self.driver.implicitly_wait(100)
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[1]/i").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[2]/td[12]/div/i").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]/span").click()
            self.driver.implicitly_wait(20)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully deleted the DR VSM."
            if message == expected_msg:
                print "Successfully deleted DR: "
            else:
                print "Warning: Unable to view log msg"
        except NoSuchElementException as vol1:
            print "Error:", str(vol1)
            sys.exit(1)

    def HA_Maintenance(self, node, state):
        '''Author:Swarnalatha
        node: name of the node which we need to move to maintenance
        '''
        try:
            self.driver.implicitly_wait(100)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[7]").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[%s]/td[1]/span" % node).click()

            nodestatus = self.driver.find_element_by_xpath(".//*[@class='nodestatus info-text']").text
            nodestatus1 = nodestatus.split(' ')[1]
            if nodestatus1 == state:
                self.driver.implicitly_wait(5)
                self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
                self.driver.find_element_by_xpath(".//*[@class='nodemanagestatetask']/a/span").click()
                self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[1]").click()
                time.sleep(100)
            else:
                print "Node is not in available state"

        except NoSuchElementException as e1:
            print "Error: Maintenance", str(e1)


    def Maintenance_table_info(self):
        table = self.driver.find_element_by_xpath("//table[@class='ha-job-table adminTable']")
        if table:
            print ("Table Present as expected")
        else:
            print ("Table not Present")
        row_count = len(self.driver.find_elements_by_xpath(
            ".//table[@class='ha-job-table adminTable']/tbody/tr"))
        print row_count
        column_count = len(self.driver.find_elements_by_xpath(
            ".//table[@class='ha-job-table adminTable']/tbody/tr[2]/td"))
        print column_count
        table_header_list = []
        first_part = ".//table[@class='ha-job-table adminTable']/tbody/tr[1]/th["
        second_part = "]"
        for i in range(column_count):
            i += 1
            final_xpath = first_part + str(i) + second_part
            table_head = self.driver.find_element_by_xpath(final_xpath)
            print table_head.text
            table_header_list.append(table_head.text)
        first_part = ".//table[@class='ha-job-table adminTable']/tbody/tr["
        second_part = "]/td["
        third_part = "]"
        table_data_list = []
        rows = row_count - 1
        for i in range(1, rows):
            i = i + 1
            # print i
            for j in range(column_count):
                j += 1
                final_xpath = first_part + str(i) + second_part + str(j) + third_part
                table_data = self.driver.find_element_by_xpath(final_xpath)
                table_data_list.append(table_data.text)
        print table_header_list
        print table_data_list
        return table_header_list, table_data_list

    def table_info(self):
        self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[4]").click()
        self.driver.implicitly_wait(10)
        table = self.driver.find_element_by_xpath("//table[@class='adminTable dataTable no-footer']")
        if table:
            print ("Table Present as expected")
        else:
            print ("Table not Present")
        row_count = len(self.driver.find_elements_by_xpath(
            ".//table[@class='adminTable dataTable no-footer']/tbody/tr"))
        print row_count
        column_count = len(self.driver.find_elements_by_xpath(
            ".//table[@class='adminTable dataTable no-footer']/tbody/tr[1]/td"))
        print column_count
        table_header_list = []
        first_part = ".//table[@class='adminTable dataTable no-footer']/thead/tr/th["
        second_part = "]"
        for i in range(column_count):
            i += 1
            final_xpath = first_part + str(i) + second_part
            table_head = self.driver.find_element_by_xpath(final_xpath)
            print table_head.text
            table_header_list.append(table_head.text)
        first_part = ".//table[@class='adminTable dataTable no-footer']/tbody/tr["
        second_part = "]/td["
        third_part = "]"
        table_data_list = []
        for i in range(row_count):
            i += 1
            for j in range(column_count):
                j += 1
                final_xpath = first_part + str(i) + second_part + str(j) + third_part
                table_data = self.driver.find_element_by_xpath(final_xpath)
                table_data_list.append(table_data.text)
        print table_header_list
        print table_data_list
        return table_header_list, table_data_list

    def poweron(self,host,username,password):
        try:
            self.driver.get(host)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(
                "html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/input[1]").send_keys(username)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(
                "html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/input[2]").send_keys(password)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='login_word']").click()
            time.sleep(5)
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(5)
            pyautogui.click(851, 395)
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            time.sleep(2)
            pyautogui.click(361, 673)
            time.sleep(5)
        except Exception as e1:
            self.log.error("Exception occured"), str(e1)
            sys.exit(1)

    def Create_MigrantVSM(self, bkp_ip):
        '''Arg:uments:
        Author: Swarnalatha
                bkp_ip= Ip for backup vsm'''

        try:
            vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
            self.driver.execute_script("$(arguments[0]).click();", vsm)
            selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span")
            self.driver.execute_script("$(arguments[0]).click();", selectvsm)
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
            self.driver.find_element_by_xpath(".//*[@class='widget action-tasks']/div/div/ul[3]/li/a").click()
            self.driver.implicitly_wait(10)
            time.sleep(10)
            self.driver.find_element_by_xpath(".//*[@class='pd-buttons buttons']/button[1]/span").click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
            pyautogui.click(422, 435)
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.find_element_by_xpath(".//*[@id='address']").send_keys(bkp_ip)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='cron month']/span[1]/span").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@class='cron-period']/div/ul/li[1]").click()
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            time.sleep(60)
        except NoSuchElementException as e:
            self.log.error("Exception occured while creating Migrant VSM"), str(e)
            return False

    def Activate_MigrantVSM(self, backupip):
        ''' Arguments:
        Author: Swarnalatha
            backupip: IP for backup vsm'''
        try:
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]").click()
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[1]").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[2]/td[1]").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='dashboard-widget']/div/div[1]/div[2]/ul/li[1]/a/i").click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div[1]/a").click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='mainselection']/select").click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                ".//*[@id='mainselection']/select/option[text()='em0 (active)']").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='settings-detail']/div/a[2]").click()
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Migrant VSM network configuration is updated successfully."
            if message == expected_msg:
                print (" Migrant VSM network configuration is updated successfully.")
            else:
                print ("Unable to view log msg")
            print ("Backup Ip assigned successfully")
            time.sleep(20)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[1]").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[2]/td[1]").click()
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
            self.driver.find_element_by_xpath(".//*[@class='widget action-tasks']/div/div/ul[2]/li[1]/a").click()
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]/span").click()
            time.sleep(30)
            self.driver.implicitly_wait(200)
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[1]/span").click()
            self.log.info("Activation is success, remount the volumes and use.")
            time.sleep(60)
        except Exception as t:
            self.log.error("Exception occured while activating Migrant VSM"), str(t)
            return False

    def Migration_Enable_Disable(self, state):
        '''Arguments:
        Author: Swarnalatha
        state: Enter Enable or Disable to do specific action'''
        try:
            self.driver.implicitly_wait(100)
            if state == "Enable":
                vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
                self.driver.execute_script("$(arguments[0]).click();", vsm)
                selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[2]")
                self.driver.execute_script("$(arguments[0]).click();", selectvsm)
                time.sleep(5)
                self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
                self.driver.find_element_by_xpath(
                    ".//*[@class='widget action-tasks']/div/div/ul[2]/li[2]/a/span").click()
                self.driver.implicitly_wait(10)
                time.sleep(10)
                self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[1]/span").click()
                time.sleep(20)
            elif state == "Disable":
                vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
                self.driver.execute_script("$(arguments[0]).click();", vsm)
                selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[2]")
                self.driver.execute_script("$(arguments[0]).click();", selectvsm)
                time.sleep(5)
                self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()
                self.driver.find_element_by_xpath(
                    ".//*[@class='widget action-tasks']/div/div/ul[2]/li[2]/a/span").click()
                self.driver.implicitly_wait(10)
                time.sleep(10)
                self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]/span").click()
                time.sleep(20)
            else:
                print ("Invalid Input Given")
        except NoSuchElementException as Enb:
            print("Exception occured during Enable/Disable Migrant schedule"), str(Enb)
            return False

    def deleteMigrantVSM(self):
        '''Author:Swarnalatha'''
        try:
            self.driver.implicitly_wait(100)
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span[1]/i").click()
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[2]/td[12]/div/i").click()
            time.sleep(2)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonset']/button[2]/span").click()
            self.driver.implicitly_wait(20)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully deleted the Migrant VSM."
            if message == expected_msg:
                print "Successfully deleted Migrant VSM: "
            else:
                print "Warning: Unable to view log msg"
        except NoSuchElementException as vol1:
            print "Error:", str(vol1)
            sys.exit(1)

    def Create_Migrantvolume(self,name):
        try:
            '''Getting elements'''
            self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[4]").click() # Click volume
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[1]/td[1]/span").click() # Select 1st volume
            time.sleep(5)
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()# Click volume actions
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='53e6ca4d-47af-328e-8c8b-7952c41b70f6']/div/div/ul[2]/li/a/span").click() # Click Migration schedule
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='cb-wizard-container']/div[2]/div[1]/div[2]/div[2]/button[1]").click()  # First form 'next' button
            self.driver.implicitly_wait(10)
            pyautogui.click(423,515) # selecting second pool
            self.driver.find_element_by_xpath(".//*[@id='cb-wizard-container']/div[2]/div[1]/div[2]/div[2]/button[1]").click()
            self.driver.implicitly_wait(10)
            time.sleep(10)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(name) # Entering migrant's name
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='cb-wizard-container']/div[2]/div[1]/div[2]/div[2]/button[1]").click()
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='address']").send_keys(const.BackupVSMIP)
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath(".//*[@id='cb-wizard-container']/div[2]/div[1]/div[2]/div[2]/button[1]").click() #Final button
            time.sleep(10)
        except NoSuchElementException as e:
            self.log.error("Exception occurred while creating migrant volume"), str(e)
            return False

    def Assign_NFSClient(self):
        try:
            time.sleep(3)
            self.driver.find_element_by_xpath(".//*[@class='widget volumeAccessible']/div[2]/div/div/div").click()
            self.driver.find_element_by_xpath(".//*[@id='authnetwork']").send_keys(const.NFSClientIP)
            self.driver.find_element_by_xpath("html/body/div[3]/div[3]/div/button[1]").click()
            message = self.driver.find_element_by_xpath(".//*[@id='container']/div[4]/div[2]/span/span").text
            Expected_message = "Authorized NFS clients have been added"
            if message == Expected_message:
                self.log.info("NFS client is assigned successfully")
            else:
                self.log.error("Exception while assigning client")
        except Exception as e1:
            print "Exception", str(e1)

    def Activate_Volume(self):
        try:
            self.driver.find_element_by_xpath(".//*[@class='dashboard-content']/div/div/ul/li[4]").click()  # Click Volumes in the side pane
            var = self.driver.find_element_by_xpath(".//*[@class='data-table tcc-leftbar']/div/div/table/tbody/tr/td/span/i")
            self.driver.execute_script("$(arguments[0]).click();", var)                   # Expanding tree view
            self.driver.find_element_by_xpath(".//*[@class='data-table tcc-leftbar']/div/div/table/tbody/tr[2]/td[1]/span").click()   # Click dest vol
            self.driver.implicitly_wait(10)
            time.sleep(15)
            self.driver.find_element_by_xpath(".//*[@class='top-widgets tcc-topbar']/div[3]/span/i").click()     # Click CB actions menu
            #self.driver.execute_script("$(arguments[0]).click();", action_menu)
            # Click 'Migrate' link
            self.driver.find_element_by_xpath(".//*[@class='activate']/a/span").click()
            time.sleep(15)
            self.driver.implicitly_wait(10)
            # Entering ok in the confirmation dialog
            self.driver.find_element_by_xpath(".//*[@class='ui-dialog-buttonpane ui-widget-content ui-helper-clearfix']/div/button[2]").click()
            time.sleep(60)

        except Exception as e:
            print "Exception occurred", str(e)

    def close_browser(self):
        self.driver.quit()
        self.log.info("Closed Browser Successfully")

def main():
    username = "admin"
    password = "test"
    url = "https://20.10.92.190/client/index.jsp"
    t = WebUtils()
    t.login_EC(url,username,password)
    time.sleep(5)
    #t.Add_Account("Sudarshan")
    #time.sleep(5)
    '''
    t.Add_HA_Group(1,"SudHA","16.10.31.5","16.10.31.6")
    time.sleep(5)
    t.Add_Node(1,"N1")
    time.sleep(5)
    t.Add_Node(2,"N2")
    t.Add_Pools(2,"SudPool",2,5)
    time.sleep(5)
    t.Add_VSMS("SudVSM1",1,"16.10.31.200")
    time.sleep(5)
    t.Add_VSMS("SudVSM2", 1,"16.10.31.201")
    time.sleep(5)
    t.Add_Volume("NFSVol1",100)
    time.sleep(5)
    t.Add_Volume("NFSVol2",100)
    time.sleep(5)'''
    #t.Add_VLAN("16")
    #t.Create_DR("DRTESTVSM","16.10.31.230")    #t.table_info()
    #time.sleep(60)
    #t.Configure_DA("CB_Storage", 18)
    #t.Add_VSMS("TestVSM", 1, "16.10.92.201")
    #time.sleep(5)
    #t.Add_Volume("TestVol",100)
    #time.sleep(5)
    #t.Add_Volume("TestVol2",100)
    #t.Add_VSMS("TestVSM2", 700, 2, "16.10.92.202")

    #t.Addsite(2,"testsite","hyd")
    #time.sleep(5)
    #t.Add_HA_Group(1,"testha","20.10.31.70","20.10.31.71")
    #time.sleep(5)
    #t.Add_Node(1,"Testnode")
    t.close_browser()

if __name__ == '__main__':
    main()

