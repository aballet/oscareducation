from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
from promotions.models import Lesson, Stage
from users.models import Professor, Student
import time


class SetUp(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.selenium.implicitly_wait(10)

        # Creation of the professor and setting up the database
        user = User.objects.create_user(username='prof', password='prof', email='prof@example.com')
        user.save()
        prof = Professor.objects.create(user=user, is_pending=False)
        prof.save()
        self.prof = prof

        # Creating a class
        stage = Stage(name="Stage", level=1)
        stage.save()
        lesson = Lesson(name="Classe", stage=stage)
        lesson.save()
        lesson.professors.add(prof)
        lesson.save()

        # Creation of a Student
        user = User.objects.create(first_name="Etudiant",
                                   last_name="Student",
                                   username="student",
                                   password="student",
                                   email="student@example.com")
        user.save()
        student = Student.objects.create(user=user)
        student.generate_new_code()
        student.save()
        self.student = student

        super(SetUp, self).setUp()


    def tearDown(self):
        self.browser.quit()
        super(SetUp, self).tearDown()

    def connect_prof(self):
        self.browser.get(self.live_server_url + "/accounts/usernamelogin/")
        self.browser.find_element_by_id("id_username").send_keys("student")
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[2]/input').click()
        self.browser.find_element_by_id("id_password").send_keys("student")
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(10)
