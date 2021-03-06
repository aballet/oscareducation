from django import template
from skills.models import StudentSkill, Section, Skill
from promotions.models import Stage


register = template.Library()

@register.simple_tag(takes_context=True)
def get_students_skills(context, of_keyword, student, at_keyword, stage, as_keyword, target_name):
    context[target_name] = StudentSkill.objects.filter(skill__in=stage.skills.all(), student=student).select_related("skill").order_by("skill__section", "skill__code")
    return ""

@register.simple_tag(takes_context=True)
def go_next_line(context, as_keyword, target_name):
    context[target_name] = StudentSkill.__next_line__()
    return ""

@register.simple_tag(takes_context=True)
def reset_counter_line(context):
    StudentSkill.__reset_counter_line__()
    return ""


@register.simple_tag(takes_context=True)
def get_depth_sorted_students_skills(context, of_keyword, student, at_keyword, stage, as_keyword, target_name):
    """ return a list of list of sorted skills """
    set = StudentSkill.objects.filter(skill__in=stage.skills.all(), student=student)
    remove = set.exclude(is_objective = None)
    context[target_name] = StudentSkill.__depth_sort_skills__(remove,student)
    return ""

@register.simple_tag(takes_context=True)
def get_student_target_skills(context, of_keyword, student, at_keyword, stage, as_keyword, target_name):
    list_target_skills = []
    student_skills = StudentSkill.objects.filter(skill__in=stage.skills.all(), student=student).order_by("skill__code")
    for student_skill in student_skills:
        if student_skill.is_objective:
         list_target_skills.append(student_skill)

    index = [0,1,2]
    d_end = {}
    for e in range(len(list_target_skills),3):
        d_end.update({e:""})

    d = dict((index[i],list_target_skills[i]) for i in range(0,len(list_target_skills)))
    d.update(d_end)
    context[target_name] = d # sorted(list_target_skills)
    return ""

@register.simple_tag(takes_context=True)
def get_first_stage_tag(context, of_keyword, lesson, as_keyword, target_name):
    context[target_name] = lesson.get_first_stage()
    return ""

@register.simple_tag
def get_skill_heatmap_class(skills_to_heatmap_class, skill):
    return skills_to_heatmap_class.get(skill, "")


@register.simple_tag
def get_stage_id(skill_short_name):
    return Stage.objects.get(short_name=skill_short_name).id


@register.filter
def clean_file_name(file_name):
    if "/" in file_name:
        file_name = file_name.split("/")[-1]

    if "." in file_name:
        file_name = ".".join(file_name.split(".")[:-1])
    if "_" in file_name:
        file_name = "_".join(file_name.split("_")[:-1])
    return file_name


@register.filter
def split_skill_as_section(skill_code):
    return "-".join(skill_code.split("-")[:2])


@register.filter
def split_skill_as_subsection(skill_code):
    return skill_code.split("-")[-1]

@register.simple_tag
def get_section_name(section_id):
    """ helper tag to get section name from section id"""
    return Section.objects.get(id=section_id).name

@register.simple_tag
def get_skill_code(section_id):
    """ helper tag to get section name from section id"""
    return Skill.objects.get(id=section_id).code
@register.filter
def encode_utf8( string ):
    #return string.encode('Windows-1252', 'ignore')
    return string