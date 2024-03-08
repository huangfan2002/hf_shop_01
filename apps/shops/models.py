from django.db import models


# Create your models here.


class UserInfoModel(models.Model):
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    phone = models.CharField(max_length=100, verbose_name='手机号')
    address = models.CharField(max_length=100, verbose_name='地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 类别信息
class CategoryModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_category'
        verbose_name = '类别信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    price = models.IntegerField(verbose_name='价格')
    image = models.ImageField(upload_to='', max_length=300, verbose_name='图片')
    content = models.TextField(verbose_name='介绍')
    number = models.IntegerField(verbose_name='数量')
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE, verbose_name='所属分类')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_good'
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    good = models.ForeignKey('GoodModel', on_delete=models.CASCADE, verbose_name='所属商品')
    user = models.ForeignKey('UserInfoModel', on_delete=models.CASCADE, verbose_name='所属用户')
    is_buy = models.BooleanField(default=False, verbose_name='是否购买')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_order'
        verbose_name = '用户订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.good.name


class HotModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    good = models.ForeignKey('GoodModel', on_delete=models.CASCADE, verbose_name='热门商品')

    class Meta:
        db_table = 'db_hot'
        verbose_name = '热门商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CommentModel(models.Model):
    user = models.ForeignKey('UserInfoModel', on_delete=models.CASCADE, verbose_name='所属用户')
    good = models.ForeignKey('GoodModel', on_delete=models.CASCADE, verbose_name='所属商品')
    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_comment'
        verbose_name = '评论信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class CollectModel(models.Model):
    user = models.ForeignKey('UserInfoModel', on_delete=models.CASCADE, verbose_name='所属用户')
    good = models.ForeignKey('GoodModel', on_delete=models.CASCADE, verbose_name='所属商品')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_collect'
        verbose_name = '收藏信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class RatingModel(models.Model):
    good = models.ForeignKey('GoodModel', on_delete=models.CASCADE, verbose_name='所属商品')
    user = models.ForeignKey('UserInfoModel', on_delete=models.CASCADE, verbose_name='所属用户')
    score = models.IntegerField(verbose_name='评分')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'db_rating'
        verbose_name = '评分信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.score)

# python manage.py makemigrations shops
