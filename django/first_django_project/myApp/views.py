from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Class, Students
from django.db.models import *

def index(request):
    return HttpResponse('jyw666')


def classes(request):
    # 去模板里取数据
    # class_list = Class.objects.all()
    # 将数据传递给模板，模板再渲染页面，将渲染号的页面，返回给浏览器
    class_list = Class.objects.filter(cgirl_num__lt=F('cboy_num'))
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


def student_search(request):
    # student_list = Students.objects.filter(sname__contains='a')
    # student_list = Students.objects.filter(sname__startswith='j', sname__endswith='i')
    # student_list = Students.objects.filter(sname__in=['jiangyuwei', 'baoqianyue'])
    # student_list = Students.objects.filter(sage__gt=100)
    # print(Students.objects.aggregate(Max('sage')))
    student_list = Students.objects.filter(Q(sage__gt=10) | Q(sclass_id__gt=2))
    student_list1 = Students.objects.filter(sage__gt=10, sclass_id__gt=2)
    print(student_list)
    print(student_list1)
    return render(request, 'myApp/student.html', {'students': student_list})


def class_search(request):
    class_list = Class.objects.filter(cdate__month=2)
    return render(request, 'myApp/class.html', {'classes': class_list})
