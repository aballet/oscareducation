import time
from SetUp import SetUp


class TestSetGoalsIndividually(SetUp):

    def test_set_goals(self):
        self.connect_prof()
        self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[4]/div/a').click()
        time.sleep(5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[1]/div[4]/div/table/tbody/tr[1]/td[1]/a').click()
        time.sleep(5)
        self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[3]/a').click()
        time.sleep(5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[1]/a').click()

        # TODO : find a way to select the buttons on the popup

        time.sleep(5)
        self.disconnect()

    def test_skill_colors(self):
        self.student_skill11.validate(self.user_prof, "Test purpose", self.lesson)
        self.student_skill12.unvalidate(self.user_prof, "Test purpose", self.lesson)
        self.student_skill13.set_objective(self.user_prof, "Test purpose", self.lesson)
        self.connect_prof()
        self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[4]/div/a').click()
        time.sleep(5)
        self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[1]/div[4]/div/table/tbody/tr[1]/td[1]/a').click()
        time.sleep(5)
        self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[3]/a').click()
        time.sleep(5)
        elem_class = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[1]/a').get_attribute("class")
        elem_class_tab = elem_class.split(" ")

        success_button = False
        for e in elem_class_tab:
            if e.find("btn-success") != -1:
                success_button = True
        assert success_button, True

        elem_class = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[2]/a').get_attribute("class")
        elem_class_tab = elem_class.split(" ")

        success_button = False
        for e in elem_class_tab:
            if e.find("btn-warning") != -1:
                success_button = True
        assert success_button, True

        elem_class = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[3]/a').get_attribute("class")
        elem_class_tab = elem_class.split(" ")

        success_button = False
        for e in elem_class_tab:
            if e.find("btn-primary") != -1:
                success_button = True
        assert success_button, True

        elem_class = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/div/ul/li[4]/a').get_attribute("class")
        elem_class_tab = elem_class.split(" ")

        success_button = False
        for e in elem_class_tab:
            if e.find("btn-info") != -1:
                success_button = True
        assert success_button, True

        time.sleep(5)
        self.disconnect()
