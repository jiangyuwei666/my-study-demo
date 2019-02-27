from django.db import models


# Create your models here.
class Class(models.Model):
    cname = models.CharField(max_length=20)
    cdate = models.DateField()
    cgirl_num = models.IntegerField()
    cboy_num = models.IntegerField()
    is_delete = models.BooleanField()

    def __str__(self):
        return "班级名：{cname}\n创建时间：{cdate}".format(cname=self.cname, cdate=self.cdate)
    class Meta:
        ordering = ['cname']
        db_table = 'class'

class Students(models.Model):
    sname = models.CharField(max_length=20)  # 字符型，最大长度为20字节
    sgender = models.BooleanField(default=True)  # boolean类型 设置默认为True
    sage = models.IntegerField()  # 整型
    scomment = models.CharField(max_length=20)
    is_delete = models.BooleanField()
    # 关联外键
    sclass = models.ForeignKey("Class")

    class Meta:
        db_table = "students"
        ordering = ['id']
