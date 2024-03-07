from django.http import JsonResponse
from django.shortcuts import render, redirect

from apps.shops.models import UserInfoModel, GoodModel, CategoryModel, CommentModel, RatingModel, CollectModel


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

    # 获取用户的评论
    comments = CommentModel.objects.filter(
        good_id=good_id
    )

    user_id = request.session.get('user_id')
    flag = RatingModel.objects.filter(
        user_id=user_id,
        good_id=good_id
    ).last()

    context = {
        'good': good,
        'flag': flag,
        'comments': comments,
    }
    return render(request, 'good_detail.html', context=context)


def add_score(request):
    # 添加评分
    user_id = request.session.get('user_id')
    good_id = request.POST.get('good_id')
    score = request.POST.get('score')
    RatingModel.objects.create(
        user_id=user_id,
        good_id=good_id,
        score=score
    )
    return JsonResponse({'code': 200})


def add_comment(request):
    # 添加评论
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'code': 400, 'message': '请先登录'})
    content = request.POST.get('content')
    good_id = request.POST.get('good_id')
    if not content:
        return JsonResponse({'code': 400, 'message': '内容不能为空'})

    CommentModel.objects.create(
        user_id=user_id,
        content=content,
        good_id=good_id
    )
    return JsonResponse({'code': 200})


def add_collect(request):
    # 添加收藏
    good_id = request.POST.get('good_id')
    user_id = request.session.get('user_id')
    flag = CollectModel.objects.filter(
        user_id=user_id,
        good_id=good_id
    ).first()
    if flag:
        return JsonResponse({'code': 400, 'message': '该商品已收藏'})
    CollectModel.objects.create(
        user_id=user_id,
        good_id=good_id
    )
    return JsonResponse({'code': 200})


def delete_collect(request):
    # 取消收藏
    collect_id = request.POST.get('collect_id')
    collect = CollectModel.objects.get(id=collect_id)
    collect.delete()
    return JsonResponse({'code': 200})


def my_collect(request):
    # 我的收藏
    user_id = request.session.get('user_id')
    collects = CollectModel.objects.filter(user_id=user_id)
    return render(request, 'my_collect.html', {'collects': collects})
