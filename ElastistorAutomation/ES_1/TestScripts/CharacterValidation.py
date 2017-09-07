#------------------------------------------------------------------------------
#!/usr/bin/env python
#title           :WebUtils.py
#description     :These methods will help for regular actions is Elasticenter.
#note            :These methods are written using EC of P5 1.4.0.1089 build.
#author          :Sudarshan Darga
#date            :2017/07/26
#version         :1
#usage           :python WebUtils.py
#notes           :
#python_version  :2.7.12
#==============================================================================

from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import *
from selenium.common.exceptions import NoAlertPresentException, WebDriverException, NoSuchElementException
import time
import pyautogui

class CharacterValidation():
    def __init__(self):
        self.driver = Firefox()

    def login_EC(self, url, username, password):
        try:
            self.driver.implicitly_wait(2)
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            emailElem = self.driver.find_element_by_xpath(".//*[@class='login-raw']/input")
            ActionChains(self.driver).move_to_element(emailElem).send_keys(username).perform()
            pyautogui.press("tab")
            pswd = self.driver.find_element_by_xpath(".//*[@class='login-raw field username']/input")
            ActionChains(self.driver).move_to_element(pswd).send_keys(password).perform()
            pyautogui.press("tab")
            pyautogui.press("enter")
        except NoSuchElementException as e1:
            print "Error:", str(e1)

    def pool_name(self,stripe,no_of_disks):
        allowed_name = "Abcdefghij1234567890-_CB"
        more_char = "Abcdefghij1234567890-_CB5"
        invalid_char = "Abcdefghij!@#$%^&*()"
        try:
            pool = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[6]")
            self.driver.execute_script("$(arguments[0]).click();", pool)
            addpool = self.driver.find_element_by_xpath(".//*[@class='action add reduced-hide']/a")
            self.driver.execute_script("$(arguments[0]).click();", addpool)
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@title='Select a Node']/select").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@title='Select a Site']/select/option[1]").click()
            self.driver.implicitly_wait(5)
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(more_char)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Please enter no more than 24 characters."
                if text1 == expected_error:
                    print "Max Character Validation success for pool name"
                else:
                    print "Max Charater Validation Failed for pool name"
                break
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(invalid_char)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Only alphanumeric and - _ . characters are allowed."
                if text1 == expected_error:
                    print "Invalid Character Validation success for pool name"
                else:
                    print "Invalid Character Validation Failed for pool name"
                break

            self.driver.find_element_by_xpath(".//*[@id='name']").clear()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(allowed_name)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@class='select-pool-group']/select/option[%s]" % stripe).click()
            self.driver.implicitly_wait(5)
            count1 = 0
            while count1 < no_of_disks:
                count1 = count1 + 2
                try:
                    self.driver.find_element_by_xpath(
                        ".//*[@class='cb-jbod editable graph-info']/table/tbody/tr[%s]/td[5]" % count1).click()
                    time.sleep(2)
                except NoSuchElementException as d:
                    print str(d)
            print "Select disks"
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            time.sleep(5)
            self.driver.implicitly_wait(30)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully added the Pool : %s" % allowed_name
            if message == expected_msg:
                print "Successfully Added Pool"
            else:
                print "Error while creating Pool"
        except NoSuchElementException as e:
            print "Error:", str(e)

    def account_name(self):
        allowed_name = "Accounthij1234567890_CB1"
        more_char = "Abcdefghij1234567890_CB51"
        invalid_char = "Abcdefghij!@#$%^&*()"
        try:
            account = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[2]")
            self.driver.execute_script("$(arguments[0]).click();", account)
            addaccount = self.driver.find_element_by_xpath(".//*[@class='action add reduced-hide']/a")
            self.driver.execute_script("$(arguments[0]).click();", addaccount)
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(more_char)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Please enter no more than 24 characters."
                if text1 == expected_error:
                    print "Max Character Validation success for account name"
                else:
                    print "Max Charater Validation Failed for account name"
                break
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(invalid_char)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Only alphanumeric and _ characters are allowed."
                if text1 == expected_error:
                    print "Invalid Character Validation success for account name"
                else:
                    print "Invalid Character Validation Failed account name"
                break

            self.driver.find_element_by_xpath(".//*[@id='name']").clear()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(allowed_name)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            self.driver.implicitly_wait(5)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully Added Account : %s" %allowed_name
            if message == expected_msg:
                print "Successfully Added Account"
            else:
                print "Error while creating account"
        except NoSuchElementException as ac1:
            print "Error:", str(ac1)

    def vsm_name(self, capacity, MGT, ip):
        allowed_name = "Abcdefghij1234567890_CB1234567"
        more_char = "Abcdefghij1234567890_CB51123456789"
        invalid_char = "Abcdefghij!@#$%^&*()"
        try:
            time.sleep(5)
            pools = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[6]")
            self.driver.execute_script("$(arguments[0]).click();", pools)
            selectpool = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[3]/td[1]/span")
            self.driver.execute_script("$(arguments[0]).click();", selectpool)
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='addtsm']/a/span").click()
            self.driver.implicitly_wait(5)
            time.sleep(5)
            self.driver.find_element_by_xpath(".//*[@class='value']/select/option[2]").click()
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(more_char)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Please enter no more than 32 characters."
                if text1 == expected_error:
                    print "Max Character Validation success for vsm"
                else:
                    print "Max Charater Validation Failed for vsm"
                break
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(invalid_char)
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Only alphanumeric and - _ . characters are allowed."
                if text1 == expected_error:
                    print "Invalid Character Validation success for vsm"
                else:
                    print "Invalid Character Validation Failed for vsm"
                break
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@id='name']").clear()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(allowed_name)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").send_keys(capacity)
            self.driver.find_element_by_xpath(".//*[@id='units']/option[%s]" % MGT).click()
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(
                ".//*[@title='Network Interface on the Node that the VSM should use']/select/option[1]").click()
            self.driver.find_element_by_xpath(".//*[@id='address']").send_keys(ip)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
        except NoSuchElementException as vsm1:
            print "Error", str(vsm1)

    def volume_name(self, capacity, MGT):
        allowed_name = "TestVolfghij1234567890_CB5112345"
        more_char = "Abcdefghij1234567890_CB51123456789"
        invalid_char = "Abcdefghij!@#$%^&*()"
        try:
            vsm = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[5]")
            self.driver.execute_script("$(arguments[0]).click();", vsm)
            selectvsm = self.driver.find_element_by_xpath(".//*[@id='dataTable']/tbody/tr[2]/td[1]/span")
            self.driver.execute_script("$(arguments[0]).click();", selectvsm)
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='sb']/a/span").click()
            self.driver.implicitly_wait(5)
            time.sleep(5)
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(more_char)
                self.driver.find_element_by_xpath(".//*[@class='range-edit']/label").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Please enter no more than 32 characters."
                if text1 == expected_error:
                    print "Max Character Validation success for volume"
                else:
                    print "Max Charater Validation Failed for volume"
                break
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(invalid_char)
                self.driver.find_element_by_xpath(".//*[@class='range-edit']/label").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Only alphanumeric and - _ . characters are allowed."
                if text1 == expected_error:
                    print "Invalid Character Validation success for volume"
                else:
                    print "Invalid Character Validation Failed for volume"
                break
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@id='name']").clear()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(allowed_name)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").clear()
            time.sleep(2)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@id='capacity']").send_keys(capacity)
            self.driver.find_element_by_xpath(".//*[@id='units']/option[%s]" % MGT).click()
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next']").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@class='protocols-items']/div[3]/input").click()
            time.sleep(5)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@class='protocols-items']/div[3]/div/div[1]/input").click()
            self.driver.implicitly_wait(60)
            while True:
                allowed_name = "TestVolfghij1234567890_CB5112345"
                more_char = "Abcdefghij1234567890_CB51123456789"
                self.driver.find_element_by_xpath(".//*[@id='mountpoint']").clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(".//*[@id='mountpoint']").send_keys(more_char)
                self.driver.find_element_by_xpath(".//*[@id='cb-wizard-container']/div[2]/div[1]/div[2]/div[1]/div[3]/div/div/form/div[8]/div/label[1]").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Please enter no more than 32 characters."
                if text1 == expected_error:
                    print "Max Character Validation success for mountpoint"
                else:
                    print "Max Charater Validation Failed for mountpoint"
                break
            time.sleep(2)
            self.driver.implicitly_wait(60)
            self.driver.find_element_by_xpath(".//*[@id='mountpoint']").clear()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='mountpoint']").send_keys(allowed_name)
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
        except NoSuchElementException as vol1:
            print "Error:", str(vol1)

    def snapshot_name(self):
        allowed_name = "Snap1234"
        more_char = "Abcdefghij1234"
        invalid_char = "Abcdefghij!@#$%^&*()"
        try:
            vol = self.driver.find_element_by_xpath(".//*[@id='navigation']/ul/li[4]")
            self.driver.execute_script("$(arguments[0]).click();", vol)
            selectvol = self.driver.find_element_by_xpath(".//*[@class='data-table tcc-leftbar']/div/div/table/tbody/tr[2]/td[1]/span")
            self.driver.execute_script("$(arguments[0]).click();", selectvol)
            time.sleep(5)
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath(".//*[@class='addLDPS']/a/span").click()
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(more_char)
                self.driver.find_element_by_xpath(".//*[@id='copies']").send_keys("2")
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Please enter no more than 8 characters."
                if text1 == expected_error:
                    print "Max Character Validation success for snapshot"
                else:
                    print "Max Charater Validation Failed for snapshot"
                break
            while True:
                self.driver.find_element_by_xpath(".//*[@id='name']").clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(invalid_char)
                self.driver.find_element_by_xpath(".//*[@id='copies']").clear()
                self.driver.find_element_by_xpath(".//*[@id='copies']").send_keys("2")
                self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
                text1 = self.driver.find_element_by_xpath(".//*[@class='error']").text
                expected_error = "Only alphanumeric and - _ . characters are allowed."
                if text1 == expected_error:
                    print "Invalid Character Validation success for snapshot"
                else:
                    print "Invalid Character Validation Failed for snapshot"
                break
            self.driver.find_element_by_xpath(".//*[@id='name']").clear()
            time.sleep(2)
            self.driver.find_element_by_xpath(".//*[@id='name']").send_keys(allowed_name)
            self.driver.find_element_by_xpath(".//*[@id='copies']").clear()
            self.driver.find_element_by_xpath(".//*[@id='copies']").send_keys("2")
            self.driver.find_element_by_xpath(".//*[@class='cloud-button next final']").click()
            self.driver.implicitly_wait(5)
            message = self.driver.find_element_by_xpath(".//*[@class='message']/span/span").text
            expected_msg = "Successfully added Local Scheduler : %s" % allowed_name
            if message == expected_msg:
                print "Successfully Added Snapshot schedule"
            else:
                print "Error while adding Snapshot schedule"
        except NoSuchElementException as snap1:
            print "Error:", str(snap1)

    def close_browser(self):
        self.driver.quit()

def main():
    username = "admin"
    password = "test"
    url = "https://20.10.31.10/client/index.jsp"
    t = CharacterValidation()
    t.login_EC(url,username,password)
    time.sleep(5)
    t.pool_name(5,1)
    time.sleep(5)
    t.account_name()
    time.sleep(5)
    t.vsm_name(10,2,"16.10.92.203")
    time.sleep(5)
    t.volume_name(10,2)
    time.sleep(5)
    t.snapshot_name()
    time.sleep(2)
    t.close_browser()

if __name__ == '__main__':
    main()