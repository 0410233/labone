import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdmin1
from django.utils.translation import gettext, gettext_lazy as _
from django.conf import settings
# from platter.views import get_client_ip, getWxPayForC, _order_num
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from server.utils import admin_image_view
from .models import *


# Register your models here.

admin.site.site_header = '一号实验室'
admin.site.site_title = '一号实验室后台管理系统'

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(User)
class UserAdmin(UserAdmin1):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ("name", "avatar", "gender", "birthday", "openid", "unionid", "session_key", "wx_user_info", "role", "tags" )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', "name", "openid", "unionid", "wx_user_info", )
    list_display = ('id', 'username', "name", 'view_avatar', "gender", 'birthday', 'role', 'date_joined', 'last_login')
    list_filter = ("role", 'gender', 'is_active', )

    list_per_page = 20

    ordering = ('-date_joined',)

    def view_avatar(self, obj):
        if obj.avatar:
            return admin_image_view(obj.avatar.name)
        else:
            return '-'
    view_avatar.short_description = '头像'
