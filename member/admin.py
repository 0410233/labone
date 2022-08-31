from django.contrib import admin

from server.utils import admin_image_view
from .models import *

# Register your models here.


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    search_fields = ("name",)
    list_filter = ("gender",)
    list_display = (
        "id", "name", "view_avatar", "gender", "birthday", "mobile",
        "created_at", "updated_at",
    )
    ordering = ('-created_at', )

    def view_avatar(self, obj: Teacher):
        if obj.avatar:
            return admin_image_view(obj.avatar.name)
        return '-'
    view_avatar.short_description = '头像'


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):

    search_fields = ("name",)
    list_filter = ("gender",)
    list_display = (
        "id", "name", "view_avatar", "gender", "birthday", "mobile",
        "created_at", "updated_at",
    )
    ordering = ('-created_at', )

    def view_avatar(self, obj: Parent):
        if obj.avatar:
            return admin_image_view(obj.avatar.name)
        return '-'
    view_avatar.short_description = '头像'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    search_fields = ("name",)
    list_filter = ("gender",)
    list_display = (
        "id", "name", "view_avatar", "gender", "birthday", "parent",
        "created_at", "updated_at",
    )
    ordering = ('-created_at', )

    def view_avatar(self, obj: Student):
        if obj.avatar:
            return admin_image_view(obj.avatar.name)
        return '-'
    view_avatar.short_description = '头像'
