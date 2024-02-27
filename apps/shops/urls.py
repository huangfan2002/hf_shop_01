from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    # 登录注册部分的路由
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

]
