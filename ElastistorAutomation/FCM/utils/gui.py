#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      (Initial Draft)
#
# Created:     10/08/2016
# Copyright:   (c) DELLEMC
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import Logging

from selenium.common.exceptions import NoAlertPresentException, \
WebDriverException, NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import *
import SendKeys as send_keys
import time,os
from GuiConstants import GuiConstants
import re


class gui():
 def __init__(self):
     self.driver = Firefox()
     self.filename = os.path.abspath(__file__)
     self.log = Logging.getLogger(self.filename,'NHC')
     self.log.info("test")
     self.directory = "C:\\Screenshots"


 def login_mnr_dashboard(self,url,username,password):
    self.driver = Firefox()
    self.driver.implicitly_wait(2)
    self.driver.get(url)
    self.driver.implicitly_wait(5)
    username = username
    password = password
    self.driver.find_element_by_id('username'). \
        send_keys(username)
    self.driver.find_element_by_id('password'). \
        send_keys(password)
    self.driver.implicitly_wait(10)
    self.driver.find_element_by_xpath("//*[text()='Sign In']").click()

 def drill_down_organization(self):
     try:
         self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
         self.driver.implicitly_wait(2)
         self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
         self.driver.implicitly_wait(2)
         self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb']/span").click()
         self.driver.implicitly_wait(2)
         self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-278952e3']/span").click()
         self.driver.implicitly_wait(2)
         self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-278952e3-3d149fdb']/span").click()
         self.driver.implicitly_wait(2)
         self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-278952e3-3d149fdb-ff247c6a']/span").click()
         self.driver.implicitly_wait(2)
     except NoSuchElementException as e:
         print e
         return False
     return True

 def drill_down_org_Quota(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-278952e3-3d149fdb-ff247c6a']/span").click()

     try:
         self.driver.find_element_by_xpath("//*[@title='system']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Quota']").click()
     except NoSuchElementException as e:
         print e
         return False
     return True

 def drill_down_org_Users(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-278952e3-3d149fdb-ff247c6a']/span").click()
     self.driver.implicitly_wait(2)
     try:
         self.driver.find_element_by_xpath("//*[@title='system']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Users']").click()
     except NoSuchElementException as e:
         print e
         return False
     return True

 def drill_down_org_Services(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-278952e3-3d149fdb-ff247c6a']/span").click()
     self.driver.implicitly_wait(2)
     try:
         self.driver.find_element_by_xpath("//*[@title='system']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Services']").click()

     except NoSuchElementException as e:
         print e
         return False
     return True

 def drill_down_applications(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-bcaea28a']/span").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='Organizations']").click()
         self.driver.find_element_by_xpath(".//*[@class='cell-value' and text()='system']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-state-default ui-corner-top' and @title='Spaces']").click()
         #self.driver.find_element_by_xpath(".//*[@class='node row-selected odd']/td[1]/div/span").click()
         self.driver.implicitly_wait(2)
         self.driver.find_element_by_xpath(".//*[@class='cell-value' and text()='notifications-with-ui']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Applications']")
         self.driver.find_element_by_xpath("//*[@title='Applications']")
         self.log.info("The grill-down to applications is done")
     except NoSuchElementException:
         self.log.info("Element not found")
         return False
     return True

 def drill_down_spaces(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-9818379c']/span").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='Spaces']").click()
         self.driver.find_element_by_xpath(".//*[@class='cell-value' and text()='system']").click()
         self.driver.find_element_by_xpath(".//*[@class='cell-value' and text()='app-usage-worker']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Build Packs']")
         self.driver.find_element_by_xpath("//*[@title='Build Packs']")
         self.log.info("The application subtable is present")
     except NoSuchElementException:
         self.log.info("Element not found")
         return False
     return True

 def pcf_inventory_users(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-71baa245']/span").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='Users']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Spaces']")
         self.log.info("The Spaces tab and table under that tab is present")
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Organizations']")
         self.log.info("The Organizations tab and table under that tab is present")
         self.driver.find_element_by_xpath(".//*[@class='cell-value' and text()='admin']").click()
         self.log.info("Each individual User summary is displayed")
     except NoSuchElementException:
         self.log.info("Element not found")
         return False
     return True


 def check_title_block_present(self):
     """
	      @author: aarthi
	       Checks whether title Chargeback by Application present under Report Library->NHC Reports
	 """
     #actions = ActionChains(self.driver)
     #path = self.driver.find_element_by_xpath("//*[@title='Report Library']")
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-91b6ea3a']/span").click()
     time.sleep(5)
     #actions.move_to_element(path)
     #actions.click()
     #actions.perform()
    # self.driver.find_element_by_xpath("//*[@title='NHC Reports']").click()
     #self.driver.find_element_by_xpath("//*[@title='Chargeback']").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='Chargeback by Application']")
     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def chargeback_by_service_plans(self):
     #actions = ActionChains(self.driver)
     #path = self.driver.find_element_by_xpath("//*[@title='Report Library']")
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-91b6ea3a']/span").click()
     time.sleep(5)
     try:
         self.driver.find_element_by_xpath("//*[@title='Chargeback by Service Plans']").click()
         self.driver.find_elements_by_xpath("//*[text()='Chargeback by Service Plans' and @class='report-name']")
     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def chargeback_by_service(self):
     # actions = ActionChains(self.driver)
     # path = self.driver.find_element_by_xpath("//*[@title='Report Library']")
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-91b6ea3a']/span").click()
     time.sleep(5)

     try:
         self.driver.find_element_by_xpath("//*[@title='Chargeback by Service']")
         self.log.info("title- Chargeback by Service is present")
     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def cloud_controller_Health(self):
     #actions = ActionChains(self.driver)
     #path = self.driver.find_element_by_xpath("//*[@title='Report Library']")
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-925211fa']/span").click()
     #self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8']/span").click()
     time.sleep(5)
     #actions.move_to_element(path)
     #actions.click()
     #actions.perform()
    # self.driver.find_element_by_xpath("//*[@title='NHC Reports']").click()
     #self.driver.find_element_by_xpath("//*[@title='Chargeback']").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='Cloud Controller Health']").click()
     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def Router_Health(self):
     #actions = ActionChains(self.driver)
     #path = self.driver.find_element_by_xpath("//*[@title='Report Library']")
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-d774a820']/span").click()
     time.sleep(5)
     try:
         self.driver.find_element_by_xpath("//*[@title='Router Health']").click()
     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def chargeback_History(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31']/span").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='Chargeback History']")
         #self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-4d6ef425']/span").click()
         #self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-7189562e']/span").click()
         #self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-5dd4bad0']/span").click()
     except NoSuchElementException:
         print "Elements not found"
         return False
     return True

 def chargeback_History_Memory(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-4d6ef425']/span").click()

     try:
         self.driver.find_element_by_xpath("//*[@title='Memory']").click()
     except NoSuchElementException:
         print "Elements not found"
         return False
     return True
 def chargeback_History_Memory_org(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-4d6ef425-e3b2ccf4']/span").click()
     try:
         #self.driver.find_element_by_xpath("//*[@title='Memory']")
         self.driver.find_element_by_xpath("//*[@title='system']").click()
     except NoSuchElementException:
         print "Elements not found"
         return False
     return True

 def chargeback_History_Service_Usage(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-7189562e']/span").click()

     try:
         self.driver.find_element_by_xpath("//*[@title='Service Usage']").click()

     except NoSuchElementException:
         print "Element not found"
         return False
     return True
 def chargeback_History_Service_Usage_org(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-7189562e-e3b2ccf4']/span").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='system']").click()
     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def chargeback_History_Disk(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-5dd4bad0']/span").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='Disk']").click()
     except NoSuchElementException:
         print "Element not found"
         return False
     return True
 def chargeback_History_Disk_org(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-81d02a31-5dd4bad0-e3b2ccf4']/span").click()
     try:
         self.driver.find_element_by_xpath("//*[@title='system']").click()
     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def chargeback_history_organization(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-91b6ea3a']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-91b6ea3a-61bc3f84']").click()

     try:
         self.driver.find_element_by_xpath("//*[@title='Chargeback by Organization']").click()
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Chargeback History']").click()
         self.log.info("the chargeback History tab is present")
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Memory']")
         self.log.info("the Memory tab is present under chargeback History tab")
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Service Usage']")
         self.log.info("the Service_usage tab is present under chargeback History tab")
         self.driver.find_element_by_xpath(".//*[@class='ui-tabs-anchor' and text()='Disk']")
         self.log.info("the Disk tab is present under chargeback History tab")

     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def applications(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-bc7ed8c3']").click()

     try:
         self.driver.find_element_by_xpath("//*[@title='Applications']").click()
         self.driver.implicitly_wait(10)
         self.driver.find_element_by_xpath(".//*[@id='e0-t62ce62219462574b-ffffffef-2c25ea99-bc7ed8c3']").click()

     except NoSuchElementException:
         print "Element not found"
         return False
     return True

 def Buildpacks_reports(self):
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-685d6790']").click()
     try:

         self.driver.find_element_by_xpath("//*[@title='Buildpacks']").click()

     except NoSuchElementException:
        self.log.info("Element not found")
        return False
     return True


 def click_Collector_Performance(self):

     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-cc1d2e8']/span").click()
     self.driver.find_element_by_xpath("//*[@title='Collector Performance']").click()
     self.driver.find_element_by_xpath("//*[@title='Collector Performance']").click()
#     try:

 #        self.driver.find_element_by_xpath("//*[@title='Collector Performance']").click()

  #   except NoSuchElementException:
   #     self.log.error("Element not found")
    #    return False
     #return True

 def table_info_common(self):

     table = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']")
     if table:
        self.log.info("Collector Performance Table Present as expected")
     else:
        self.log.error("Router Table not Present")

     table_value1 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]")
     table_header = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[1]")
     table_val_ip = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[2]")
     table_header_ip = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[2]")
     table_val_2x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[3]")
     table_header_2x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[3]")

     self.log.info("The values from table : %s is %s ", table_header.text, table_value1.text)
     self.log.info("The values from table : %s is %s ", table_header_ip.text, table_val_ip.text)
     self.log.info("The values from table : %s is %s ", table_header_2x.text, table_val_2x.text)

 def sparkline_validation_health(self):
     sparkline_val_req = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[5]/div/span/span[2]/canvas")
     sparkline_val_2x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[6]/div/span/span[2]/canvas")
     sparkline_val_3x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[7]")
     sparkline_val_4x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[8]/div/span/span[2]/canvas")
     if sparkline_val_req and sparkline_val_2x and sparkline_val_3x and sparkline_val_4x:
        self.log.info("Sparklines are displayed as expected")
     else:
        self.log.error("All sparkline graphs are not displayed")

 def sparkline_validation_Router_health(self):
     sparkline_val_req = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[5]/div/span/span[2]/canvas")
     sparkline_val_2x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[6]/div/span/span[2]/canvas")
     sparkline_val_3x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[7]/div/span/span[2]/canvas")
     sparkline_val_4x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[8]/div/span/span[2]/canvas")
     sparkline_val_5x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[9]/div/span/span[2]/canvas")
     sparkline_val_6x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[10]/div/span/span[2]/canvas")

     if sparkline_val_req and sparkline_val_2x and sparkline_val_3x and sparkline_val_4x and sparkline_val_5x and sparkline_val_6x:
        self.log.info("Sparklines are displayed as expected")
     else:
        self.log.error("All sparkline graphs are not displayed")

 def sparkline_validation_com(self,item):

    if item == "cloud controller health":
        line_graph_cloudC_health_cpu = self.driver.find_elements_by_xpath(GuiConstants.line_graph_cloudC_health_cpu)
        line_graph_cloudC_health_ram_c = self.driver.find_elements_by_xpath(GuiConstants.line_graph_cloudC_health_ram_c)
        line_graph_cloudC_health_ram_f = self.driver.find_elements_by_xpath(GuiConstants.line_graph_cloudC_health_ram_f)
        line_graph_cloudC_health_ram_u = self.driver.find_elements_by_xpath(GuiConstants.line_graph_cloudC_health_ram_u)

        if line_graph_cloudC_health_cpu and line_graph_cloudC_health_ram_c and line_graph_cloudC_health_ram_f and line_graph_cloudC_health_ram_u:
            self.log.info("Line Graphs are displayed in table as expected")
        else:
            self.log.error("All line graphs are not displayed")
    elif item == "router_health":
        line_graph_routerh_badgateways = self.driver.find_elements_by_xpath(GuiConstants.line_graph_routerh_badgateways)
        line_graph_routerh_rejectedreqs = self.driver.find_elements_by_xpath(GuiConstants.line_graph_routerh_rejectedreqs)
        line_graph_routerh_routedapp = self.driver.find_elements_by_xpath(GuiConstants.line_graph_routerh_routedapp)
        line_graph_routerh_totalreqs = self.driver.find_elements_by_xpath(GuiConstants.line_graph_routerh_totalreqs)
        line_graph_routerh_reqspersec = self.driver.find_elements_by_xpath(GuiConstants.line_graph_routerh_reqspersec)
        line_graph_routerh_totalroutes = self.driver.find_elements_by_xpath(GuiConstants.line_graph_routerh_totalroutes)
        if line_graph_routerh_badgateways and line_graph_routerh_rejectedreqs and line_graph_routerh_routedapp and line_graph_routerh_totalreqs and line_graph_routerh_reqspersec and line_graph_routerh_totalroutes:
            self.log.info("Line Graphs are displayed in table as expected")
        else:
            self.log.error("All line graphs are not displayed")

 def graph_info_health(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8-338178e1']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def graph_info_health_memory(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     #self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='g1Rtl2QhYifAmtkIn1u1WMQNs9q6GPLZGNSePnK7U58HvR6bmk9YW0aOw0IQulP13TmiTCyqNMtgf7cuPM5ITa460BadzhiEwFuhAiQ6P55GeLzZ5eTsnjW4dplBqhjns']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def graph_info_health_Service_usage(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     #self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='greynRKDnJwDlYlL5PqCY2jsK7NCXMJ19ElZ67H5jaClK5wLCUXGCOqU0eWJcBil4ud0640WD0iB0oJs2ZWdSUYkefo1kmuAqoeKDH5MEDLBMPrxOdsranW4FreYFz8AK']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def graph_info_health_Disk(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     #self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='g7Cnonye2rqVAkolwpgn8QDDui5OwrD4Q7zaAOzrQFE7O22xEAKydaIyFkP2ENK8HPxSre946xCNbfrU2wW2eOtGFAak8GRo903Pq5kTTjtqfUJcYwMx5fmuBYcnzNGso']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def graph_info_health_Disk_org(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     #self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='gA4AdRAk1CqvzaclhZJKupZHZwG5gzZBzNRApE1raMO9ykrrFt7hgYcUsSKB7ZsmL7WhdP34PjHSDQjwAOnpua7qofwhq5gnqzi1gadJWnikLBy0RComauV4uHCfILikK']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def graph_info_health_Serviceusage_org(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     #self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='gxovQoP1DOHiQ6FYwYstvwCOLRPj2bM0oFR434gJKv93IVcyniUouLQgfE6dvkV99oI05Z0Ux8FN4XQrTpzV0j0VdDhLKkchRJuJdcy2Enh98XqMfi9tOXK4d6yy0FBnd']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def graph_info_health_Memory_org(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     #self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='gZ9MKF400ZkmI9m2PXvi8xbLvIbA8E0XJ53JMVwdCwxnl716DtZGJVQKKMIxSjQUtdlPbBWrKP5nJwxjJGUEdnizk5Zq1jGSwD7n55e6UWgYD4X32X7cezfdGNehpvtVm']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def graph_info_Router_health(self,filename):
     file_path = os.path.join(self.directory,filename)
     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")
     self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='g5Dddl9DWmX8cEdAguGBvAImCVGPSTkDaZsV9iomwk9iK8IdEgujRjddYRsuTVxvLMT6huDfraZcKNcL0msOSEXnjUXkMy6tv3ZEVC6GSaBrv2dDrMIQPdVzdMQnqsj2l']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)

 def legend_item_validation_router(self):
    legend_item1 = self.driver.find_elements_by_xpath(".//*[text()='router.rejected_requests' and @class='ui-button-text']")
    legend_item2 = self.driver.find_elements_by_xpath(".//*[text()='router.total_requests' and @class='ui-button-text']")
    legend_item3 = self.driver.find_elements_by_xpath(".//*[text()='healthy' and @class='ui-button-text']")
    legend_item4 = self.driver.find_elements_by_xpath(".//*[text()='router.routed_app_requests' and @class='ui-button-text']")
    legend_item5 = self.driver.find_elements_by_xpath(".//*[text()='router.bad_gateways' and @class='ui-button-text']")
    legend_item6 = self.driver.find_elements_by_xpath(".//*[text()='router.total_routes' and @class='ui-button-text']")
    legend_item7 = self.driver.find_elements_by_xpath(".//*[text()='router.requests_per_sec' and @class='ui-button-text']")

    if legend_item1 and legend_item2 and legend_item3 and legend_item4 and legend_item5 and legend_item6 and legend_item7:
        self.log.info("All legend items are displayed as expected")
    else:
        self.log.error("Legend Items aren't displayed as expected")

 def legend_item_validation_Gbhrs(self):
    legend_item1 = self.driver.find_elements_by_xpath(".//*[text()='(GbHrs)' and @class='ui-button-text']")
    if legend_item1:
        self.log.info("The legend items are displayed as expected")
    else:
        self.log.error("Legend Items aren't displayed as expected")

 def legend_item_validation_hrs(self):
    legend_item1 = self.driver.find_elements_by_xpath(".//*[text()='(Hrs)' and @class='ui-button-text']")
    if legend_item1:
        self.log.info("The legend items are displayed as expected")
    else:
        self.log.error("Legend Items aren't displayed as expected")

 def legend_item_validation_com(self,item):

    if item == "CloudControllerThread":
        legend_item1 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread1)
        legend_item2 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread2)
        legend_item3 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread3)
        legend_item4 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread4)
        legend_item5 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread5)
        legend_item6 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread6)

        if legend_item1 and legend_item2 and legend_item3 and legend_item4 and legend_item5 and legend_item6:
            self.log.info("All legend items are displayed as expected")
        else:
            self.log.error("Legend Items aren't displayed as expected")
    elif item == "routerhealth Thread":
        legend_item1 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_routerhealth_thread1)
        legend_item2 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_routerhealth_thread2)
        legend_item3 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_routerhealth_thread3)
        legend_item4 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_routerhealth_thread4)
        legend_item5 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_routerhealth_thread5)
        legend_item6 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_routerhealth_thread6)
        legend_item7 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_routerhealth_thread7)

        if legend_item1 and legend_item2 and legend_item3 and legend_item4 and legend_item5 and legend_item6 and legend_item7:
            self.log.info("All legend items are displayed as expected")
        else:
            self.log.error("Legend Items aren't displayed as expected")
    elif item == "chargeback history":
        legend_item1 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_chargebackH_thread1)
        if legend_item1:
            self.log.info("The legend item is displayed as expected")
        else:
            self.log.info("Legend item is not displayed as expected")
    elif item == "chargeback history hrs":
        legend_item1 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_chargebackH_thread2)
        if legend_item1:
            self.log.info("The legend item is displayed as expected")
        else:
            self.log.info("Legend item is not displayed as expected")

 def click_Router_Performance(self):
     """
	   @author: aarthi
	   Checks whether title Chargeback by Application present under Report Library->NHC Reports->PCF Operations->Router->Router Performance
	 """

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-d774a820']/span").click()

     try:

         self.driver.find_element_by_xpath("//*[@title='Router Performance']").click()

     except NoSuchElementException:
        self.log.info("Element not found")
        return False
     return True

 def click_Etcd_Health(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()

     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433']/span").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8']/a").click()
     self.driver.find_element_by_xpath(".//*[@title='etcd Health']").click()

 def click_Cloud_Controller_Queue(self):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-925211fa']/span").click()

     try:

         self.driver.find_element_by_xpath("//*[@title='Cloud Controller Queues']").click()

     except NoSuchElementException:
        self.log.info("Element not found")
        return False
     return True


 def click_Cloud_Controller_Threads(self,xpath):

     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-925211fa']/span").click()
     self.driver.implicitly_wait(5)

     try:

         self.driver.find_element_by_xpath(xpath).click()

     except NoSuchElementException:
        self.log.info("Element not found")
        return False
     return True

 def click_Situations_To_Watch(self):

     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     #self.driver.find_element_by_xpath("//*[@title='Situations to Watch']").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-78b1520e']/span").click()
     self.driver.implicitly_wait(5)


     try:

         self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-78b1520e-cd96fc77']/a").click()
         self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-78b1520e-cd96fc77']/a").click()

     except NoSuchElementException:
        self.log.info("Element not found")
        return False
     return True

 def click_Situations_To_Etcd(self):

     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     #self.driver.find_element_by_xpath("//*[@title='Situations to Watch']").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-78b1520e']/span").click()
     self.driver.implicitly_wait(5)


     try:

         self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd']/a").click()
         self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd']/a").click()

     except NoSuchElementException:
        self.log.info("Element not found")
        return False
     return True

 def table_info_com(self):
    table = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']")
    if table:
        self.log.info("Table Present as expected")
    else:
        self.log.error("Table not Present")

    #get no of rows in table
    row_count = len(self.driver.find_elements_by_xpath(
                ".//table[@class='content-table dataTable no-footer']/tbody/tr"))

    # get no of columns in table
    column_count = len(self.driver.find_elements_by_xpath(
        ".//table[@class='content-table dataTable no-footer']/tbody/tr[1]/td"))

    # get list of headers of table
    # divided xpath In three parts  to pass Row_count and Col_count values.
    table_header_list = []
    first_part = ".//table[@class='content-table dataTable no-footer']/thead/tr/th["
    second_part = "]/div/a"
    for i in range(column_count):
        i += 1
        #prepared final xpath
        final_xpath = first_part+str(i)+second_part
        table_head = self.driver.find_element_by_xpath(final_xpath)
        table_header_list.append(table_head.text)
    #divided xpath In three parts  to pass Row_count and Col_count values.
    first_part = ".//table[@class='content-table dataTable no-footer']/tbody/tr["
    second_part = "]/td["
    third_part = "]"
    # Used for loop for number of rows.
    table_data_list = []
    for i in range(row_count):
        i += 1
        # Used for loop for number of columns.
        for j in range(column_count):
            j += 1
            # Prepared final xpath of specific cell as per values of i and j.
            final_xpath = first_part+str(i)+second_part+str(j)+third_part
            # Will retrieve value from located cell and print It.
            table_data = self.driver.find_element_by_xpath(final_xpath)
            table_data_list.append(table_data.text)

    for row_list in [table_data_list[i:i + len(table_header_list)] for i in range(0, len(table_data_list), len(table_header_list))]:
         for (head, data) in zip(table_header_list, row_list):
                 self.log.info("The values from table : %s is %s ", head, data)
    return (table_header_list, table_data_list)

 def print_table(self, table_head, table_data):
     self.log.info("inside print table")
     for row_list in [table_data[i:i + len(table_head)] for i in range(0, len(table_data), len(table_head))]:
         for (head, data) in zip(table_head, row_list):
                 self.log.info("The values from table : %s is %s ", head, data)


 def table_info(self):
     table = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']")
     if table:
        self.log.info("Router Table Present as expected")
     else:
        self.log.error("Router Table not Present")

     table_value1 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]")
     table_header = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[1]")
     table_val_ip = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[2]")
     table_header_ip = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[2]")
     table_val_xxx = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[7]")
     table_header_xxx = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[7]")
     table_val_2x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[3]")
     table_header_2x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[3]")
     table_val_3x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[4]")
     table_header_3x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[4]")
     table_val_4x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[5]")
     table_header_4x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[5]")
     table_val_5x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[6]")
     table_header_5x = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[6]")

     self.log.info("The values from table : %s is %s ", table_header.text, table_value1.text)
     self.log.info("The values from table : %s is %s ", table_header_ip.text, table_val_ip.text)
     self.log.info("The values from table : %s is %s ", table_header_2x.text, table_val_2x.text)
     self.log.info("The values from table : %s is %s ", table_header_3x.text, table_val_3x.text)
     self.log.info("The values from table : %s is %s ", table_header_4x.text, table_val_4x.text)
     self.log.info("The values from table : %s is %s ", table_header_5x.text, table_val_5x.text)
     self.log.info("The values from table : %s is %s ", table_header_xxx.text, table_val_xxx.text)


     #self.log.info(table.text)




     #return table.text

 def sparkline_validation(self):
     sparkline_val_req = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-d254819a-9ffc5675-7e3c4543-95e0f588']/td[3]/div/span/span[2]/canvas")
     sparkline_val_2x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-d254819a-9ffc5675-7e3c4543-95e0f588']/td[4]/div/span/span[2]/canvas")
     sparkline_val_3x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-d254819a-9ffc5675-7e3c4543-95e0f588']/td[5]/div/span/span[2]/canvas")
     sparkline_val_4x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-d254819a-9ffc5675-7e3c4543-95e0f588']/td[6]/div/span/span[2]/canvas")
     sparkline_val_5x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-d254819a-9ffc5675-7e3c4543-95e0f588']/td[7]/div/span/span[2]/canvas")
     sparkline_val_x = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-d254819a-9ffc5675-7e3c4543-95e0f588']/td[8]/div/span/span[2]/canvas")

     if sparkline_val_req and sparkline_val_2x and sparkline_val_3x and sparkline_val_4x and sparkline_val_5x and sparkline_val_x:
        self.log.info("Sparklines are displayed as expected")
     else:
        self.log.error("All sparkline graphs are not displayed")

 def linegraph_validation_cloud_controller_log_errors(self,item):

   if item == "CloudControllerLogErrors":
     line_graph_error_log_count = self.driver.find_elements_by_xpath(GuiConstants.error_log_count)
     line_graph_fatal_log_count = self.driver.find_elements_by_xpath(GuiConstants.fatal_log_count)
     line_graph_warn_log_count = self.driver.find_elements_by_xpath(GuiConstants.warn_log_count)
   if item == "SituationsToWatchCloudController":
     line_graph_error_log_count = self.driver.find_elements_by_xpath(GuiConstants.situations_to_watch_cloud_controller_error)
     line_graph_fatal_log_count = self.driver.find_elements_by_xpath(GuiConstants.situations_to_watch_cloud_controller_fatal)
     line_graph_warn_log_count = self.driver.find_elements_by_xpath(GuiConstants.situations_to_watch_cloud_controller_warn)

     if line_graph_error_log_count and line_graph_fatal_log_count and line_graph_warn_log_count:
        self.log.info("Line Graphs are displayed in table as expected")
     else:
        self.log.error("All lie graphs are not displayed")


 def sparkline_validation_com(self):
     line_graph_connection_count = self.driver.find_elements_by_xpath(GuiConstants.line_graph_connection_count)
     line_graph_resqueue_size = self.driver.find_elements_by_xpath(GuiConstants.line_graph_resqueue_size)
     line_graph_resqueue_waiting = self.driver.find_elements_by_xpath(GuiConstants.line_graph_resqueue_waiting)
     line_graph_threadqueue_size = self.driver.find_elements_by_xpath(GuiConstants.line_graph_threadqueue_size)
     line_graph_threadqueue_waiting = self.driver.find_elements_by_xpath(GuiConstants.line_graph_threadqueue_waiting)

     if line_graph_connection_count and line_graph_resqueue_size and line_graph_resqueue_waiting and line_graph_threadqueue_size and line_graph_threadqueue_waiting:
        self.log.info("Line Graphs are displayed in table as expected")
     else:
        self.log.error("All lie graphs are not displayed")

 def sparkline_validation_etcd_health(self):
     sparkline_val_server = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[4]/div/span/span[2]/canvas")
     sparkline_val_leader = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[5]/div/span/span[2]/canvas")
     sparkline_val_rec_req = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[6]/div/span/span[2]/canvas")
     sparkline_val_send_req = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[7]/div/span/span[2]/canvas")
     sparkline_val_comp_del = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[8]/div/span/span[2]/canvas")
     sparkline_val_comp_swap = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[9]/div/span/span[2]/canvas")
     sparkline_val_create_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[10]/div/span/span[2]/canvas")
     sparkline_val_del_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[11]/div/span/span[2]/canvas")
     sparkline_val_ec = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[12]/div/span/span[2]/canvas")
     sparkline_val_gets_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[13]/div/span/span[2]/canvas")
     sparkline_val_sets_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[14]/div/span/span[2]/canvas")
     sparkline_val_update_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[15]/div/span/span[2]/canvas")
     sparkline_val_watchers = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920']/td[16]/div/span/span[2]/canvas")

     if sparkline_val_server and sparkline_val_leader and sparkline_val_rec_req and sparkline_val_send_req and sparkline_val_comp_del and sparkline_val_comp_swap and sparkline_val_create_fail and sparkline_val_del_fail and sparkline_val_ec and sparkline_val_gets_fail and sparkline_val_sets_fail and sparkline_val_update_fail and sparkline_val_watchers:
        self.log.info("Sparklines are displayed as expected")
     else:
        self.log.error("All sparkline graphs are not displayed")


 def linegraph_validation_situations_to_watch_etcd_store(self):
     sparkline_val_server = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[3]/div/span/span[2]/canvas")
     sparkline_val_leader = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[4]/div/span/span[2]/canvas")
     sparkline_val_rec_req = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[5]/div/span/span[2]/canvas")
     sparkline_val_send_req = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[6]/div/span/span[2]/canvas")
     sparkline_val_comp_del = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[7]/div/span/span[2]/canvas")
     sparkline_val_comp_swap = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[8]/div/span/span[2]/canvas")
     sparkline_val_create_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[9]/div/span/span[2]/canvas")
     sparkline_val_del_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[10]/div/span/span[2]/canvas")
     sparkline_val_ec = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[11]/div/span/span[2]/canvas")
     sparkline_val_gets_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[12]/div/span/span[2]/canvas")
     sparkline_val_sets_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[13]/div/span/span[2]/canvas")
     sparkline_val_update_fail = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[14]/div/span/span[2]/canvas")
     sparkline_val_watchers = self.driver.find_elements_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[15]/div/span/span[2]/canvas")

     if sparkline_val_server and sparkline_val_leader and sparkline_val_rec_req and sparkline_val_send_req and sparkline_val_comp_del and sparkline_val_comp_swap and sparkline_val_create_fail and sparkline_val_del_fail and sparkline_val_ec and sparkline_val_gets_fail and sparkline_val_sets_fail and sparkline_val_update_fail and sparkline_val_watchers:
        self.log.info("Sparklines are displayed as expected")
     else:
        self.log.error("All sparkline graphs are not displayed")
 def table_info_etcd(self):

     table = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']")
     if table:
        self.log.info("etcd Health Table Present as expected")
     else:
        self.log.error("Router Table not Present")

     table_value1 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]")
     table_header = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[1]")
     table_val_2 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[2]")
     table_header_2 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[2]")
     table_val_3 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[3]")
     table_header_3 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[3]")
     table_val_4 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[4]")
     table_header_4 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[4]")
     table_val_5 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[5]")
     table_header_5 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[5]")
     table_val_6 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[6]")
     table_header_6 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[6]")
     table_val_7 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[7]")
     table_header_7 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[7]")
     table_val_8 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[8]")
     table_header_8 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[8]")
     table_val_9 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[9]")
     table_header_9 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[9]")
     table_val_10 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[10]")
     table_header_10 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[10]")
     table_val_11 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[11]")
     table_header_11 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[11]")
     table_val_12 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[12]")
     table_header_12 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[12]")
     table_val_13 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[13]")
     table_header_13 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[13]")
     table_val_14 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[14]")
     table_header_14 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[14]")
     table_val_15 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[15]")
     table_header_15 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[15]")
     table_val_16 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[16]")
     table_header_16 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[16]")


     self.log.info("The values from table : %s is %s ", table_header.text, table_value1.text)
     self.log.info("The values from table : %s is %s ", table_header_2.text, table_val_2.text)
     self.log.info("The values from table : %s is %s ", table_header_3.text, table_val_3.text)
     self.log.info("The values from table : %s is %s ", table_header_4.text, table_val_4.text)
     self.log.info("The values from table : %s is %s ", table_header_5.text, table_val_5.text)
     self.log.info("The values from table : %s is %s ", table_header_6.text, table_val_6.text)
     self.log.info("The values from table : %s is %s ", table_header_7.text, table_val_7.text)
     self.log.info("The values from table : %s is %s ", table_header_8.text, table_val_8.text)
     self.log.info("The values from table : %s is %s ", table_header_9.text, table_val_9.text)
     self.log.info("The values from table : %s is %s ", table_header_10.text, table_val_10.text)
     self.log.info("The values from table : %s is %s ", table_header_11.text, table_val_11.text)
     self.log.info("The values from table : %s is %s ", table_header_12.text, table_val_12.text)
     self.log.info("The values from table : %s is %s ", table_header_13.text, table_val_13.text)
     self.log.info("The values from table : %s is %s ", table_header_14.text, table_val_14.text)
     self.log.info("The values from table : %s is %s ", table_header_15.text, table_val_15.text)
     self.log.info("The values from table : %s is %s ", table_header_16.text, table_val_16.text)


 def table_info_cloudcntrl_queue(self):

     table = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']")
     if table:
        self.log.info("etcd Health Table Present as expected")
     else:
        self.log.error("Router Table not Present")

     table_value1 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]")
     table_header = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[1]")
     table_val_2 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[2]")
     table_header_2 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[2]")
     table_val_3 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[3]")
     table_header_3 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[3]")
     table_val_4 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[4]")
     table_header_4 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/thead/tr/th[4]")
     self.log.info("The values from table : %s is %s ", table_header.text, table_value1.text)
     self.log.info("The values from table : %s is %s ", table_header_2.text, table_val_2.text)
     self.log.info("The values from table : %s is %s ", table_header_3.text, table_val_3.text)
     self.log.info("The values from table : %s is %s ", table_header_4.text, table_val_4.text)

 def graph_info(self):
     directory = "C:\\Screenshots"
     #if not os.path.exists(directory):os.mkdir(directory)

     str1 = "router_performance_graph.png"
     f_path = os.path.join(directory,str1)
     print f_path

     if os.path.isfile(f_path):
        os.remove(f_path)
     else:
        self.log.info("Cannot delete file")

     path = os.path.join(directory,str1)
     print path

     table_value1 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]")
     table_value1.click()
     self.driver.implicitly_wait(5)
     self.driver.find_elements_by_xpath(".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-d254819a-9ffc5675-7e3c4543-95e0f588-acdfbabb']")
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(path)
     self.log.info("Please find the logs under this location %s",path)

 def graph_info_common(self,filename):
     file_path = os.path.join(self.directory,filename)

     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")

     self.driver.find_element_by_xpath(".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-cc1d2e8-812f2be8-ce4e4e0d']/td[1]/div/span").click()
     self.driver.implicitly_wait(5)
     xpath = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-cc1d2e8-812f2be8-ce4e4e0d-2cb21c89']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s",file_path)


 def graph_info_etcd(self,filename):
     file_path = os.path.join(self.directory,filename)

     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")

     table_value1 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]")
     table_value1.click()
     self.driver.implicitly_wait(5)
     #xpath = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-cc1d2e8-812f2be8-ce4e4e0d-2cb21c89']"
     xpath = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-b92cc433-40f0b8a8-3f4e0920-527c9148']/div[3]"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s", file_path)
     #self.log.info("Please find the logs under this location %s",file_path

 def graph_info_cloud_controller_queue(self,filename):
     file_path = os.path.join(self.directory,filename)

     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")

     table_value1 = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']/tbody/tr/td[1]")
     table_value1.click()
     self.driver.implicitly_wait(5)
     #xpath = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-cc1d2e8-812f2be8-ce4e4e0d-2cb21c89']"
     xpath = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-d079b07b-cf0b9f8-e8d922c0']"
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)
     self.log.info("Please find the logs under this location %s", file_path)
     #self.log.info("Please find the logs under this location %s",file_path

 def graph_info_com(self,xpath,filename):
     file_path = os.path.join(self.directory,filename)

     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")

     self.driver.find_element_by_xpath(GuiConstants.click_table_cloud_controller_threads).click()
     self.driver.implicitly_wait(5)
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)


 def graph_info_cloud_controller_errors(self,xpath,filename):
     file_path = os.path.join(self.directory,filename)

     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")

     self.driver.find_element_by_xpath(GuiConstants.cloud_controller_log_errors_table).click()
     self.driver.implicitly_wait(5)
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)

 def graph_info_situations_to_watch_cloud_controller_errors(self,xpath,filename):
     file_path = os.path.join(self.directory,filename)

     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")

     self.driver.find_element_by_xpath(GuiConstants.situations_to_watch_table).click()
     self.driver.implicitly_wait(5)
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)

 def graph_info_situations_to_watch_etcd_store(self,xpath,filename):
     file_path = os.path.join(self.directory,filename)

     if os.path.isfile(file_path):os.remove(file_path)
     else:self.log.debug("Cannot delete file-File doesnot exist")

     self.driver.find_element_by_xpath(GuiConstants.situations_to_watch_table_etcd).click()
     self.driver.implicitly_wait(5)
     self.driver.find_elements_by_xpath(xpath)
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(file_path)

 def legend_item_validation_cloudcntller_queue(self):
    legend_item1 = self.driver.find_elements_by_xpath(".//*[text()='cc.job_queue_length.cc-generic' and @class='ui-button-text']")
    #legend_item2 = self.driver.find_elements_by_xpath(".//*[text()='router.responses[component=CloudController,status=3xx]' and @class='ui-button-text']")
    if legend_item1:
        self.log.info("All legend items are displayed as expected")
    else:
        self.log.error("Legeng Items aren't displayed as expected")


 def legend_item_validation(self):
    legend_item1 = self.driver.find_elements_by_xpath(".//*[text()='router.responses[component=CloudController,status=2xx]' and @class='ui-button-text']")
    legend_item2 = self.driver.find_elements_by_xpath(".//*[text()='router.responses[component=CloudController,status=3xx]' and @class='ui-button-text']")
    legend_item3 = self.driver.find_elements_by_xpath(".//*[text()='router.requests[component=CloudController]' and @class='ui-button-text']")
    legend_item4 = self.driver.find_elements_by_xpath(".//*[text()='router.responses[component=CloudController,status=4xx]' and @class='ui-button-text']")
    legend_item5 = self.driver.find_elements_by_xpath(".//*[text()='router.responses[component=CloudController,status=5xx]' and @class='ui-button-text']")
    legend_item6 = self.driver.find_elements_by_xpath(".//*[text()='router.responses[component=CloudController,status=xxx]' and @class='ui-button-text']")


    if legend_item1 and legend_item2 and legend_item3 and legend_item4 and legend_item5 and legend_item6:
        self.log.info("All legend items are displayed as expected")
    else:
        self.log.error("Legeng Items aren't displayed as expected")


 def legend_item_validation_quan_three(self):


        legend_item1 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_error)
        legend_item2 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_fatal)
        legend_item3 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_warn)


        if legend_item1 and legend_item2 and legend_item3:
            self.log.info("All legend items are displayed as expected")
        else:
            self.log.error("Legend Items aren't displayed as expected")

 def legend_item_validation_com(self,item):



    if item == "CloudControllerThread":
        legend_item1 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread1)
        legend_item2 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread2)
        legend_item3 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread3)
        legend_item4 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread4)
        legend_item5 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread5)
        legend_item6 = self.driver.find_elements_by_xpath(GuiConstants.legend_item_cloud_controller_thread6)


    if legend_item1 and legend_item2 and legend_item3 and legend_item4 and legend_item5 and legend_item6:
        self.log.info("All legend items are displayed as expected")
    else:
        self.log.error("Legend Items aren't displayed as expected")


 def logout_mnr_dashboard(self):
     self.driver.find_element_by_xpath("//*[@title='Logout']").click()

 def login_kibana_ui(self,url):
    """
	@author: aarthi
	Logins to Kibana Dashboard
	"""
    self.driver = Firefox()
    self.driver.get(url)
    self.driver.implicitly_wait(10)
    self.driver.find_element_by_xpath(".//*[text()='Settings']").click()
    self.driver.implicitly_wait(5)
    self.driver.find_element_by_xpath(".//*[text()='Advanced']").click()

 def sort_by_date(self):
     """
	   @author: aarthi
	   Kibana UI-> Change the settings from boolean to date
	 """
     self.driver.find_element_by_xpath("//*/tbody/tr[2]/td[3]/button[1]").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath("//*/tbody/tr[2]/td[2]/form/textarea").clear()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath("//*/tbody/tr[2]/td[2]/form/textarea"). \
         send_keys('{ "unmapped_type": "date" }')
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath("//*/tbody/tr[2]/td[3]/button[1]").click()

 def verify_new_user_log_added(self,username):
     """
	   @author: aarthi
	   @param: username: user added
	   Kibana UI-> Discover Tab-> searches for the string provided and returns the latest value
	 """
     self.driver.find_element_by_xpath(".//*[text()='Discover']").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath('//*[@type="text" and @aria-label="Search input"]').clear()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath('//*[@type="text" and @aria-label="Search input"]'). \
         send_keys(username)
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath('//*[@type="submit" and @aria-label="Search"]').click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath("//*/table/tbody/tr[1]/td[3]")


 def verify_alert_created(self, alert_sev, alert_comp):
     '''
     This module will verify if an alert is created or not when you
     give the severity and component name of the alert you are looking for
     :param alert_sev: This can be CRITICAL|MAJOR|MINOR
     :param alert_comp: This will be the component name of the alert
     :return: None
     '''
     try:
         if self.driver:
             self.driver.find_element_by_link_text("Report Library").click()
             self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b']/span").click()
             self.driver.implicitly_wait(5)
             self.driver.find_element_by_link_text("NHC Reports").click()
             self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
             self.driver.implicitly_wait(5)
             self.driver.find_element_by_link_text("Alerts").click()
             self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-467fd402']/span").click()
             self.driver.implicitly_wait(5)
             self.driver.find_element_by_link_text("Alerts Summary").click()
             self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-467fd402-b7c36fe2']/span").click()
             self.driver.implicitly_wait(5)
             self.driver.find_element_by_link_text("Alerts by Severity").click()
             self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-467fd402-b7c36fe2-1f9f1408']/span").click()
             self.driver.implicitly_wait(5)
             if "MAJOR" in alert_sev:
                self.driver.find_element_by_link_text("MAJOR").click()
                self.driver.find_element_by_xpath(
                     ".//*[@id='node-0-t62ce62219462574b-ffffffef-467fd402-b7c36fe2-1f9f1408-30961dc3']/span").click()
                self.driver.implicitly_wait(5)
                (table_head, table_data) = self.table_info()
             elif "CRITICAL" in alert_sev:
                 self.driver.find_element_by_link_text("CRITICAL").click()
                 self.driver.find_element_by_xpath(
                     ".//*[@id='node-0-t62ce62219462574b-ffffffef-467fd402-b7c36fe2-1f9f1408-b56efc3c']/span").click()
                 (table_head, table_data) = self.table_info()
             self.driver.implicitly_wait(15)
             # split table data to list of table rows
             found = 0
             for row_list in [table_data[i:i+len(table_head)] for i  in range(0, len(table_data), len(table_head))]:
                if alert_comp in row_list:
                    found = 1
                    for (head, data) in zip(table_head, row_list):
                        self.log.info("The values from table : %s is %s ", head, data)
             if not found:
                 self.log.error("Alert is not found")
     except Exception as e:
         self.log.error("Exception found %s", format(e))

 def table_info(self):
    '''
    This will extract table information in the current page
    :return: This will return 2 lists, one for header and one for data
    '''
    self.log.info("inside table_info")
    table = self.driver.find_element_by_xpath(".//table[@class='content-table dataTable no-footer']")
    if table:
        self.log.info("Table Present as expected")
    else:
        self.log.error("Table not Present")

    #get no of rows in table
    row_count = len(self.driver.find_elements_by_xpath(
                ".//table[@class='content-table dataTable no-footer']/tbody/tr"))
    #print row_count
    # get no of columns in table
    column_count = len(self.driver.find_elements_by_xpath(
        ".//table[@class='content-table dataTable no-footer']/tbody/tr[1]/td"))
    #print column_count
    # get list of headers of table
    # divided xpath In three parts  to pass Row_count and Col_count values.
    table_header_list = []
    first_part = ".//table[@class='content-table dataTable no-footer']/thead/tr/th["
    second_part = "]/div/a"
    for i in range(column_count):
        i += 1
        #prepared final xpath
        final_xpath = first_part+str(i)+second_part
        table_head = self.driver.find_element_by_xpath(final_xpath)
        self.log.info(table_head.text)
        table_header_list.append(table_head.text)
    #divided xpath In three parts  to pass Row_count and Col_count values.
    first_part = ".//table[@class='content-table dataTable no-footer']/tbody/tr["
    second_part = "]/td["
    third_part = "]"
    # Used for loop for number of rows.
    table_data_list = []
    for i in range(row_count):
        i += 1
        # Used for loop for number of columns.
        for j in range(column_count):
            j += 1
            # Prepared final xpath of specific cell as per values of i and j.
            final_xpath = first_part+str(i)+second_part+str(j)+third_part
            # Will retrieve value from located cell and print It.
            table_data = self.driver.find_element_by_xpath(final_xpath)
            self.log.info(table_data.text)
            table_data_list.append(table_data.text)
    return (table_header_list, table_data_list)

 def print_table(self, table_head, table_data):
     '''
     This module will just print the table info in readable format
     :param table_head: table header list
     :param table_data: table data list
     :return: None
     '''
     self.log.info("inside print table")
     for row_list in [table_data[i:i + len(table_head)] for i in range(0, len(table_data), len(table_head))]:
         for (head, data) in zip(table_head, row_list):
             self.log.info("The values from table : %s is %s ", head, data)

 def close_browser(self):
     self.driver.quit()

 def close_firefox(self):
     os.system("TASKKILL /F /IM firefox.exe")
     self.log.info("Done")

 def click_alert_definitions(self):
     '''
     This module will click the PCF Alert Definitions
     :return: None
     '''
     self.driver.find_element_by_link_text("Local Manager").click()
     self.driver.find_element_by_xpath(".//*[@id='node-TG9jYWwgTWFuYWdlcg']/a").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Alert definitions").click()
     self.driver.find_element_by_xpath(".//*[@id='node-TG9jYWwgTWFuYWdlcg-YWxlcnRz']/span").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("PCF").click()
     self.driver.find_element_by_xpath(".//*[@id='node-TG9jYWwgTWFuYWdlcg-YWxlcnRz-Zi1QQ0Y']/span").click()
     self.driver.implicitly_wait(5)

 def login_alerting_page(self, mnr_ip):
     '''
     This module will login to the alerting frontend page
     :param mnr_ip: IP address of mnr VM
     :return: None
     '''
     url = "http://" + mnr_ip + ":58080/alerting-frontend/"
     username = "admin"
     password = "changeme"
     self.login_mnr_dashboard(url,username,password)
     self.driver.implicitly_wait(10)

 def click_component_alert_definition(self, alert_component):
     '''
     This module will click to the given alert definition under PCF
     :param alert_component: The component name of an alert
     :return: None
     '''
     self.log.info(alert_component)
     self.driver.find_element_by_link_text(alert_component).click()
     self.driver.implicitly_wait(5)

 def read_component_alert_definition(self, severity):
     '''
     This module will read the threshold value of the given severity
     :param severity: This can be CRITICAL|MAJOR|MINOR
     :return: This will return threshold value
     '''
     self.log.info(severity)
     if 'CRITICAL' in severity:
         alert_threshold = self.driver.find_element_by_xpath(".//form/div[1]/div/div[1]/input")
     elif 'MAJOR' in severity:
         alert_threshold = self.driver.find_element_by_xpath(".//form/div[2]/div/div[1]/input")
     elif 'MINOR' in severity:
         alert_threshold = self.driver.find_element_by_xpath(".//form/div[3]/div/div[1]/input")
     else:
         self.log.error("severity is not valid, should be one of 'CRITICAL, MAJOR, MINOR' but got %s") %severity
         return
     threshold = alert_threshold.get_attribute('value')
     self.log.info("threshold %s", threshold)
     return threshold

 def set_component_alert_definition(self, severity, threshold):
     '''
     This module will set the threshold value of the given severity
     :param severity: This can be CRITICAL|MAJOR|MINOR
     :param threshold: This is the threshold value need to be set
     :return: None
     '''
     self.log.info(severity)
     if 'CRITICAL' in severity:
        alert_threshold = self.driver.find_element_by_xpath(".//form/div[1]/div/div[1]/input")
     elif 'MAJOR' in severity:
        alert_threshold = self.driver.find_element_by_xpath(".//form/div[2]/div/div[1]/input")
     elif 'MINOR' in severity:
        alert_threshold = self.driver.find_element_by_xpath(".//form/div[3]/div/div[1]/input")
     else:
        self.log.error("severity is not valid, should be one of 'CRITICAL, MAJOR, MINOR' but got %s") % severity
     alert_threshold.clear()
     alert_threshold.send_keys(threshold)
     self.driver.find_element_by_xpath("//*[@title='save edited configuration']").click()
     self.driver.implicitly_wait(5)

     ######Sudarshan###########

 def pcf_serviceplans(self):
     '''
          author: Sudarshan
          :This method verify's serviceplans under pcfInventory
          '''
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-af4c0bf4']/span").click()
     self.driver.implicitly_wait(10)
     time.sleep(5)
     self.driver.find_element_by_xpath(".//*[@title='bronze']").click()

 def pcf_runtime_resources(self):
     '''author: Sudarshan
     :This method verify's services under pcfRuntimeresources
     '''
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-4cff162a']/span").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-4cff162a-925211fa']").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         ".//*[@id='l0-t62ce62219462574b-ffffffef-4cff162a-925211fa-115f93c4']/td[4]/div/span/span[2]/canvas")

 def physical_host_info(self):
     '''author: Sudarshan
     :This method verify's hostinfo under physical host and checks the sparkline.
      '''
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-hec5dbf0c996e70a3']/span").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-hec5dbf0c996e70a3-ad496bc0']").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         ".//*[@id='l0-t62ce62219462574b-hec5dbf0c996e70a3-ad496bc0-409669a5']/td[9]/div/span/span[2]/canvas")

 def nhc_centric(self, url):
     '''author: Sudarshan
     :This method navigates to nhc_centric in kibana UI
          '''
     self.driver = Firefox()
     self.driver.maximize_window()
     self.driver.get(url)
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[text()='Visualize']").click()
     self.driver.implicitly_wait(5)

 def navigate_to_url(self, url):
     '''author: Sudarshan
     :This method navigates to specified url.
          '''
     self.driver.get(url)
     self.driver.implicitly_wait(10)
     self.driver.maximize_window()

 def pcf_data_memory(self, filename):
     '''author: Sudarshan
     :This method gives the usage report after pcf login.
          '''
     directory = "C:\\Screenshots"
     path = os.path.join(directory, filename)
     self.driver.find_element_by_xpath("//*[@class='close']").click()
     time.sleep(10)
     self.driver.find_element_by_xpath(
         "//*[@href='/organizations/f59d3580-0c00-4864-a87c-8f24b0f76512/usage_report']").click()
     self.driver.implicitly_wait(10)
     time.sleep(10)
     self.driver.save_screenshot(path)

 def pcfinventory_services(self):
     '''author: Sudarshan
          :This method verify's services under pcfInventory
          '''
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-3da45eae']/span").click()
     self.driver.find_element_by_xpath(
         ".//*[@id='node-0-t62ce62219462574b-ffffffef-2c25ea99-3da45eae-8acf8fca']/span").click()
     self.driver.implicitly_wait(5)
     time.sleep(5)
     self.driver.find_element_by_xpath(".//*[@title='Applications']").click()

 def screenshot(self, filename):
     '''author: Sudarshan
          :This method is used to save screenshot.
          '''
     directory = "C:\\Screenshots"
     path = os.path.join(directory, filename)
     self.driver.save_screenshot(path)

 def validate_visual_hosts(self):
     '''author: Sudarshan
     :This method is used to validate the visual hosts.
          '''
     self.driver.find_element_by_xpath("html/body/div[2]/div/div/div/div/div/div/span")

 def discover_nhc_hosts(self, filename):
     '''author: Sudarshan
          :This method is used to discover nhc_hosts and verify nhc_host logs.
          '''
     directory = "C:\\Screenshots"
     path = os.path.join(directory, filename)
     self.driver.find_element_by_xpath('//*[@class="ng-scope" and @aria-label="Load Saved Search"]').click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         "html/body/div[2]/div/div/config/div/div[1]/form/saved-object-finder/paginate/ul/a[2]/li").click()
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(path)
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         "html/body/div[2]/div/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/doc-table/div[2]/table/thead/th[3]/span[1]").click()

 def discover_pcf_hosts(self, filename):
     '''author: Sudarshan
               :This method is used to discover pcf_hosts and verify pcf logs.
               '''
     directory = "C:\\Screenshots"
     path = os.path.join(directory, filename)
     self.driver.find_element_by_xpath('//*[@class="ng-scope" and @aria-label="Load Saved Search"]').click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         "html/body/div[2]/div/div/config/div/div[1]/form/saved-object-finder/paginate/ul/a[3]/li").click()
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(path)
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         "html/body/div[2]/div/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/doc-table/div[2]/table/thead/th[3]/span[1]").click()

 def discover_all_hosts(self, filename):
     '''author: Sudarshan
               :This method is used to discover all_hosts and verify all hosts  logs.
               '''
     directory = "C:\\Screenshots"
     path = os.path.join(directory, filename)
     self.driver.find_element_by_xpath('//*[@class="ng-scope" and @aria-label="Load Saved Search"]').click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         "html/body/div[2]/div/div/config/div/div[1]/form/saved-object-finder/paginate/ul/a[1]/li").click()
     self.driver.implicitly_wait(5)
     self.driver.save_screenshot(path)
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(
         "html/body/div[2]/div/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/doc-table/div[2]/table/thead/th[3]/span[1]")

 def login_horizon_dashboard(self, url, domain, username, password):
     '''author: Sudarshan
               :This method is to login to horizon.
               '''
     self.driver = Firefox()
     self.driver.maximize_window()
     self.driver.get(url)
     self.driver.implicitly_wait(2)
     domain = domain
     username = username
     password = password
     self.driver.find_element_by_id('id_domain'). \
         send_keys(domain)
     self.driver.find_element_by_id('id_username'). \
         send_keys(username)
     self.driver.implicitly_wait(2)
     self.driver.find_element_by_id('id_password'). \
         send_keys(password)
     self.driver.implicitly_wait(2)
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath("//*[text()='Sign In']").click()

 def logout_horizon(self):
     '''author: Sudarshan
               :This method is used to logout of horizon.
               '''
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_id('profile_editor_switcher').click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath("//*[@href='/horizon/auth/logout/']").click()

     ########Sudarshan#########

 def Blobstore_Capacity_Utilization_Graph(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to identify the Blobstore Capacity Utilization element
     """
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-36f535dc']/span").click()
     self.driver.find_element_by_xpath(
         ".//*[@id='node-0-t62ce62219462574b-ffffffef-2c4856fb-36f535dc-68d769b8']/a").click()
     element = self.driver.find_element_by_xpath(
         ".//*[@id='gHH0mdv0weIKGVJLzW0PzRRjsciyNbLuTP5zJ5ZbGi8EXQySADMNOMP5QuCeKzDyVe6f4UMHPWjy7dT5G9HHIlGwXNAtZD7FRM9fzXNob6uLij2f4hW4HJQTHs4J07FHJ']")
     if element:
         self.log.info("Blobstore Capacity Utilization Graph exists")
     else:
         self.log.error("Blobstore Capacity Utilization Graph does not exists")

 def drilldown_till_pcfoperations(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to drill down till PCF Operations Report
     """
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa']/span").click()

 def navigate_to_etcd_store_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the etcd Store Report
     """
     self.driver.find_element_by_link_text("etcd Store").click()

 def navigate_to_RouterHealth_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Router Health Report
     """
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-d774a820']/span").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Router Health").click()

 def navigate_to_RouterResponses_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Router Responses Report
     """
     self.driver.find_element_by_link_text("Router Responses").click()

 def navigate_to_RouterPerformance_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Router Performance Report
     """
     self.driver.find_element_by_link_text("Router Performance").click()

 def navigate_to_CloudControllerHealth_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Cloud Controller Report
     """
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-925211fa']/span").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Cloud Controller Health").click()

 def navigate_to_CloudControllerResponses_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Cloud Controller Responses
     """
     self.driver.find_element_by_link_text("Cloud Controller Responses").click()

 def navigate_to_CloudControllerQueues_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Cloud Controller Queues
     """
     self.driver.find_element_by_link_text("Cloud Controller Queues").click()

 def navigate_to_CloudControllerThreads_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Cloud Controller Threads
     """
     self.driver.find_element_by_link_text("Cloud Controller Threads").click()

 def navigate_to_CloudControllerLogErrors_page(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Cloud Controller Log Errors
     """
     self.driver.find_element_by_link_text("Cloud Controller Log Errors").click()

 def navigate_to_DiegoBrainAuctioneer(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Diego Brain Auctioneer
     """
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-b9684433']/span").click()
     self.driver.find_element_by_xpath(
         ".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-b9684433-b462fff1']/span").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Diego Brain Auctioneer").click()

 def navigate_to_DiegoBrainRoutes(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Diego Brain Routes
     """
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Diego Brain Routes").click()

 def navigate_to_DiegoDatabase(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Diego Database
     """
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Diego Database").click()

 def navigate_to_DiegoCellContainer(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Diego Cell Container
     """
     self.driver.find_element_by_xpath(
         ".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-b9684433-58ea42bc']/span").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Diego Cell Container").click()

 def navigate_to_DiegoCellDisk(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Diego Cell Disk
     """
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Diego Cell Disk").click()

 def navigate_to_DiegoCellMemory(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to navigate to the Diego Cell Memory
     """
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_link_text("Diego Cell Memory").click()

 def validate_DiegoCellVMIPs(self, DiegoCellVM1IP, DiegoCellVM2IP, DiegoCellVM3IP):
     """
     @author: venkateswara prasad guntupalli
     this method is to validate MNR Diego Cell Table VM IPs with the PCF OPS Manager DiegoCell VM IPs
     Args:
        DiegoCellVM1IP: DiegoCell VM1 IP address from PCF OPS Manager
        DiegoCellVM2IP: DiegoCell VM2 IP address from PCF OPS Manager
        DiegoCellVM3IP: DiegoCell VM3 IP address from PCF OPS Manager
     """
     self.driver.implicitly_wait(5)
     IPAddressColumnText = self.driver.find_element_by_xpath(
         ".//table[@class='content-table dataTable no-footer']/thead/tr/th[2]/div/a").text
     if IPAddressColumnText == "IP Address":
         self.log.info("IP Address coulmn exists in Diego Cell Table Header")
     else:
         self.log.info("IP Address coulmn doesn't exists in Diego Cell Table Header")

     self.driver.implicitly_wait(5)
     VM1IPAddress = self.driver.find_element_by_xpath(
         ".//table[@class='content-table dataTable no-footer']/tbody/tr[2]/td[2]/div/span").text
     print VM1IPAddress
     if VM1IPAddress:
         self.log.info("VM1 IP Address exists in Table Header %s ", VM1IPAddress)
         if VM1IPAddress == DiegoCellVM1IP:
             self.log.info("DiegoCellVM1 IP Address matches with IP Address in PCF OPS Manager")
         else:
             self.log.error("DiegoCellVM1 IP Address does not matches with IP Address in PCF OPS Manager")
     else:
         self.log.error("VM1 IP Address doesn't exists in Table Header")

     self.driver.implicitly_wait(5)
     VM2IPAddress = self.driver.find_element_by_xpath(
         ".//table[@class='content-table dataTable no-footer']/tbody/tr[1]/td[2]/div/span").text
     print VM2IPAddress
     if VM2IPAddress:
         self.log.info("VM2 IP Address exists in Table Header %s ", VM2IPAddress)
         if VM2IPAddress == DiegoCellVM2IP:
             self.log.info("DiegoCellVM2 IP Address matches with IP Address in PCF OPS Manager")
         else:
             self.log.error("DiegoCellVM2 IP Address does not matches with IP Address in PCF OPS Manager")
     else:
         self.log.error("VM2 IP Address doesn't exists in Table Header")

     self.driver.implicitly_wait(5)
     VM3IPAddress = self.driver.find_element_by_xpath(
         ".//table[@class='content-table dataTable no-footer']/tbody/tr[3]/td[2]/div/span").text
     print VM3IPAddress
     if VM3IPAddress:
         self.log.info("VM3 IP Address exists in Table Header %s ", VM3IPAddress)
         if VM3IPAddress == DiegoCellVM3IP:
             self.log.info("DiegoCellVM3 IP Address matches with IP Address in PCF OPS Manager")
         else:
             self.log.error("DiegoCellVM3 IP Address does not matches with IP Address in PCF OPS Manager")
     else:
         self.log.error("VM3 IP Address doesn't exists in Table Header")

 def getIPAddressfromPCFOperationsTable(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch IP address value from the first row of the PCF Operations table in the navigated page.
     """
     self.driver.implicitly_wait(5)
     IPAddressColumnText = self.driver.find_element_by_xpath(
         ".//table[@class='content-table dataTable no-footer']/thead/tr/th[2]/div/a").text
     if IPAddressColumnText == "IP Address":
         self.log.info("IP Address coulmn exists in Table Header")
     else:
         self.log.info("IP Address coulmn doesn't exists in etcd Table Header")
     self.driver.implicitly_wait(5)
     IPAddress = self.driver.find_element_by_xpath(
         ".//table[@class='content-table dataTable no-footer']/tbody/tr/td[2]/div/span").text
     if IPAddress:
         self.log.info("IP Address exists in Table Header %s ", IPAddress)
         return IPAddress
     else:
         self.log.info("IP Address doesn't exists in Table Header")
         return False

 def login_pivotal(self, url_ops, username_ops, password_ops):
     """
     @author: venkateswara prasad guntupalli
     this method is to login to the PCF OPS Manager portal & navigate to Pivotal Elastic Runtime tile -> Status tab
     Args:
         url_ops: PCF OPS Manager URL
         username_ops: PCF OPS Manager username
         password_ops: PCF OPS Manager password
         
     """
     self.driver.get(url_ops)
     self.driver.implicitly_wait(15)
     ref = self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[1]")
     ref.send_keys(username_ops)
     self.driver.implicitly_wait(10)
     ref = self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[2]")
     ref.send_keys(password_ops)
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[3]").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[@id='show-cf-configure-action']").click()
     self.driver.implicitly_wait(5)
     self.driver.find_element_by_xpath(".//*[@id='show-status-action']").click()
     self.driver.implicitly_wait(10)

 def getetcdIPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch etcd VM IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     etcdIPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[3]/td[3]").text
     if etcdIPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for etcd in Ops Manager %s ", etcdIPAddressValue_fromOPSManager)
         return etcdIPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for etcd in Ops Manager")
         return False

 def getRouterIPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch Router VM IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     RouterIPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[6]/td[3]").text
     if RouterIPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for Router in Ops Manager %s ", RouterIPAddressValue_fromOPSManager)
         return RouterIPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for Router in Ops Manager")
         return False

 def getCloudControllerIPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch Cloud Controller VM IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     CloudControllerIPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[9]/td[3]").text
     if CloudControllerIPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for Cloud Controller in Ops Manager %s ",
                       CloudControllerIPAddressValue_fromOPSManager)
         return CloudControllerIPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for Cloud Controller in Ops Manager")
         return False

 def getDiegoBrainIPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch Diego Brain VM IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     DiegoBrainIPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[15]/td[3]").text
     if DiegoBrainIPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for Diego Brain in Ops Manager %s ", DiegoBrainIPAddressValue_fromOPSManager)
         return DiegoBrainIPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for Diego Brain in Ops Manager")
         return False

 def getDiegoCellVM1IPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch Diego Cell VM1 IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     DiegoCellVM1IPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[16]/td[3]").text
     if DiegoCellVM1IPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for Diego CellVM1 in Ops Manager %s ",
                       DiegoCellVM1IPAddressValue_fromOPSManager)
         return DiegoCellVM1IPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for Diego CellVM1 in Ops Manager")
         return False

 def getDiegoCellVM2IPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch Diego Cell VM2 IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     DiegoCellVM2IPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[17]/td[2]").text
     if DiegoCellVM2IPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for Diego CellVM2 in Ops Manager %s ",
                       DiegoCellVM2IPAddressValue_fromOPSManager)
         return DiegoCellVM2IPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for Diego CellVM2 in Ops Manager")
         return False

 def getDiegoCellVM3IPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch Diego Cell VM3 IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     DiegoCellVM3IPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[18]/td[2]").text
     if DiegoCellVM3IPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for Diego CellVM3 in Ops Manager %s ",
                       DiegoCellVM3IPAddressValue_fromOPSManager)
         return DiegoCellVM3IPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for Diego CellVM3 in Ops Manager")
         return False

 def getDiegoDatabaseIPAdressfromPCFOpsManger(self):
     """
     @author: venkateswara prasad guntupalli
     this method is to fetch Diego Database IP address value from PCF OPS Manager.
     """
     time.sleep(15)
     DiegoDatabaseIPAddressValue_fromOPSManager = self.driver.find_element_by_xpath(
         ".//*[@id='cf-6174b334269c3e4e2241-status-table']/tbody/tr[4]/td[3]").text
     if DiegoDatabaseIPAddressValue_fromOPSManager:
         self.log.info("IP Address exists for Diego Database in Ops Manager %s ",
                       DiegoDatabaseIPAddressValue_fromOPSManager)
         return DiegoDatabaseIPAddressValue_fromOPSManager
     else:
         self.log.info("IP Address does not exists for Diego Database in Ops Manager")
         return False

############Dayananda#########################
 def read_and_validate(self):
     '''
     Author:Dayananda D R
     read and validate whether table headers are having respective values in all the tables
     '''
     #self.driver=driver
     #time.sleep(2)
     list_xpath=[]
     table_head,table_data=self.table_info()
     self.custom(table_head,table_data)
     #time.sleep(1)
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-e32d3628']/a").click()
     #time.sleep(1)
     self.driver.find_element_by_xpath(".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-e32d3628-c7eaf1c3']/div[1]/h2/span").click()
     #time.sleep(1)
     table_head,table_data=self.table_info()
     self.custom(table_head,table_data)
     #time.sleep(3)
     list_xpath=["d079b07b']/a","1a64743e']/a","b5786efe']/a"]
     for i in list_xpath:
         self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-"+str(i)).click()
         #time.sleep(3)
         table_head,table_data=self.table_info()
         self.custom(table_head,table_data)
         #time.sleep(3)
     #self.close_browser()
     return self.driver

 def drill_down_service_org(self):
     '''
     Author:Dayananda
     Navigating to Drill down service organisation.
     '''
     #self.driver.implicitly_wait(10)
     time.sleep(1)
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.find_element_by_link_text("PCF Operations").click()
     self.driver.implicitly_wait(10)
     time.sleep(1)
     self.driver.find_element_by_xpath(".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8']/div[1]/h3/span").click()
     time.sleep(1)
     return self.driver

 def drill_down_pcf_run_time_resource(self):
     '''
     Author:Dayananda
     Navigating to PCF Run time resources
     '''	 
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b']/span").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath("//*[@id='node-0-t62ce62219462574b-ffffffef']/span").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[@id='node-0-t62ce62219462574b-ffffffef-4cff162a']/a").click()
     self.driver.implicitly_wait(10)
     time.sleep(3)
    #self.driver.find_element_by_xpath(".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8']/div[1]/h3/span").click()
    #time.sleep(2)
 def read_table_value(self):
     '''
     Author:Dayananda
     customised read_table_value for my test cases
     '''
     table_head,table_data=self.table_info()
     self.custom(table_head,table_data)
     time.sleep(5)
     #test.close_browser()

 def login_pivotal_dashboard(self,ops_manager_ip,username,password):
     '''
     Author:Dayananda
     logging into pivotal Dashboard and Ops Manager Dashboard
     '''
     #ops_manager_ip
     #self.log.info("Logging into Pivotal Dashboard")
     self.username=username
     self.password=password
     url="http://"+ops_manager_ip+"/uaa/login"
     #self.driver=webdriver.Firefox()
     self.driver.implicitly_wait(10)
     self.driver.get(url)
     self.driver.implicitly_wait(10)
     ref=self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[1]")
     ref.send_keys(username)
     self.driver.implicitly_wait(10)
     ref=self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[2]")
     ref.send_keys(password)
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[3]").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[@id='tile-1']/a/div").click()
     self.driver.implicitly_wait(10)
     self.driver.close()
     self.driver.switch_to_window(self.driver.window_handles[-1])
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[@id='show-cf-configure-action']/div[2]/h3").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_id("show-domains-action").click()
     self.driver.implicitly_wait(10)
     ref=self.driver.find_element_by_xpath(".//*[@id='new_tempest_form_renderers_form']/div[1]/div[1]/input")
     system_domain =ref.get_attribute("value")
     self.driver.find_element_by_link_text("Credentials").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[@id='.uaa.admin_credentials']").click()
     j=self.driver.find_element_by_xpath("xhtml:html/xhtml:body/xhtml:pre")
     credentials= j.text
     credentials=str(credentials)
     c1=credentials.split(",")
     c2=c1[2]
     c3=c2.split(":")
     c4=c3[1]
     regex = re.compile('[^a-zA-Z0-9]')
     pwd = regex.sub('', c4)
     url="login."+system_domain
     self.driver.get(url)
     self.driver.implicitly_wait(10)
     ref=self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[1]")
     ref.send_keys("admin")
     ref=self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[2]")
     ref.send_keys(pwd)
     self.driver.find_element_by_xpath("html/body/div[1]/div[2]/div/form/input[3]").click()
     self.driver.implicitly_wait(10)
     self.driver.find_element_by_xpath(".//*[@id='tile-1']/a/div").click()
     self.driver.close()
     self.driver.switch_to_window(self.driver.window_handles[-1])
     self.driver.implicitly_wait(10)
     #time.sleep(10)
 def usage_report(self):
     '''
     Author:Dayananda
     Reading and validating Usage Report value in APP PCF .
     '''
     time.sleep(5)
     self.driver.find_element_by_xpath(".//*[@id='quota']/div[1]/div[2]/div/a").click()
     #self.driver.implicitly_wait(10)
     time.sleep(30)
     val1=self.driver.find_element_by_xpath("html/body/div[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div")
     val1=val1.text
     #print "The value of upper value",val1
     self.log.info("The value of System memory usage is %s",val1)
     #self.driver.implicitly_wait(10)
     val2=self.driver.find_element_by_xpath("html/body/div[1]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/ul/li[2]/div/div[2]")
     val2=val2.text
     #print "The value of lower value",val2
     self.log.info("The value of App Usage is %s",val2)
     if val1==val2:
         self.log.info("The value of System memory usage is equal to the value of App Usage Value")
     else:
         self.log.error("The value of System memory usage is not equal to the value of App Usage Value")
     #self.log.info("The value of App memory usage is %s",val2)


 def read_app_total_memory(self):
     '''
     Author:Dayananda
     It clicks on the app total memory and waits for 10 seconds...sleep satements are mandatory hence I used it.
     '''
     time.sleep(5)
     self.driver.find_element_by_xpath(".//*[@id='spaces_tab']/div/ul/li[5]/a/div/div/h4").click()
     time.sleep(10)
 	
 def custom(self, table_head, table_data):
     '''
	 @Author:Dayananda D R
     This module will just print the table info in readable format
     :param table_head: table header list
     :param table_data: table data list
     :return: None
     '''
     self.log.info("inside print table")
     for row_list in [table_data[i:i + len(table_head)] for i in range(0, len(table_data), len(table_head))]:
         if row_list[1] =="":
             self.log.error("Ip address field doesnot contain value")
             sys.exit(0)
         else:
             self.log.info("Ip addess field has value : %s", row_list[1])
         for (head, data) in zip(table_head, row_list):
             self.log.info("The values from table : %s is %s ", head, data)
##############End Of Dayananda#########################