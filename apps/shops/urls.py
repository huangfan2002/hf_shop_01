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

    # 添加收藏，删除收藏，展示收藏
    path('add_collect/', views.add_collect, name='add_collect'),
    path('delete_collect/', views.delete_collect, name='delete_collect'),
    path('my_collect/', views.my_collect, name='my_collect'),

    # 购买商品，展示订单，取消订单
    path('my_order/', views.my_order, name='my_order'),
    path('add_order/', views.add_order, name='add_order'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),

    # 商品推荐
    path('recommend_goods/', views.recommend_goods, name='recommend_goods'),

    # 添加购物车
    path('add_shoppingcar/', views.add_shoppingcar, name='add_shoppingcar'),
    path('delete_shoppingcar/', views.delete_shoppingcar, name='delete_shoppingcar'),
    path('my_shoppingcar/', views.my_shoppingcar, name='my_shoppingcar'),
]
