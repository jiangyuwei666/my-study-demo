from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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


def attr(request):
    print('path', request.path)
    print('method', request.method)
    print('encoding', request.encoding)
    print('GET', request.GET)
    print('POST', request.POST)
    print('FILES', request.FILES)
    print('COOKIES', request.COOKIES)
    print('session', request.session)

    return HttpResponse('asd')


def get1(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    c = request.GET.get('c')
    return HttpResponse(a + ' ' + b + ' ' + c)


def get2(request):
    a = request.GET.getlist('a')
    c = request.GET.get('c')
    print(a)
    return HttpResponse(' '.join(a) + ' ' + c)


def register(request):
    """
    获取表单并显示
    """
    name = request.POST.get('name')
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    if 1 == int(gender):
        gender = '男'
    else:
        gender = '女'
    hobby = request.POST.getlist('hobby')
    response = HttpResponse('姓名:' + name + '\n' + '性别:' + gender + '\n' + '年龄:' + age + '\n' + '爱好:' + ','.join(hobby))
    print(response.status_code)
    print(response.content)
    print(response.charset)
    return response


def showregister(request):
    """
    显示注册界面
    """
    return render(request, 'myApp/register.html')


def redirect1(request):
    return redirect('/redirect2')


def redirect2(request):
    return HttpResponse('重定向')


# session+重定向
def main(request):
    # 取出session
    username = request.session.get('username')
    if username:
        pass
    else:
        username = '未登录，请先登录'
    return render(request, 'myApp/main.html', {'username': username})


def login(request):
    return render(request, 'myApp/login.html')


def showmain(request):
    username = request.POST.get('username')
    print(username)
    # 储存session
    request.session['username'] = username
    # request.session.set_expiry(10)# 10秒后过期
    # request.session.set_expiry()# 10秒后过期
    return redirect('/main')


from django.contrib.auth import logout


def qt(request):
    # 清楚session
    logout(request)
    # request.session.clear()
    # request.session.flush()
    return redirect('/main')


def test(request):
    return render(request, 'myApp/test.html', {'test_list': [11, 'asd']})


def firstpage(request):
    return render(request, 'myApp/firstpage.html')


def upfile(request):
    return render(request, 'myApp/upfile.html')


TEST_PATH = '.'
import os


def savefile(request):
    if request.method == "POST":
        f = request.FILES.get('file')
        path = os.path.join(TEST_PATH, f.name)
        with open(path, 'wb') as fp:
            for per in f.chunks():
                fp.write(per)
        return HttpResponse('上传成功')
    else:
        return HttpResponse('fuck wrong')
