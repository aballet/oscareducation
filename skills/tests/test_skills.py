from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Professor, Student
from skills.models import Section, Skill, Relations, StudentSkill, SkillHistory
from promotions.models import Lesson, Stage
from exceptions import TypeError, ValueError
from django.utils import timezone

class SkillsTests(TestCase):
    def reload_db_info(self):
         """"Refresh stud_skill_tab from the database"""
         for i in xrange(len(self.stud_skill_tab)):
             sk = self.stud_skill_tab[i]
             self.stud_skill_tab[i] = StudentSkill.objects.get(skill = sk.skill )


    def setUp(self):
        self.student_user = User.objects.create(username="student1")
        self.student = Student.objects.create(user=self.student_user, is_pending=False)
        self.prof_user = User.objects.create(username="professor1")
        self.prof = Professor.objects.create(user=self.prof_user, is_pending=False)

        self.stage1 = Stage.objects.create(id=1, name="Stage1", short_name="sta", level=1, skills=[])
        self.lesson1 = Lesson.objects.create(id=1, name="Lesson1", students=[self.student], professors=[self.prof], stage=self.stage1)

        self.section1 = Section.objects.create(name="Section1")

        self.skill_tab = []
        self.stud_skill_tab = []
        for i in range(0,5):
            self.skill_tab.append(Skill.objects.create(code="u"+str(i), name="Skill"+str(i), section=self.section1))
            self.stud_skill_tab.append(StudentSkill.objects.create(student=self.student, skill=self.skill_tab[i]))

        random_skill = Skill.objects.create(code="u9", name="Skill9")

        self.relation1 = Relations.objects.create(from_skill=self.skill_tab[0], to_skill=self.skill_tab[1], relation_type="depend_on")

    def test_dependance_skills_1(self):
        """"Check get_depending_skills function"""
        dep = self.skill_tab[1].get_depending_skills()
        self.assertEquals(dep[0], self.skill_tab[0])
        self.assertEquals(len(dep), 1)

    def test_prerequisites_skills_1(self):
        """"Check get_prerequisites_skills function"""
        pre = self.skill_tab[0].get_prerequisites_skills()
        self.assertTrue(self.skill_tab[1] in pre)
        self.assertEquals(len(pre), 1)

    def test_dependance_skills_2(self):
        """"Check get_depending_skills function for 2 dependances"""
        relation2 = Relations.objects.create(from_skill=self.skill_tab[2], to_skill=self.skill_tab[1], relation_type="depend_on")
        dep = self.skill_tab[1].get_depending_skills()
        self.assertTrue(self.skill_tab[0] in dep)
        self.assertTrue(self.skill_tab[2] in dep)
        self.assertFalse(self.skill_tab[1] in dep)
        self.assertEquals(len(dep), 2)

    def test_recommended_to_learn_false(self):
        """Check that recommended_to_learn is false"""
        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.recommended_to_learn())

    def test_set_objective_1(self):
        """Check set_objective for 1 skill"""
        self.stud_skill_tab[1].set_objective(self.prof_user, "because", self.lesson1)
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[0].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[2].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[3].recommended_to_learn())

    def test_remove_objective_1(self):
        """Check remove_objective for 1 skill"""
        self.stud_skill_tab[1].set_objective(self.prof_user, "because", self.lesson1)
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.stud_skill_tab[1].remove_objective(self.prof_user, "because", self.lesson1)
        self.assertFalse(self.stud_skill_tab[1].recommended_to_learn())

    def test_set_objective_prereq(self):
        """Check set_objective for 1 skill and its prerequisites"""
        self.stud_skill_tab[0].set_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        pre = self.skill_tab[0].get_prerequisites_skills()
        self.assertTrue(self.skill_tab[1] in pre)
        self.assertTrue(self.stud_skill_tab[0].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[2].recommended_to_learn())

    def test_set_objective_lvl2(self):
        """Check set_objective for 1 skill with 2 levels of prerequisites"""
        relation3 = Relations.objects.create(from_skill=self.skill_tab[1], to_skill=self.skill_tab[3], relation_type="depend_on")
        self.stud_skill_tab[0].set_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.assertTrue(self.stud_skill_tab[0].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[3].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[2].recommended_to_learn())

    def test_remove_objective_prereq(self):
        """Check remove_objective for 1 skill and its prerequisites"""
        self.stud_skill_tab[0].set_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.stud_skill_tab[0].remove_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        pre = self.skill_tab[0].get_prerequisites_skills()
        self.assertTrue(self.skill_tab[1] in pre)
        self.assertFalse(self.stud_skill_tab[0].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[1].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[2].recommended_to_learn())

    def test_remove_objective_prereq_objective(self):
        """Check remove_objective for 1 skill but not its prerequisite as it is
           also an objective."""
        self.stud_skill_tab[0].set_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.stud_skill_tab[1].set_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.assertTrue(self.stud_skill_tab[0].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.stud_skill_tab[0].remove_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.assertFalse(self.stud_skill_tab[0].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.assertFalse(self.stud_skill_tab[2].recommended_to_learn())

    def test_remove_objective_prereq_recommended(self):
        """Check remove_objective for 1 skill but not its prerequisite as it is
           common to another objective."""
        relation3 = Relations.objects.create(from_skill=self.skill_tab[1], to_skill=self.skill_tab[3], relation_type="depend_on")
        relation4 = Relations.objects.create(from_skill=self.skill_tab[2], to_skill=self.skill_tab[3], relation_type="depend_on")
        self.stud_skill_tab[1].set_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.stud_skill_tab[2].set_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.assertTrue(self.stud_skill_tab[1].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[2].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[3].recommended_to_learn())
        self.stud_skill_tab[1].remove_objective(self.prof_user, "because", self.lesson1)
        self.reload_db_info()
        self.assertFalse(self.stud_skill_tab[1].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[2].recommended_to_learn())
        self.assertTrue(self.stud_skill_tab[3].recommended_to_learn())

    def test_cant_add_objective_0(self):
        """Check cant_add_objective for no objective"""
        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.cant_add_objective())

    def test_cant_add_objective_1(self):
        """Check cant_add_objective for 1 objective"""
        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.cant_add_objective())
        self.stud_skill_tab[0].set_objective(self.prof_user, "because", self.lesson1)
        for stud_skill in self.stud_skill_tab:
            self.assertFalse(stud_skill.cant_add_objective())

    def test_cant_add_objective_3(self):
        """Check cant_add_objective for the 3 objectives"""
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

    def test_depth_sort_skills_1(self):
        """Check depth_sort_skills for 1 skill"""
        sorted_list = StudentSkill.__depth_sort_skills__([self.stud_skill_tab[1]], None)
        self.assertEquals(len(sorted_list), 2) #[0] : acquired skills ; [1] : level 1
        self.assertTrue(self.stud_skill_tab[1] in sorted_list[1])

    def test_depth_sort_skills_1_prerequisite(self):
        """Check depth_sort_skills for 1 skill with a prerequisite"""
        sorted_list = StudentSkill.__depth_sort_skills__([self.stud_skill_tab[0]], None)
        self.assertEquals(len(sorted_list), 3)
        self.assertTrue(self.stud_skill_tab[1] in sorted_list[1])
        self.assertTrue(self.stud_skill_tab[0] in sorted_list[2])

    def test_depth_sort_skills_lvl2(self):
        """Check depth_sort_skills for 1 skill with 2 levels of prerequisites"""
        relation3 = Relations.objects.create(from_skill=self.skill_tab[1], to_skill=self.skill_tab[3], relation_type="depend_on")
        sorted_list = StudentSkill.__depth_sort_skills__([self.stud_skill_tab[0]], None)
        self.assertEquals(len(sorted_list), 4)
        self.assertEquals(len(sorted_list[0]), 0)
        self.assertEquals(len(sorted_list[1]), 1)
        self.assertTrue(self.stud_skill_tab[3] in sorted_list[1])
        self.assertEquals(len(sorted_list[2]), 1)
        self.assertTrue(self.stud_skill_tab[1] in sorted_list[2])
        self.assertEquals(len(sorted_list[3]), 1)
        self.assertTrue(self.stud_skill_tab[0] in sorted_list[3])

    def test_depth_sort_skills_lvl2_long(self):
        """Check depth_sort_skills for 1 skill with 2 levels of prerequisites"""
        relation3 = Relations.objects.create(from_skill=self.skill_tab[1], to_skill=self.skill_tab[3], relation_type="depend_on")
        relation4 = Relations.objects.create(from_skill=self.skill_tab[0], to_skill=self.skill_tab[2], relation_type="depend_on")
        relation5 = Relations.objects.create(from_skill=self.skill_tab[2], to_skill=self.skill_tab[4], relation_type="depend_on")
        sorted_list = StudentSkill.__depth_sort_skills__([self.stud_skill_tab[0]], None)
        self.assertEquals(len(sorted_list), 4)
        self.assertEquals(len(sorted_list[0]), 0)
        self.assertEquals(len(sorted_list[1]), 2)
        self.assertTrue(self.stud_skill_tab[3] in sorted_list[1])
        self.assertTrue(self.stud_skill_tab[4] in sorted_list[1])
        self.assertEquals(len(sorted_list[2]), 2)
        self.assertTrue(self.stud_skill_tab[1] in sorted_list[2])
        self.assertTrue(self.stud_skill_tab[2] in sorted_list[2])
        self.assertEquals(len(sorted_list[3]), 1)
        self.assertTrue(self.stud_skill_tab[0] in sorted_list[3])
