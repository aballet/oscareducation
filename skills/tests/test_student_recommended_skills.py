import time
from SetUp import SetUp


class TestStudentRecommendedSkills(SetUp):

    def test_has_recommended_skills(self):
        self.student_skill11.set_objective(self.user_prof, "Test purpose", self.lesson)
        self.student_skill12.set_objective(self.user_prof, "Test purpose", self.lesson)
        self.student_skill13.set_objective(self.user_prof, "Test purpose", self.lesson)
        self.connect_student()

        title = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[3]/div[2]/div[2]/div[3]/div/a[1]/button').get_attribute("data-original-title")
        assert title == "Skill 4 name"

        title = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[3]/div[2]/div[2]/div[3]/div/a[2]/button').get_attribute("data-original-title")
        assert title == "Skill 2 name"

        title = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[3]/div[2]/div[2]/div[3]/div/a[3]/button').get_attribute("data-original-title")
        assert title == "Skill 1 name"

        title = self.browser.find_element_by_xpath(
            '/html/body/div[2]/div[3]/div[2]/div[2]/div[3]/div/a[4]/button').get_attribute("data-original-title")
        assert title == "Skill 3 name"

        time.sleep(5)
        self.disconnect()



