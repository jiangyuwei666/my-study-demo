from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),  # 用正则匹配
    url(r'^class/$', views.classes),
    url(r'^student/$', views.students),
    url(r'^class/(\d+)$', views.class_students),
    url(r'^student/(\d+)$', views.student_info),
    url(r'^studentsearch/$', views.student_search),
    url(r'^classsearch/$', views.class_search),
]
