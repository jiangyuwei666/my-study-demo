from django.contrib import admin

# Register your models here.
from .models import Class, Students


# 创建时会选择添加若干个学生
class StudentInfo(admin.TabularInline):
    model = Students  # 关联类
    extra = 2  # 学生个数


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    inlines = [StudentInfo]
    # 列表页属性
    list_display = ['pk', 'cname', 'cdate', 'cgirl_num', 'cboy_num']  # 显示字段
    list_filter = ['cname']  # 过滤字段
    search_fields = ['cname']  # 搜索字段
    list_per_page = 5  # 分页，每5条一页
    # 添加、修改页
    # fields = []  # 属性的先后顺序
    fieldsets = [
        ("num", {"fields": ['cboy_num', 'cgirl_num']}),
        ("base", {"fields": ['cdate', 'cname', 'is_delete']})
    ]  # 给属性分组  两个属性不能同时使用


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    def gender(self):
        if self.sgender:
            return '男'
        else:
            return '女'

    # 设置页面的列的名称
    gender.short_description = '性别哟栽种'
    list_display = ['pk', 'sname', 'sage', gender, 'scomment', 'sclass']

    list_per_page = 3
    # 执行动作的位置
    actions_on_bottom = True
    actions_on_top = False

# admin.site.register(Class, ClassAdmin)
# admin.site.register(Students, StudentAdmin)
