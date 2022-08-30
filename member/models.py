from django.db import models

from server.utils import get_file_path

# Create your models here.


class Teacher(models.Model):
    """教师"""

    name = models.CharField('姓名', max_length='50')
    avatar = models.ImageField('头像', upload_to=get_file_path, max_length=500, blank=True, null=True)
    gender = models.IntegerField('性别', default=0, choices=[(0, '未设置'), (1, '男'), (2, '女')])
    birthday = models.DateField('生日', blank=True, null=True)
    mobile = models.CharField('联系方式', max_length='50')
    # grade = models.ForeignKey('setting.Grade', on_delete=models.SET_NULL, verbose_name='年级id', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(self.name, self.mobile)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
        db_table = 'teachers'
        ordering = ('-created_at',)



class Parent(models.Model):
    """家长"""

    name = models.CharField('姓名', max_length='50')
    avatar = models.ImageField('头像', upload_to=get_file_path, max_length=500, blank=True, null=True)
    gender = models.IntegerField('性别', default=0, choices=[(0, '未设置'), (1, '男'), (2, '女')])
    birthday = models.DateField('生日', blank=True, null=True)
    mobile = models.CharField('联系方式', max_length='50')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(self.name, self.mobile)

    class Meta:
        verbose_name = '家长'
        verbose_name_plural = verbose_name
        db_table = 'parents'
        ordering = ('-created_at',)



class Student(models.Model):
    """学生"""

    name = models.CharField('姓名', max_length='50')
    avatar = models.ImageField('头像', upload_to=get_file_path, max_length=500, blank=True, null=True)
    gender = models.IntegerField('性别', default=0, choices=[(0, '未设置'), (1, '男'), (2, '女')])
    birthday = models.DateField('生日', blank=True, null=True)
    parent = models.ForeignKey('member.Parent', on_delete=models.SET_NULL, verbose_name='家长', blank=True, null=True)
    # grade = models.ForeignKey('setting.Grade', on_delete=models.SET_NULL, verbose_name='年级', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.pk), self.name)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
        db_table = 'students'
        ordering = ('-created_at',)
