import numpy as np
from django.http import JsonResponse
from django.shortcuts import render, redirect

from apps.shops.models import UserInfoModel, GoodModel, CategoryModel, CommentModel, RatingModel, CollectModel, \
    OrderModel, ShoppingCarModel


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

    # 如果初始没有评分，创建评分，如果有评分 修改评分
    flag = RatingModel.objects.filter(
        user_id=user_id,
        good_id=good_id
    ).first()
    if flag:
        flag.score = score
        flag.save()
        return JsonResponse({'code': 200})
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


def my_order(request):
    # 我的订单
    user_id = request.session.get('user_id')
    orders = OrderModel.objects.filter(user_id=user_id)
    return render(request, 'my_order.html', {'orders': orders})


def add_order(request):
    # 购买物品
    good_id = request.POST.get('good_id')
    user_id = request.session.get('user_id')
    good = GoodModel.objects.get(id=good_id)
    if good.number == 0:
        return JsonResponse({'code': 400, 'message': '该商品暂无库存，请联系管理员'})
    good.number -= 1
    good.save()
    OrderModel.objects.create(
        user_id=user_id,
        good_id=good_id,
        is_buy=True
    )
    return JsonResponse({'code': 200})


def cancel_order(request):
    # 取消订单
    order_id = request.POST.get('order_id')
    order = OrderModel.objects.get(id=order_id)
    order.is_buy = False
    order.good.number += 1
    order.good.save()
    order.save()
    return JsonResponse({'code': 200})


def calculate_cosine_similarity(user_ratings1, user_ratings2):
    # 将用户1的商品评分存入字典，键为商品ID，值为评分
    good_ratings1 = {rating.good_id: rating.score for rating in user_ratings1}
    # 将用户2的商品评分存入字典，键为商品ID，值为评分
    good_ratings2 = {rating.good_id: rating.score for rating in user_ratings2}

    # 找出两个用户共同评价过的商品
    common_goods = set(good_ratings1.keys()) & set(good_ratings2.keys())

    if len(common_goods) == 0:
        return 0.0  # 无共同评价的商品，相似度为0

    # 提取共同评价商品的评分，存入NumPy数组
    user1_scores = np.array([good_ratings1[good_id] for good_id in common_goods])
    user2_scores = np.array([good_ratings2[good_id] for good_id in common_goods])

    # 计算余弦相似度
    cosine_similarity = np.dot(user1_scores, user2_scores) / (
            np.linalg.norm(user1_scores) * np.linalg.norm(user2_scores))
    return cosine_similarity


def user_based_recommendation(request, user_id):
    try:
        # 获取目标用户对象
        target_user = UserInfoModel.objects.get(pk=user_id)
    except UserInfoModel.DoesNotExist:
        return JsonResponse({'error': '用户不存在'}, status=404)

    # 获取目标用户的商品评分记录
    target_user_ratings = RatingModel.objects.filter(user=target_user)

    # 用于存储推荐商品的字典
    recommended_goods = {}

    # 遍历除目标用户外的所有其他用户
    for other_user in UserInfoModel.objects.exclude(pk=user_id):
        # 获取其他用户的商品评分记录
        other_user_ratings = RatingModel.objects.filter(user=other_user)

        # 计算目标用户与其他用户的相似度
        similarity = calculate_cosine_similarity(target_user_ratings, other_user_ratings)

        if similarity > 0:
            # 遍历其他用户评价的商品
            for good_rating in other_user_ratings:
                # 仅考虑目标用户未评价过的商品
                if good_rating.good not in target_user_ratings.values_list('good', flat=True):
                    if good_rating.good.id in recommended_goods:
                        # 累积相似度加权的评分和相似度
                        recommended_goods[good_rating.good.id]['score'] += similarity * good_rating.score
                        recommended_goods[good_rating.good.id]['similarity'] += similarity
                    else:
                        # 创建推荐商品的记录
                        recommended_goods[good_rating.book.id] = {'score': similarity * good_rating.score,
                                                                  'similarity': similarity}

    # 将推荐商品按照加权评分排序
    sorted_recommended_goods = sorted(recommended_goods.items(), key=lambda x: x[1]['score'], reverse=True)

    # 获取排名靠前的推荐商品的ID
    top_recommended_goods = [book_id for book_id, _ in sorted_recommended_goods[:5]]

    # 构建响应数据
    response_data = []
    for good_id in top_recommended_goods:
        good = GoodModel.objects.get(pk=good_id)
        similarity = recommended_goods[good_id]['similarity']
        response_data.append({
            'name': good.name,
            'content': good.content,
            'id': good.id,
            'image': good.image,
            'category': good.category,
            'number': good.number,
            'similarity': similarity,
        })

    return response_data


def recommend_goods(request):
    # 商品推荐
    user_id = request.session.get('user_id')
    resp_list = user_based_recommendation(request, user_id)
    return render(request, 'recommend_goods.html', {'resp_list': resp_list})


# 添加购物车
def add_shoppingcar(request):
    good_id = request.POST.get('good_id')
    user_id = request.session.get('user_id')
    good = GoodModel.objects.get(id=good_id)
    if good.number == 0:
        return JsonResponse({'code': 400, 'message': '该商品暂无库存，请联系管理员'})
    ShoppingCarModel.objects.create(
        user_id=user_id,
        good_id=good_id,
    )
    return JsonResponse({'code': 200})


# 移出购物车
def delete_shoppingcar(request):
    my_shopping_car_id = request.POST.get('my_shopping_car_id')
    delete_shoppingcar = ShoppingCarModel.objects.get(id=my_shopping_car_id)
    delete_shoppingcar.delete()
    return JsonResponse({'code': 200})


def my_shoppingcar(request):
    user_id = request.session.get('user_id')
    shopping_car = ShoppingCarModel.objects.filter(user_id=user_id)
    return render(request, 'my_shoppingcar.html', {'shoppingcars': shopping_car})
