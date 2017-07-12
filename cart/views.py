from django.shortcuts import render, get_object_or_404
from cart.models import CartInfo
from django.http import JsonResponse
from usercenter.models import TTSXUser
from cart.models import CartInfo
from goods.models import GoodsInfo


# Create your views here.
def add_cart(request):
    print(request.POST, '>>>' * 20)
    uid = int(request.POST.get('uid'))
    gid = int(request.POST.get('gid'))
    gcount = int(request.POST.get('gcount'))

    cart_info = CartInfo.objects.get_or_create(user_id=uid, goods_id=gid)
    # 先查出当前数据库已存过的该用户该商品的数量
    cart_info[0].count = cart_info[0].count + gcount

    cart_info[0].save()

    return JsonResponse({'success': '1'})


def my_cart(request):
    context = {'title': '天天生鲜 - 购物车', 'subtitle': '我的购物车'}
    user = get_object_or_404(TTSXUser, pk=request.session.get('login_id'))
    context['user'] = user

    # 查询对应用户的购物车信息
    cart_info = CartInfo.objects.filter(user=user)
    goods_list = []
    # total_price = 0
    for info in cart_info:
        goods_info = get_object_or_404(GoodsInfo, pk=info.goods_id)
        # total_price += goods_info.price * info.count
        goods_list.append({'goods_info': goods_info, 'goods_count': info.count})
    print(goods_list)
    context['goods_list'] = goods_list
    # context['total_count'] = len(goods_list)
    # context['total_price'] = total_price
    return render(request, 'cart/cart.html', context=context)
