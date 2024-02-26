from django.urls import path
from . import views

app_name = 'shop'
urlpatterns =[
    # 登录部分的路由
    path('',views.index,name = 'index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name = 'register'),
    path('logout/',views.logout,name = 'logout'),


]