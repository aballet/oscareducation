from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from django.contrib.auth.models import User
from promotions.models import Lesson, Stage
from users.models import Professor, Student
from skills.models import Skill, StudentSkill, Section, Relations

import time


class SetUp(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        # Creation of the professor and setting up the database
        user_prof = User.objects.create_user(username='prof', password='prof', email='prof@example.com')
        user_prof.save()
        self.user_prof = user_prof
        prof = Professor.objects.create(user=user_prof, is_pending=False)
        prof.save()
        self.prof = prof

        # Creation of a Student 1
        user1 = User.objects.create(first_name="Fake",
                                    last_name="Student 1",
                                    username="student1",
                                    email="student1@example.com")
        user1.save()
        student1 = Student.objects.create(user=user1, is_pending=True)
        self.code1 = student1.generate_new_code()
        student1.save()
        self.student1 = student1

        # Creation of a Student 2
        user2 = User.objects.create(first_name="Fake",
                                    last_name="Student 2",
                                    username="student2",
                                    email="student2@example.com")
        user2.save()
        student2 = Student.objects.create(user=user2, is_pending=True)
        self.code2 = student2.generate_new_code()
        student2.save()
        self.student2 = student2

        # Creation of a Student 3
        user3 = User.objects.create(first_name="Fake",
                                    last_name="Student 3",
                                    username="student3",
                                    email="student3@example.com")
        user3.save()
        student3 = Student.objects.create(user=user3, is_pending=True)
        self.code3 = student3.generate_new_code()
        student3.save()
        self.student3 = student3

        # Creation of a stage
        stage = Stage(name="Study year 1", level=1)
        stage.save()

        # Creation of a class
        lesson = Lesson(name="Class 1", stage=stage)
        lesson.save()
        self.lesson = lesson
        lesson.professors.add(prof)  # Adds a professor to the class
        lesson.students.add(student1)  # Adds students to the class
        lesson.students.add(student2)
        lesson.students.add(student3)
        lesson.save()

        # Creation of a section
        section = Section.objects.create(name="Section test")
        section.save()

        # Creation of skills for the stage, linked to the stage
        skill1 = Skill.objects.create(code="skill1", name="Skill 1 name", description="This is skill 1.", section=section)
        skill2 = Skill.objects.create(code="skill2", name="Skill 2 name", description="This is skill 2.", section=section)
        skill3 = Skill.objects.create(code="skill3", name="Skill 3 name", description="This is skill 3.", section=section)
        skill4 = Skill.objects.create(code="skill4", name="Skill 4 name", description="This is skill 4.", section=section)
        skill1.save()
        skill2.save()
        skill3.save()
        skill4.save()
        stage.skills.add(skill1)
        stage.skills.add(skill2)
        stage.skills.add(skill3)
        stage.skills.add(skill4)

        # Add relation between skills 3 and 4
        # from_skill = models.ForeignKey(Skill, null=False, blank=False, related_name='from_skill', default=0)
        # to_skill = models.ForeignKey(Skill, null=False, blank=False, related_name='to_skill', default=0)
        # relation_type = models.CharField(max_length=255, null=False, blank=False, choices=(
        #
        #     ("depend_on", "depend de"),
        #     ("similar_to", "similaire a"),
        #     ("identic_to", "identique a"),
        # ))
        relation = Relations.objects.create(from_skill=skill3, to_skill=skill4, relation_type="depend_on")
        relation.save()

        # Link students to the skills
        student_skill11 = StudentSkill.objects.create(student=student1, skill=skill1)
        student_skill12 = StudentSkill.objects.create(student=student1, skill=skill2)
        student_skill13 = StudentSkill.objects.create(student=student1, skill=skill3)
        student_skill14 = StudentSkill.objects.create(student=student1, skill=skill4)
        student_skill11.default(user_prof, "Test purpose", lesson)
        student_skill12.default(user_prof, "Test purpose", lesson)
        student_skill13.default(user_prof, "Test purpose", lesson)
        student_skill14.default(user_prof, "Test purpose", lesson)
        self.student_skill11 = student_skill11
        self.student_skill12 = student_skill12
        self.student_skill13 = student_skill13
        self.student_skill14 = student_skill14

        student_skill21 = StudentSkill.objects.create(student=student2, skill=skill1)
        student_skill22 = StudentSkill.objects.create(student=student2, skill=skill2)
        student_skill23 = StudentSkill.objects.create(student=student2, skill=skill3)
        student_skill24 = StudentSkill.objects.create(student=student2, skill=skill4)
        student_skill21.default(user_prof, "Test purpose", lesson)
        student_skill22.default(user_prof, "Test purpose", lesson)
        student_skill23.default(user_prof, "Test purpose", lesson)
        student_skill24.default(user_prof, "Test purpose", lesson)
        self.student_skill21 = student_skill21
        self.student_skill22 = student_skill22
        self.student_skill23 = student_skill23
        self.student_skill24 = student_skill24

        student_skill31 = StudentSkill.objects.create(student=student3, skill=skill1)
        student_skill32 = StudentSkill.objects.create(student=student3, skill=skill2)
        student_skill33 = StudentSkill.objects.create(student=student3, skill=skill3)
        student_skill34 = StudentSkill.objects.create(student=student3, skill=skill4)
        student_skill31.default(user_prof, "Test purpose", lesson)
        student_skill32.default(user_prof, "Test purpose", lesson)
        student_skill33.default(user_prof, "Test purpose", lesson)
        student_skill34.default(user_prof, "Test purpose", lesson)
        self.student_skill31 = student_skill31
        self.student_skill32 = student_skill32
        self.student_skill33 = student_skill33
        self.student_skill34 = student_skill34

        super(SetUp, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(SetUp, self).tearDown()

    def connect_prof(self):
        self.browser.get(self.live_server_url + "/accounts/usernamelogin/")
        self.browser.find_element_by_id("id_username").send_keys("prof")
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[2]/input').click()
        self.browser.find_element_by_id("id_password").send_keys("prof")
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(5)

    def connect_student(self, number=1):
        self.browser.get(self.live_server_url + "/accounts/usernamelogin/")
        self.browser.find_element_by_id("id_username").send_keys("student" + str(number))
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[2]/input').click()

        switcher = {
            1: self.code1,
            2: self.code2,
            3: self.code3,
        }

        self.browser.find_element_by_id("id_password").send_keys(switcher.get(number, self.code1))
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        self.browser.find_elements_by_id("id_password")[0].send_keys("student")
        self.browser.find_elements_by_id("id_password")[1].send_keys("student")
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/input').click()
        time.sleep(10)

    def disconnect(self):
        self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/ul/li/a').click()

    def connect_admin(self):
        self.browser.get(self.live_server_url + "/admin/")
        self.browser.find_element_by_id("id_username").send_keys("username")
        self.browser.find_element_by_id("id_password").send_keys("password")
        self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        time.sleep(5)

    def disconnect_admin(self):
        self.browser.find_element_by_xpath('//*[@id="user-tools"]/a[3]').click()
