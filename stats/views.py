import csv

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from examinations.models import Context as Question
from promotions.models import Lesson, Stage
from promotions.utils import user_is_professor
from resources.models import KhanAcademy, Sesamath
from skills.models import Skill
from users.models import Professor, Student
from .utils import user_is_superuser

from stats.StatsObject import get_class_stat, get_student_stat

@user_is_professor
def exportCSV(request, pk):
    """Downloads a CSV file of the displayed data"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    lesson = get_object_or_404(Lesson, pk=pk)
    students = Student.objects.filter(lesson=lesson)
    #stats.ExamsPassed.



    display_type = request.POST.get("csv_type", None)

    if display_type == "euro":
        writer = csv.writer(response, delimiter=";")
    else:
        writer = csv.writer(response)
    writer.writerow([display_type])

    for student in students:
        writer.writerow([student, lesson.name])
    # already prints student names, figure what the method is to get the data which is displayed into the CSV
    return response


@user_is_superuser
def dashboard(request):
    questions_per_stage = []
    for stage in Stage.objects.annotate(Count("skills"), Count("skills__exercice")):
        skills = stage.skills_with_exercice_count()
        questions_per_stage.append({
            "stage": stage,
            "skills_count_with_questions": skills.filter(exercice__count__gt=0),
            # "skills_count_without_questions": skills.filter(exercice__count=0),
        })

    return render(request, "stats/dashboard.haml", {
        "professors": Professor.objects.all(),
        "students": Student.objects.all(),
        "lessons": Lesson.objects.all(),
        "skills": Skill.objects.all(),
        "skills_with_khan_ressources": Skill.objects.annotate(Count('khanacademyvideoskill')).filter(
            khanacademyvideoskill__count__gt=0),
        "skills_with_sesamath_ressources": Skill.objects.annotate(Count('sesamathskill')).filter(
            sesamathskill__count__gt=0),
        "khanacademyvideoskill": KhanAcademy.objects.order_by('-created_at').select_related('skill', 'reference'),
        "sesamathskill": Sesamath.objects.order_by('-created_at').select_related('skill', 'reference'),
        "questions": Question.objects.all().order_by("-modified_at"),
        "stages_with_skills_with_questions": questions_per_stage,
        "skills_with_questions": Skill.objects.annotate(Count('exercice')).filter(exercice__count__gt=0),
    })


def view_student(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    students = Student.objects.filter(lesson=lesson)

    return render(request, "stats/student_list.haml", {
        "lesson": lesson,
        "students": students
    })


@user_is_professor
def viewstats(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    students = Student.objects.filter(lesson=lesson)

    # TODO: make automatic detection of timespan instead of hard coding
    predefined_timespan = {
        "-----": None,
        "Septembre 2016 - Decembre 2016": "01/09/2016-31/12/2016",
        "Janvier 2017 - Juin 2017": "01/01/2017-31/06/2017",
        "Septembre 2017 - Decembre 2017": "01/09/2017-31/12/2017",

    }

    stats = get_class_stat(lesson)

    return render(request, "stats/viewstats.haml", {
        "stats": stats,
        "lesson": lesson,
        "student_number": len(Student.objects.filter(lesson=lesson)),
        "students": students,
        "predefined_timespan": predefined_timespan,

    })


def stat_student(request, pk_lesson, pk_student):

    predefined_timespan = {
        "-----": None,
        "Septembre 2016 - Decembre 2016": "01/09/2016-31/12/2016",
        "Janvier 2017 - Juin 2017": "01/01/2017-31/06/2017",
        "Septembre 2017 - Decembre 2017": "01/09/2017-31/12/2017",

    }

    lesson = get_object_or_404(Lesson, pk=pk_lesson)
    student = get_object_or_404(Student, pk=pk_student)
    stats = get_student_stat(student, lesson)

    return render(request, "stats/viewstats.haml", {
        "lesson": lesson,
        "student": student,
        "stats": stats,
        "predefined_timespan": predefined_timespan,

    })


def stat_student_tab(request, pk_lesson, pk_student):
    lesson = get_object_or_404(Lesson, pk=pk_lesson)
    student = get_object_or_404(Student, pk=pk_student)

    return render(request, "stats/stat_student.haml", {
        "lesson": lesson,
        "student": student
    })

