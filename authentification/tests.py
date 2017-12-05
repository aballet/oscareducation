from django.test import TestCase

# Create your tests here.

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestConnection(unittest.TestCase):
    base_url = "http://localhost:8000"

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def testConnectionStudent(self):
        self.browser.implicitly_wait(10)  # seconds
        self.browser.get(self.base_url+'/accounts/usernamelogin/')
        usernameField = self.browser.find_element_by_xpath('//*[@id="id_username"]')
        usernameField.send_keys('henri.moumal')
        usernameField.send_keys(Keys.RETURN)

        self.browser.implicitly_wait(10)  # seconds
        passwordField = self.browser.find_element_by_xpath('//*[@id="id_password"]')
        passwordField.send_keys('henri')
        passwordField.send_keys(Keys.RETURN)

        self.browser.implicitly_wait(20)  # seconds
        assert self.browser.current_url == self.base_url+"/student/dashboard/"

        self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/ul/li/a').click()


"""
    def testConnectionProfessor(self):
        self.browser.implicitly_wait(30)  # seconds
        self.browser.get(self.base_url + '/accounts/usernamelogin/')
        usernameField = self.browser.find_element_by_xpath('//*[@id="id_username"]')
        usernameField.send_keys('kim')
        usernameField.send_keys(Keys.RETURN)

        passwordField = self.browser.find_element_by_xpath('//*[@id="id_password"]')
        passwordField.send_keys('kim')
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()

        assert self.browser.current_url == self.base_url + "/professor/dashboard/"

        self.browser.find_element_by_xpath('/ html / body / div[2] / div[1] / div / div / ul / li / a').click()

"""

    #def tearDown(self):