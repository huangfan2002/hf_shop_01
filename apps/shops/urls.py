from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    # 登录注册部分的路由
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # 商品展示部分路由
    path('good_list/<int:category_id>/', views.good_list, name='good_list'),
    path('good_detail/<int:good_id>/', views.good_detail, name='good_detail'),

    # 添加评分
    path('add_score/', views.add_score, name='add_score'),

    # 添加评论
    path('add_comment/', views.add_comment, name='add_comment'),
]
