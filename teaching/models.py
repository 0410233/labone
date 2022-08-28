from django.db import models

# Create your models here.



class Teacher(models.Model):
    """教师"""

    name = models.CharField('姓名', max_length='50')
    mobile = models.CharField('联系方式', max_length='50')
    grade = models.ForeignKey('setting.Grade', on_delete=models.SET_NULL, verbose_name='年级id', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

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
    mobile = models.CharField('联系方式', max_length='50')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

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
    parent = models.ForeignKey('teaching.Parent', on_delete=models.SET_NULL, verbose_name='家长', blank=True, null=True)
    grade = models.ForeignKey('setting.Grade', on_delete=models.CASCADE, verbose_name='年级')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.pk), self.name)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
        db_table = 'students'
        ordering = ('-created_at',)
