from django.db import models
from django.utils import timezone

from server.utils import get_file_path

# Create your models here.


class LessonGroup(models.Model):
    """课程分组"""
    
    name = models.CharField('组名', max_length='50')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.pk), self.name)

    class Meta:
        verbose_name = '课程分组'
        verbose_name_plural = verbose_name
        db_table = 'lesson_groups'
        ordering = ('-created_at',)


class Lesson(models.Model):
    """课程"""
    
    name = models.CharField('课程名', max_length='50')
    image = models.ImageField('图片', upload_to=get_file_path, max_length=500, blank=True, null=True)
    content = models.TextField('课程介绍', blank=True, null=True)

    status = models.BooleanField('启用', blank=True, default=True, help_text='已经不用的课程不要删除，取消启用即可')

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

    lesson = models.ForeignKey('teaching.Lesson', on_delete=models.CASCADE, verbose_name='课程')
    teacher = models.ForeignKey('member.Teacher', on_delete=models.SET_NULL, verbose_name='老师', blank=True, null=True)
    group = models.ForeignKey('teaching.LessonGroup', on_delete=models.CASCADE, verbose_name='分组')

    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    max_student = models.IntegerField('学生人数', blank=True, default=10, help_text='最大学生人数')
    student_count = models.IntegerField('报名人数', blank=True, default=0)

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


class TimetableStudent(models.Model):
    """报名"""
    
    timetable = models.ForeignKey('teaching.Timetable', on_delete=models.CASCADE, verbose_name='课表')
    student = models.ForeignKey('member.Student', on_delete=models.CASCADE, verbose_name='学生')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}--{}'.format(str(self.student), str(self.timetable))

    class Meta:
        verbose_name = '报名'
        verbose_name_plural = verbose_name
        db_table = 'timetable_students'
        ordering = ('-created_at',)


class TeacherSignin(models.Model):
    """教师签到"""
    
    timetable = models.ForeignKey('teaching.Timetable', on_delete=models.CASCADE, verbose_name='课表')
    teacher = models.ForeignKey('member.Teacher', on_delete=models.CASCADE, verbose_name='老师')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.timetable), str(self.teacher))

    class Meta:
        verbose_name = '教师签到'
        verbose_name_plural = verbose_name
        db_table = 'teacher_signin'
        ordering = ('-created_at',)


class StudentSignin(models.Model):
    """学生签到"""
    
    timetable = models.ForeignKey('teaching.Timetable', on_delete=models.CASCADE, verbose_name='课表')
    student = models.ForeignKey('member.Student', on_delete=models.CASCADE, verbose_name='学生')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.timetable), str(self.student))

    class Meta:
        verbose_name = '学生签到'
        verbose_name_plural = verbose_name
        db_table = 'student_signin'
        ordering = ('-created_at',)


class TeacherSigninReport(models.Model):
    """教师签到统计"""

    group = models.ForeignKey('teaching.LessonGroup', on_delete=models.CASCADE, verbose_name='分组')
    teacher = models.ForeignKey('member.Teacher', on_delete=models.CASCADE, verbose_name='老师')
    should_signin = models.IntegerField('应到', blank=True, default=0)
    actual_signin = models.IntegerField('实到', blank=True, default=0)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.group), str(self.teacher))

    class Meta:
        verbose_name = '教师签到统计'
        verbose_name_plural = verbose_name
        db_table = 'teacher_signin_report'
        ordering = ('-created_at',)


class StudentSigninReport(models.Model):
    """学生签到统计"""

    group = models.ForeignKey('teaching.LessonGroup', on_delete=models.CASCADE, verbose_name='分组')
    student = models.ForeignKey('member.Student', on_delete=models.CASCADE, verbose_name='学生')
    should_signin = models.IntegerField('应到', blank=True, default=0)
    actual_signin = models.IntegerField('实到', blank=True, default=0)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.group), str(self.student))

    class Meta:
        verbose_name = '学生签到统计'
        verbose_name_plural = verbose_name
        db_table = 'student_signin_report'
        ordering = ('-created_at',)
