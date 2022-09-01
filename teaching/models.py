from django.db import models
from django.utils import timezone

from server.utils import get_file_path

# Create your models here.


class TimetableStudent(models.Model):
    """课程报名"""
    
    timetable = models.ForeignKey('lesson.Timetable', on_delete=models.CASCADE, verbose_name='课表')
    student = models.ForeignKey('member.Student', on_delete=models.CASCADE, verbose_name='学生')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}--{}'.format(str(self.student), str(self.timetable))

    class Meta:
        verbose_name = '课程报名'
        verbose_name_plural = verbose_name
        db_table = 'timetable_students'
        ordering = ('-created_at',)


class TeacherSignin(models.Model):
    """老师签到"""
    
    timetable = models.ForeignKey('lesson.Timetable', on_delete=models.CASCADE, verbose_name='课表')
    teacher = models.ForeignKey('member.Teacher', on_delete=models.CASCADE, verbose_name='老师')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(str(self.timetable), str(self.teacher))

    class Meta:
        verbose_name = '老师签到'
        verbose_name_plural = verbose_name
        db_table = 'teacher_signin'
        ordering = ('-created_at',)


class StudentSignin(models.Model):
    """学生签到"""
    
    timetable = models.ForeignKey('lesson.Timetable', on_delete=models.CASCADE, verbose_name='课表')
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


# class TeacherSigninReport(models.Model):
#     """教师签到统计"""

#     group = models.ForeignKey('teaching.LessonGroup', on_delete=models.CASCADE, verbose_name='分组')
#     teacher = models.ForeignKey('member.Teacher', on_delete=models.CASCADE, verbose_name='老师')
#     should_signin = models.IntegerField('应到', blank=True, default=0)
#     actual_signin = models.IntegerField('实到', blank=True, default=0)

#     created_at = models.DateTimeField('创建时间', auto_now_add=True)
#     updated_at = models.DateTimeField('修改时间', auto_now=True)

#     def __str__(self) -> str:
#         return '{}-{}'.format(str(self.group), str(self.teacher))

#     class Meta:
#         verbose_name = '教师签到统计'
#         verbose_name_plural = verbose_name
#         db_table = 'teacher_signin_report'
#         ordering = ('-created_at',)


# class StudentSigninReport(models.Model):
#     """学生签到统计"""

#     group = models.ForeignKey('teaching.LessonGroup', on_delete=models.CASCADE, verbose_name='分组')
#     student = models.ForeignKey('member.Student', on_delete=models.CASCADE, verbose_name='学生')
#     should_signin = models.IntegerField('应到', blank=True, default=0)
#     actual_signin = models.IntegerField('实到', blank=True, default=0)

#     created_at = models.DateTimeField('创建时间', auto_now_add=True)
#     updated_at = models.DateTimeField('修改时间', auto_now=True)

#     def __str__(self) -> str:
#         return '{}-{}'.format(str(self.group), str(self.student))

#     class Meta:
#         verbose_name = '学生签到统计'
#         verbose_name_plural = verbose_name
#         db_table = 'student_signin_report'
#         ordering = ('-created_at',)
