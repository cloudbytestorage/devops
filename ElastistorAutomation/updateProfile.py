#------------------------------------------------------------------------------
#!/usr/bin/env python
#title           :updateProfile.py
#description     :These methods will help to perform regular actions is Elasticenter.
#note            :These methods are written using EC of P5 1.4.0.1089 build.
#author          :Swarnalatha
#date            :2017/07/29
#version         :1
#usage           :python HA_updateProfile.py
#notes           :
#python_version  :2.7.12
#==============================================================================

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import time
from selenium.common.exceptions import NoSuchElementException
from Config import GuiConfig as const
import logging

class WebUtils():
    def __init__(self):
        self.driver = webdriver.Firefox()
        #System.setProperty("webdriver.chrome.driver", "E:/Chromdriver/chromedriver.exe");
        path_to_ff_proifle = "C:\\Users\\cloudbyte\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\pb5vjcuq.default-1492595518029"
        print path_to_ff_proifle
        self.fp = webdriver.FirefoxProfile(path_to_ff_proifle)
        #self.driver = webdriver.Chrome("E:\\Chromdriver\\chromedriver.exe")


    def login_EC(self, url, username, initialpassword):
        '''Arguments:
                url = url to reach EC
                username = "username to login"
                password = "password to login" '''
        try:
            self.driver.implicitly_wait(2)
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            emailElem = self.driver.find_element_by_xpath(".//*[@class='login-raw']/input")
            ActionChains(self.driver).move_to_element(emailElem).send_keys(username).perform()
            pyautogui.press("tab")
            time.sleep(2)
            pswd = self.driver.find_element_by_xpath(".//*[@class='login-raw field username']/input")
            ActionChains(self.driver).move_to_element(pswd).send_keys(initialpassword).perform()
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.press("enter")
        except NoSuchElementException as e1:
            print "Error: Login", str(e1)


    def update_Profile(self, newpassword, confirmpassword, firstname, lastname, emailid, phoneno, orgname):
        ''' Arguments:
        newpassword: set new password for EC
        confirmpassword: confirm password
        firstname: first name of the user
        lastname: last name of the user
        emaild: emaild of the user
        phoneno: phoneno of the user
        orgname: users orgnization name'''

        try:
            self.driver.find_element_by_id("password").send_keys(newpassword)
            self.driver.find_element_by_id("password-confirm").send_keys(confirmpassword)
            self.driver.find_element_by_id("firstName").send_keys(firstname)
            self.driver.find_element_by_id("lastName").send_keys(lastname)
            self.driver.find_element_by_id("emailId").send_keys(emailid)
            self.driver.find_element_by_id("phoneNumber").send_keys(phoneno)
            self.driver.find_element_by_id("organizationName").send_keys(orgname)
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.press("enter")


        except NoSuchElementException as e1:
            print "Error:  updateProfile", str(e1)
            raise
def main():
        username = const.username
        initialpassword = const.initialpassword
        url = const.url
        t = WebUtils()
        t.login_EC(url, username, initialpassword)
        time.sleep(2)
        newpassword = const.newpassword
        confirmpassword = const.confirmpassword
        firstname = const.firstname
        lastname = const.lastname
        emailid = const.emailid
        phoneno = const.phoneno
        orgname = const.orgname
        t.update_Profile(newpassword, confirmpassword, firstname, lastname, emailid, phoneno, orgname)

if __name__ == '__main__':
    main()
