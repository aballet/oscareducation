import unittest

from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Professor, Student
from skills.models import Skill, Relations, StudentSkill, SkillHistory
from promotions.models import Lesson, Stage
from exceptions import TypeError, ValueError
from django.utils import timezone

class SkillsTests(TestCase):
    def setUp(self):
        self.student_user = User.objects.create(username="student1")
        self.student = Student.objects.create(user=self.student_user, is_pending=False)
        self.prof_user = User.objects.create(username="professor1")
        self.prof = Professor.objects.create(user=self.prof_user, is_pending=False)

        self.skill_tab = []
        self.stud_skill_tab = []
        for i in range(0,4):
            self.skill_tab.append(Skill.objects.create(code="u"+str(i), name="Skill"+str(i)))
            self.stud_skill_tab.append(StudentSkill.objects.create(student=self.student, skill=self.skill_tab[i]))

        random_skill = Skill.objects.create(code="u9", name="Skill9")

        self.relation1 = Relations.objects.create(from_skill=self.skill_tab[0], to_skill=self.skill_tab[1], relation_type="depend_on")

        #self.stud_skill1 = StudentSkill.objects.create(student=self.student, skill=self.skill_tab[0])

        self.stage1 = Stage.objects.create(id=1, name="Stage1", short_name="sta", level=1, skills=[])
        self.lesson1 = Lesson.objects.create(id=1, name="Lesson1", students=[self.student], professors=[self.prof], stage=self.stage1)

    def test_skill(self):
        self.assertEquals(self.skill_tab[0], self.skill_tab[0])

    def test_dependance_1skill(self):
        dep = self.skill_tab[1].get_depending_skills()
        self.assertEquals(dep[0], self.skill_tab[0])
        self.assertEquals(len(dep), 1)

    def test_prerequisites_1skill(self):
        pre = self.skill_tab[0].get_prerequisites_skills()
        self.assertTrue(self.skill_tab[1] in pre)

    def test_dependance_2skills(self):
        relation2 = Relations.objects.create(from_skill=self.skill_tab[2], to_skill=self.skill_tab[1], relation_type="depend_on")
        dep = self.skill_tab[1].get_depending_skills()
        self.assertTrue(self.skill_tab[0] in dep)
        self.assertTrue(self.skill_tab[2] in dep)
        self.assertFalse(self.skill_tab[1] in dep)

    def test_not_recommended(self):
        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.recommended_to_learn())

    def test_set_objective_1(self):
        self.stud_skill_tab[1].set_objective(self.prof_user, "because", self.lesson1)
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[0].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[2].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[3].recommended_to_learn())

    def test_remove_objective_1(self):
        self.stud_skill_tab[1].set_objective(self.prof_user, "because", self.lesson1)
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.stud_skill_tab[1].remove_objective(self.prof_user, "because", self.lesson1)
        self.assertFalse(self.stud_skill_tab[1].recommended_to_learn())

    def test_set_objective_2(self):
        self.stud_skill_tab[0].set_objective(self.prof_user, "because", self.lesson1)
        self.assertTrue(self.stud_skill_tab[0].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[2].recommended_to_learn())

    def test_cant_add_objective(self):
        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.cant_add_objective())

        self.stud_skill_tab[0].set_objective(self.prof_user, "because", self.lesson1)

        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.cant_add_objective())

        self.stud_skill_tab[1].set_objective(self.prof_user, "because", self.lesson1)

        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.cant_add_objective())

        self.stud_skill_tab[2].set_objective(self.prof_user, "because", self.lesson1)

        for stud_skill in self.stud_skill_tab:
            self.assertTrue(stud_skill.cant_add_objective())

    def test_depth_sort_skills(self):
        for stud_skill in self.stud_skill_tab:
            stud_skill.set_objective(self.prof_user, "because", self.lesson1)
        sorted_list = StudentSkill.__depth_sort_skills__(self.stud_skill_tab)
        self.assertEquals(len(sorted_list), 3)
