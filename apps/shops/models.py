from django.db import models

# Create your models here.


class UserInfoModel(models.Model):
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    phone = models.CharField(max_length=100, verbose_name='手机号')
    address = models.CharField(max_length=100,verbose_name='地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# python manage.py makemigrations shop
