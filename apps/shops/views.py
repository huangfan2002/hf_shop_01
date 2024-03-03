from django.http import JsonResponse
from django.shortcuts import render, redirect

from apps.shops.models import UserInfoModel, GoodModel, CategoryModel, CommentModel, RatingModel


# Create your views here.
def index(request):
    categories = CategoryModel.objects.all()
    context = {
        'categories': categories
    }

    return render(request, 'index.html', context=context)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        if not (username or password1 or password2):
            return JsonResponse({'code': 400, 'message': '缺少必传的参数'})

        if password1 != password2:
            return JsonResponse({'code': 400, 'message': '两次输入的密码不一致！'})

        flag = UserInfoModel.objects.filter(username=username).first()
        if flag:
            return JsonResponse({'code': 400, 'message': '该用户名已存在'})
        UserInfoModel.objects.create(
            username=username,
            password=password1,
            phone=phone
        )
        return JsonResponse({'code': 200})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 用户登录
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username or password):
            return JsonResponse({'code': 400, 'message': '缺少必传的参数'})
        user = UserInfoModel.objects.filter(username=username, password=password).first()
        if not user:
            return JsonResponse({'code': 400, 'message': '账号或密码错误'})
        request.session['login_in'] = True
        request.session['username'] = user.username
        request.session['user_id'] = user.id
        return JsonResponse({'code': 200})


def logout(request):
    # 退出登录
    flag = request.session.clear()
    return redirect('/')


def good_list(request, category_id):
    if request.method == 'GET':
        # 商品列表
        goods = GoodModel.objects.filter(
            category_id=category_id
        )
        context = {
            'goods': goods
        }
        return render(request, 'good_list.html', context=context)


def good_detail(request, good_id):
    # 图书详情界面
    good = GoodModel.objects.filter(
        id=good_id
    ).first()
    user_id = request.session.get('user_id')

    context = {
        'good': good,
    }
    return render(request, 'good_detail.html', context=context)