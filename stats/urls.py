from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^lesson/(?P<pk>\d+)/stats/$', views.viewstats, name='viewstats'),
    url(r'^lesson/(?P<pk>\d+)/stats/export/$', views.exportCSV, name='exportCSV'),
    url(r'^lesson/(?P<pk>\d+)/stats/students$', views.view_student, name='view_student'),
    url(r'^lesson/(?P<pk_lesson>\d+)/stats/students/(?P<pk_student>\d+)$', views.stat_student, name='stat_student'),
    url(r'^statistics/student/(?P<student>[a-zAZ0-9]+)', views.dashboard, name='dashboard2'),
    url(r'^statistics/classroom/(?P<class>[a-zA-Z0-9]+)', views.dashboard, name='dashboard3'),
]
