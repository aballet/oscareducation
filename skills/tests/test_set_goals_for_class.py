from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from SetUp import SetUp

class TestSetGoalsForClass(SetUp):

    def test_set_goals(self):
        self.connect_prof()
        self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[4]/div/a').click()
        time.sleep(5)
        self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[4]/a').click()
        time.sleep(5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[2]/td[1]/input').click()
        time.sleep(0.5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[3]/td[1]/input').click()
        time.sleep(0.5)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/div[3]/div/div/div[2]/div/ul/li[2]/input').click()
        time.sleep(0.5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/div[3]/div/div/div[2]/div/ul/li[1]/input').click()
        time.sleep(0.5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/div[3]/div/div/div[2]/div/ul/li[3]/input').click()
        time.sleep(0.5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/div[3]/div/div/div[2]/div/ul/li[4]/input').click()

        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.alert_is_present())

        alert = self.browser.switch_to.alert
        assert "maximum" in alert.text
        time.sleep(3)
        alert.accept()

        self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/form/div[5]/button').click()
        time.sleep(5)

        assert "" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[1]/td[3]/span').text

        assert "" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[1]/td[4]/span').text

        assert "" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[1]/td[5]/span').text

        assert "Skill 1 name" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[2]/td[3]/span').text

        assert "Skill 2 name" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[2]/td[4]/span').text

        assert "Skill 3 name" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[2]/td[5]/span').text

        assert "Skill 1 name" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[3]/td[3]/span').text

        assert "Skill 2 name" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[3]/td[4]/span').text

        assert "Skill 3 name" == self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[3]/td[5]/span').text

        self.disconnect()
