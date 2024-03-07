from django.contrib import admin
from django.utils.html import format_html
# Register your models here.

from .models import GoodModel, CategoryModel, UserInfoModel, CommentModel, RatingModel


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'phone', 'address', 'create_time')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')


class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'number', 'image_tag', 'category')

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="/image/{}" style="width:70px;height:100px;"/>'.format(obj.image))
        return ""

    image_tag.allow_tags = True
    image_tag.short_description = '照片'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'good', 'content')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('good', 'user', 'score', 'create_time')


admin.site.register(UserInfoModel, UserInfoAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(GoodModel, GoodAdmin)

admin.site.register(CommentModel, CommentAdmin)
admin.site.register(RatingModel, RatingAdmin)

admin.site.site_header = '商城后台管理系统'
