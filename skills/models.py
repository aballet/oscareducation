# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from operator import attrgetter

from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from examinations.models import Context


class Skill(models.Model):
    """[FR] Compétence
        A Skill can be evaluated through questions answered by a student.
        Thus, when evaluated, a Skill can be acquired by a student, or not.
    """

    code = models.CharField(max_length=20, unique=True, db_index=True)
    """The Skill reference code"""

    name = models.CharField(max_length=255)
    """The Skill name"""

    description = models.CharField(max_length=255)
    """The Skill description"""

    section = models.ForeignKey('Section', null=True)
    """The Section to which the Skill belongs @to remove after """

    # depends_on = models.ManyToManyField('Skill', related_name="depends_on+")
    """If a Skill depends on another (i.e. a prerequisite), this is set in this relation"""

    # similar_to = models.ManyToManyField('Skill', related_name="similar_to+")
    """The Skills that are similar, but with different references"""

    resource = models.ManyToManyField('resources.Resource', related_name="skill_resource+")
    """The Resources linked to this Skill. A Resource can be linked to several Skills"""

    image = models.CharField(max_length=255, null=True, blank=True)
    """Icon used to categorize the Skill"""

    oscar_synthese = models.TextField(null=True, blank=True)
    """The Skill abstract provided by Oscar"""

    modified_by = models.ForeignKey(User, null=True)
    """The last user that modified this Skill"""

    time_skill = models.IntegerField(default=0, null=True)

    relations = models.ManyToManyField("self", through="Relations", related_name="related_to", symmetrical=False)
    """ Make relation between skills through a relation Model with a strict options : depended_on , similar_to  and identic_to """

    def __unicode__(self):
        return self.code + " : " + self.name

    def skills_with_exercice_count(self):
        """ Count Context in relation with the current Skills"""
        return Context.objects.filter(skill=self).count()

    def get_prerequisites_skills(self):
        """
        :return: Queryset of prerequisites Skills for the current Skill
        """

        return self.relations.filter(
            to_skill__relation_type="depend_on"
        )

    def get_depending_skills(self):
        """
        :return: Queryset of Skills depending on the current Skill
        """

        return self.related_to.filter(
            from_skill__relation_type="depend_on"
        )
    def __eq__(self, other):
        return self.code == other.code


class Relations(models.Model):
    """ The through relation skill model """

    from_skill = models.ForeignKey(Skill, null=False, blank=False, related_name='from_skill', default=0)
    to_skill = models.ForeignKey(Skill, null=False, blank=False, related_name='to_skill', default=0)
    relation_type = models.CharField(max_length=255, null=False, blank=False, choices=(

        ("depend_on", "dépend de"),
        ("similar_to", "similaire à"),
        ("identic_to", "identique à"),
    ))

    def __unicode__(self):
        return self.from_skill.code + " , " + self.to_skill.code + ", " + self.relation_type

    class Meta:
        verbose_name = 'Relations between Skill'
        verbose_name_plural = 'Relations between Skill\'s'


class Section(models.Model):
    """[FR] Rubrique
        A Section regroups a list of CodeR and a list
        of Skills. Sections form socles (most of the
        time, a socle represents a year of mathematics
        class)
    """

    name = models.CharField(max_length=255)
    """The Section name"""
    # editable=False,
    resource = models.ManyToManyField('resources.Resource', related_name="section_resource+")
    """The resources linked to this Section. A resource can be linked to several Sections"""

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CodeR(models.Model):
    """[FR] Ressource (ou Code R),
    à ne pas confondre avec une ressource pédagogique
        A CodeR describes concept(s) to master, in orderskills_coder_skill
        to acquire the skill(s) based on that CodeR.
        Unlike a Skill, A CodeR cannot be evaluated
        directly.
    """

    section = models.ForeignKey('Section', null=True)
    """The Section to which the CodeR belongs"""

    sub_code = models.CharField(max_length=10)
    """The CodeR reference code"""

    name = models.CharField(max_length=255)
    """The CodeR name"""

    # paired_to = models.ManyToManyField('CodeR', related_name="paired_to+")
    """@todo remove """

    resource = models.ManyToManyField('resources.Resource', related_name="coder_resource+")
    """The Resources linked to this CodeR. A Resource can be linked to several CodeR"""

    skill = models.ManyToManyField('Skill', related_name="coder_skill+")
    """The Skills linked to this CodeR. A Skill can be linked to several CodeR"""

    def __unicode__(self):
        return self.sub_code + " : " + self.name

    class Meta:
        verbose_name = 'CodeR'
        verbose_name_plural = 'CodeR'


class CodeR_relations(models.Model):
    """ The through relation CodeR model  """

    from_coder = models.ForeignKey(CodeR, null=False, blank=False, related_name='from_coder', default=0)
    to_coder = models.ForeignKey(CodeR, null=False, blank=False, related_name='to_coder', default=0)
    relation_type = models.CharField(max_length=255, null=False, blank=False, choices=(

        ("depend_on", "dépend de"),
        ("similar_to", "similaire à"),
        ("identic_to", "identique à"),
    ))

    def __unicode__(self):
        return self.from_coder.name + " , " + self.to_coder.name + ", " + self.relation_type

    class Meta:
        verbose_name = 'Relations between CodeR'
        verbose_name_plural = 'Relations between CodeR\'s'


class SkillHistory(models.Model):
    """
        The reason why a Skill is acquired or not,
        or not yet, when and by who/how
    """

    skill = models.ForeignKey(Skill)
    """The Skill to validate"""
    student = models.ForeignKey('users.Student')
    """The Student concerned by this Skill"""
    datetime = models.DateTimeField(auto_now_add=True)
    """The date the Skill status was created"""
    value = models.CharField(max_length=255, choices=(
        ('unknown', 'Inconnu'),
        ('acquired', 'Acquise'),
        ('not acquired', 'None Acquise'),
    ))
    """The Skill status : unknown, acquired or not acquired"""

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    reason_object = GenericForeignKey('content_type', 'object_id')
    reason = models.CharField(max_length=255)
    """Why the Skill is validated or not"""

    by_who = models.ForeignKey(User)

    class Meta:
        ordering = ['datetime']


class StudentSkill(models.Model):
    """
        The link between a Skill and a Student
    """
    student = models.ForeignKey('users.Student')
    """The Student concerned by the Skill"""
    skill = models.ForeignKey(Skill)
    """The Skill the Student acquired/did not acquired"""
    tested = models.DateTimeField(default=None, null=True)
    """When the Skill was tested"""
    acquired = models.DateTimeField(default=None, null=True)
    """When the Skill was acquired"""
    is_objective = models.DateTimeField(default=None, null=True)
    """When the Skill was set as objective"""
    is_recommended = models.DateField(default=None, null=True)
    """When the Skill was set as recommended"""

    sort_high = models.IntegerField(default = 0, null=True)
    sort_section_name = models.CharField(max_length=255, null=True)
    sort_time = models.IntegerField(default = 0, null=True)


    def reset_sort_variables(self):
        pass

    def __unicode__(self):
        return u"%s - %s - %s" % (
        self.student, self.skill, "green" if self.acquired else ("orange" if self.tested else "white"))

    def go_down_visitor(self, function):
        """Help function to explore and validate prerequisites when a Skill is validated"""
        # protective code against loops in skill tree
        already_done = set()

        def traverse(student_skill):
            function(student_skill)

            for sub_student_skill in StudentSkill.objects.filter(
                    skill__in=student_skill.skill.get_prerequisites_skills(), student=self.student):
                if sub_student_skill.id not in already_done:
                    already_done.add(sub_student_skill.id)
                    traverse(sub_student_skill)

        traverse(self)

    # TODO: Does not work, need to create a reverse to the Manytomany relation
    def go_up_visitor(self, function):
        """
        Help function to explore and invalidate (parent) Skill that depends on the failed Skill.
        A failed prerequisite implies that the Skills that depends on it must be failed too.
        """
        # protective code against loops in skill tree
        already_done = set()

        def traverse(student_skill):
            function(student_skill)

            for sub_student_skill in StudentSkill.objects.filter(
                    skill__in=student_skill.skill.get_prerequisites_skills(), student=self.student):
                if sub_student_skill.id not in already_done:
                    already_done.add(sub_student_skill.id)
                    traverse(sub_student_skill)

        traverse(self)

    def validate(self, who, reason, reason_object):
        """Validates a Skill (change its status to "acquired")"""

        def validate_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="acquired",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )

            student_skill.acquired = datetime.now()
            student_skill.is_objective = None
            student_skill.is_recommended = None
            student_skill.save()

        self.go_down_visitor(validate_student_skill)

    def __eq__(self, other):
        return self.skill.code == other.skill.code


    def __le__(self,other):
        pass

    def __ge__(self,other):
        pass

    def unvalidate(self, who, reason, reason_object):
        """Invalidates a Skill (change its status to "not acquired")"""

        def unvalidate_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="not acquired",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )

            student_skill.sort_time = self.skill.time_skill
            student_skill.sort_section_name = self.skill.section.name
            student_skill.acquired = None
            student_skill.tested = datetime.now()
            student_skill.save()

        # Up traversal does not work, disabled
        # self.go_up_visitor(unvalidate_student_skill)

        # TODO: erase the following lines when go_up_visitor is repaired
        SkillHistory.objects.create(
            skill=self.skill,
            student=self.student,
            value="not acquired",
            by_who=who,
            reason=reason,
            reason_object=reason_object,
        )
        self.acquired = None
        self.tested = datetime.now()
        self.sort_time = self.skill.time_skill
        self.sort_section_name = self.skill.section.name
        self.save()

    def default(self, who, reason, reason_object):
        """"Reset" a Skill (change its status to "unknown")"""
        SkillHistory.objects.create(
            skill=self.skill,
            student=self.student,
            value="unknown",
            by_who=who,
            reason=reason,
            reason_object=reason_object,
        )

        self.acquired = None
        self.tested = None
        self.is_objective = None
        self.sort_time = self.skill.time_skill
        self.sort_section_name = self.skill.section.name
        self.save()

    def set_objective(self, who, reason, reason_object):
        """"Reset" a Skill (change its status to "unknown")"""
        def recommend_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="recommended",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )
            student_skill.sort_time = self.skill.time_skill
            student_skill.sort_section_name = self.skill.section.name

            if(not student_skill.acquired):
                student_skill.is_recommended = datetime.now()

            student_skill.save()

        self.is_objective = datetime.now()
        self.is_recommended = datetime.now()
        self.sort_time = self.skill.time_skill
        self.sort_section_name = self.skill.section.name
        self.save()
        self.go_down_visitor(recommend_student_skill)

    def remove_objective(self, who, reason, reason_object):
        """"Reset" a Skill (change its status to "unknown")"""
        def not_recommend_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="not recommended",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )

            if(not student_skill.acquired):
                student_skill.is_recommended = None
                student_skill.save()

        self.is_objective = None
        self.is_recommended = None
        self.save()
        self.go_down_visitor(not_recommend_student_skill)

    def cant_add_objective(self):
        req = StudentSkill.objects.filter(student=self.student)
        list_objectives = req.exclude(is_objective = None)
        #print(list_objectives.count())
        if list_objectives.count() >= 3:
            return True
        return False

    def recommended_to_learn(self):
        """
        Determines if the Skill is to recommend to the Student.
        All the tested and not acquired Skills will be recommended,
        except if at least one of its prerequisites is not acquired
        """
        if self.acquired :
            return False

        if self.is_objective or self.is_recommended:
            return True

        """for skill in self.skill.get_prerequisites_skills():
            skill = StudentSkill.objects.get(student=self.student, skill=skill)
            if skill.is_objective:
                return True"""

        return False

    @staticmethod
    def __depth_sort_skills__(list_obj, current_stud):
        list_level = [[]]
        list_acquired = []
        list_std_skill = []

        def recursive(std_skill):
            q_set_r = StudentSkill.objects.filter(skill__in=std_skill.skill.get_prerequisites_skills(), student=std_skill.student)# acquired = None)  # Set of StudentSkill children not yet acquired
            q_set = q_set_r.filter(acquired = None) #skills not acquired
            q_set_acq = q_set_r.exclude(acquired = None) #skills acquired

            # Puts every acquired item in list_acquired
            for elem in q_set_acq:
                if elem not in list_acquired:
                    list_acquired.append(elem)
                    std_skill.sort_high = -1
                    std_skill.save()

            # if the QuerySet is empty
            if q_set.count() == 0:
                if std_skill not in list_level[0]:
                    list_level[0].append(std_skill)
                    list_std_skill.append(std_skill)
                    std_skill.sort_high = 0
                    std_skill.save()
                return 1
            else:
                result = 0
                for e in q_set:
                    a = recursive(e)
                    if a > result:
                        result = a
                if len(list_level) <= result:
                    list_level.append([])
                if std_skill not in list_level[result]:
                    list_level[result].append(std_skill)
                    list_std_skill.append(std_skill)
                    std_skill.sort_high = result
                    std_skill.save()
                return result+1

        '''if(len(list_obj) == 0):
            q_set_r = StudentSkill.objects.filter(student=current_stud)
            ToReturn = [[]]
            for stud_skill in q_set_r:
                q_set_pre = StudentSkill.objects.filter(skill__in=stud_skill.skill.get_prerequisites_skills())
                if len(q_set_pre) == 0:
                    ToReturn[0].append(stud_skill)
                else:
                    to_take = True
                    for std_skill  in q_set_pre:
                        if std_skill.acquired == None:
                            to_take = False
                    if to_take and stud_skill not in ToReturn :
                        ToReturn[0].append(stud_skill)
            return ToReturn'''


        for std_skill_objective in list_obj:
            recursive(std_skill_objective)

        sort_criterion = getOrderSort()
        criterion1 = sort_criterion[0][0]
        list_std_skill = sorted(list_std_skill, key=lambda student_skill: getattr(student_skill,criterion1))
        prevList = []
        level_List = []

        for std_skill in list_std_skill:
            if prevList == []:
                prevList.append(std_skill)
            else:
                if getattr(std_skill,criterion1) == getattr(prevList[0],criterion1):
                    prevList.append(std_skill)
                else:
                    level_List.append(prevList)
                    prevList = [std_skill]

        level_List.append(prevList)
        for sublist in level_List:
            sublist.sort(key=lambda student_skill: (getattr(student_skill,sort_criterion[1][0]),getattr(student_skill,sort_criterion[2][0])))

        list_level.insert(0, list_acquired)

        if len(list_level) == 2 and len(list_level[0]) == 0:  # Empty list
            return None
        else:
            return level_List

    global var
    var = 3

    @staticmethod
    def __next_line__():
        print(var)
        if var == 0:
            global  var
            var = random.randint(0,2)
            return True
        global var
        var = var - 1
        return False

    @staticmethod
    def __reset_counter_line__():
        global var
        var = random.randint(0,2)
        print("new var %d"%(var))


SORT_CHOICES = (
    (0, "First"),
    (1, "Second"),
    (2, "Third")
)

class Sort(models.Model):
    name      = models.TextField(null=False, editable = False)
    weight    = models.IntegerField(choices=SORT_CHOICES, default=1)

    def __unicode__(self):
        sortOrder = None;
        if self.weight == 0 :
            sortOrder = "First"
        elif self.weight == 1:
            sortOrder = "Second"
        else:
            sortOrder = "Third"
        return "{0} : {1}".format(self.name, sortOrder)

def getOrderSort():
    sortOrder =[]
    q_set_r = Sort.objects.filter(Q(name="Sort by number of unvalidated prerequisites") | Q(name="Sort by section name") | Q(name="Sort by time to make the exercice"))
    for sort in q_set_r:
        if sort.name == "Sort by number of unvalidated prerequisites":
            sortOrder.append(("sort_high",sort.weight))
        elif sort.name == "Sort by section name":
            sortOrder.append(("sort_section_name", sort.weight))
        else:
            sortOrder.append(("sort_time", sort.weight))
    sortOrder.sort(key=lambda tup: tup[1], reverse=True)
    return sortOrder
    #print sortOrder
