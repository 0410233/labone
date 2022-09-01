from django.contrib import admin

from server.utils import admin_image_view, admin_text_view
from .models import *


# Register your models here.



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
