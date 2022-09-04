from django.db import models
from django.utils import timezone

from server.utils import get_file_path

# Create your models here.


class Group(models.Model):
    """分组"""
    
    name = models.CharField('组名', max_length=50)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.pk), self.name)

    class Meta:
        verbose_name = '分组'
        verbose_name_plural = verbose_name
        db_table = 'groups'
        ordering = ('-created_at',)


class Grade(models.Model):
    """年级"""

    name = models.CharField('年级', max_length=50)
    display = models.IntegerField('显示顺序', blank=True, default=0, help_text='大的靠前')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = '年级'
        verbose_name_plural = verbose_name
        db_table = 'grades'
        ordering = ('-display', '-created_at')


class Lesson(models.Model):
    """课程"""
    
    name = models.CharField('课程名', max_length=50)
    grade = models.ForeignKey('lesson.Grade', on_delete=models.SET_NULL, verbose_name='年级', blank=True, null=True)
    image = models.ImageField('图片', upload_to=get_file_path, max_length=500, blank=True, null=True)
    content = models.TextField('课程介绍', blank=True, null=True)

    is_active = models.BooleanField('是否启用', blank=True, default=True, help_text='不用的课程不要删除，设置为不启用即可')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.pk), self.name)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        db_table = 'lessons'
        ordering = ('-created_at',)


class Timetable(models.Model):
    """课表"""

    lesson = models.ForeignKey('lesson.Lesson', on_delete=models.CASCADE, verbose_name='课程')
    grade = models.ForeignKey('lesson.Grade', on_delete=models.CASCADE, verbose_name='年级')
    group = models.ForeignKey('lesson.Group', on_delete=models.CASCADE, verbose_name='分组')
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')

    teacher = models.ForeignKey('member.Teacher', on_delete=models.SET_NULL, verbose_name='老师', blank=True, null=True)

    max_student = models.IntegerField('课堂人数', blank=True, default=10, help_text='最大学生人数')
    student_count = models.IntegerField('报名人数', blank=True, default=0)

    is_active = models.BooleanField('是否启用', blank=True, default=True, help_text='停掉的课表不要删除，设置为不启用即可')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        tz = timezone.get_current_timezone()
        return '{}({})'.format(self.lesson.name, self.start_time.astimezone(tz).strftime('%m-%d'))

    class Meta:
        verbose_name = '课表'
        verbose_name_plural = verbose_name
        db_table = 'timetables'
        ordering = ('-created_at',)
