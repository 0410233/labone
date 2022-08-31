from django.contrib import admin

from server.utils import admin_image_view, admin_text_view
from .models import *


# Register your models here.


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    search_fields = ("name",)
    list_display = (
        "id", "name", "created_at", "updated_at",
    )
    ordering = ('-created_at', )


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):

    list_display = (
        "id", "name", "display", "created_at", "updated_at",
    )
    ordering = ('-display', '-created_at', )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    search_fields = ("name",)
    list_filter = ("grade",)
    list_display = (
        "id", "name", "grade", "view_image", "view_content", "is_active", "created_at", "updated_at",
    )
    ordering = ('-created_at', )

    def view_image(self, obj: Lesson):
        if obj.image:
            return admin_image_view(obj.image.name)
        return '-'
    view_image.short_description = '图片'

    def view_content(self, obj: Lesson):
        return admin_text_view(obj.content)
    view_content.short_description = '课程介绍'


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):

    search_fields = ("teacher__name",)
    list_filter = ("lesson", "grade", "group")
    list_display = (
        "id", "lesson", "grade", "group", "start_time", "end_time", "teacher",
        "max_student", "student_count", "is_active", "created_at", "updated_at",
    )
    ordering = ('-created_at', )


@admin.register(TimetableStudent)
class TimetableStudentAdmin(admin.ModelAdmin):

    list_filter = ("created_at",)
    list_display = (
        "id", "timetable", "student", "created_at",
    )
    ordering = ('-created_at', )


@admin.register(TeacherSignin)
class TeacherSigninAdmin(admin.ModelAdmin):

    list_filter = ("created_at",)
    list_display = (
        "id", "timetable", "teacher", "created_at",
    )
    ordering = ('-created_at', )


@admin.register(StudentSignin)
class StudentSigninAdmin(admin.ModelAdmin):

    list_filter = ("created_at",)
    list_display = (
        "id", "timetable", "student", "created_at",
    )
    ordering = ('-created_at', )
