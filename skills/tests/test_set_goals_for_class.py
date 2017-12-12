from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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


        #assert "Skill 1 name" in self.browser.find_element_by_xpath(
        #    '/html/body/div[2]/div[2]/div[2]/div/form/table/tbody/tr[2]/td[3]/span').text

        time.sleep(10000)

        self.disconnect()

    # def test_goal_is_objective(self):
    #     self.student_skill11.validate(self.user_prof, "Test purpose", self.lesson)
    #     self.student_skill12.unvalidate(self.user_prof, "Test purpose", self.lesson)
    #     self.student_skill13.set_objective(self.user_prof, "Test purpose", self.lesson)
    #     self.connect_prof()
    #     self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[4]/div/a').click()
    #     time.sleep(5)
    #     self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/div[4]/div/table/tbody/tr[1]/td[1]/a').click()
    #     time.sleep(5)
    #     self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[3]/a').click()
    #     time.sleep(5)
    #     elem_class = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[1]/a').get_attribute("class")
    #     elem_class_tab = elem_class.split(" ")
    #
    #     success_button = False
    #     for e in elem_class_tab:
    #         if e.find("btn-success") != -1:
    #             success_button = True
    #     assert success_button, True
    #
    #     elem_class = self.browser.find_element_by_xpath(
    #         '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[2]/a').get_attribute("class")
    #     elem_class_tab = elem_class.split(" ")
    #
    #     success_button = False
    #     for e in elem_class_tab:
    #         if e.find("btn-warning") != -1:
    #             success_button = True
    #     assert success_button, True
    #
    #     elem_class = self.browser.find_element_by_xpath(
    #         '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[3]/a').get_attribute("class")
    #     elem_class_tab = elem_class.split(" ")
    #
    #     success_button = False
    #     for e in elem_class_tab:
    #         if e.find("btn-primary") != -1:
    #             success_button = True
    #     assert success_button, True
    #
    #     elem_class = self.browser.find_element_by_xpath(
    #         '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[4]/a').get_attribute("class")
    #     elem_class_tab = elem_class.split(" ")
    #
    #     success_button = False
    #     for e in elem_class_tab:
    #         if e.find("btn-info") != -1:
    #             success_button = True
    #     assert success_button, True
    #
    #     time.sleep(5)
    #     self.disconnect()
