from django.contrib import admin
from django.utils.html import format_html
# Register your models here.

from .models import GoodModel, CategoryModel, UserInfoModel


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'phone', 'address', 'create_time')


admin.site.register(UserInfoModel, UserInfoAdmin)
