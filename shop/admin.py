from django.contrib import admin

from server.utils import admin_image_view, admin_text_view
from .models import *

# Register your models here.


@admin.register(PointLog)
class PointLogAdmin(admin.ModelAdmin):

    search_fields = ("student__name",)
    list_filter = ("created_at",)
    list_display = (
        "id", "student", "log_type", "points", "remark", "created_at",
    )
    ordering = ('-created_at', )


@admin.register(PointReport)
class PointReportAdmin(admin.ModelAdmin):

    search_fields = ("student__name",)
    list_display = (
        "id", "student", "points", "created_at", "updated_at",
    )
    ordering = ('-updated_at', )


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):

    search_fields = ("name",)
    list_display = (
        "id", "name", "view_image", "price", "stock", "created_at", "updated_at",
    )
    ordering = ('-created_at', )

    def view_image(self, obj: Goods):
        if obj.image:
            return admin_image_view(obj.image.name)
        return '-'
    view_image.short_description = '图片'


@admin.register(ExchangeLog)
class ExchangeLogAdmin(admin.ModelAdmin):

    search_fields = ("student__name", "goods__name",)
    list_filter = ("created_at",)
    list_display = (
        "id", "student", "goods", "points", "created_at",
    )
    ordering = ('-created_at', )
