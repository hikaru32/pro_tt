from django.shortcuts import render
from cart.models import CartInfo
from django.http import JsonResponse


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

