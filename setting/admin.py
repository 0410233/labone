from django.contrib import admin
from django import forms

from . import models
from user.admin import BaseAdmin
from server.utils import admin_text_view


# Register your models here.


@admin.register(models.UserSetting)
class UserSettingAdmin(BaseAdmin):

    list_filter = ('group', 'scope')
    list_display = ('name', 'view_value', 'display', 'group', 'scope')
    readonly_fields = ('key','name',)
    ordering = ('-display', 'id')

    def view_value(self, obj):
        return admin_text_view(obj.value, width=400)
    view_value.short_description = '值'



@admin.register(models.SystemTaskLog)
class SystemTaskLogAdmin(BaseAdmin):
    list_display = ("id", "task_type", "remark", "created_at", )
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
        