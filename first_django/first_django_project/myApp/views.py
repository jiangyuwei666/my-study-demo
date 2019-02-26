from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Class, Students


def index(request):
    return HttpResponse('jyw666')


def classes(request):
    # 去模板里取数据
    class_list = Class.objects.all()
    # 将数据传递给模板，模板再渲染页面，将渲染号的页面，返回给浏览器
    return render(request, 'myApp/class.html', {"classes": class_list})


def students(request):
    student_list = Students.objects.all()
    return render(request, 'myApp/student.html', {"students": student_list})


def class_students(request, num):
    # 获得对应的班级对象
    class1 = Class.objects.get(pk=num)
    # 获得学生集合
    student_list = class1.students_set.all()
    return render(request, 'myApp/student.html', {"students": student_list})


def student_info(request, num):
    student = Students.objects.get(pk=num)
    return render(request, 'myApp/student_info.html', {"student": student})
