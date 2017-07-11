from django.shortcuts import render
from cart.models import CartInfo

# Create your views here.
def add_cart(request):
    print(request.POST, '>>>' * 20)
    uid = request.POST.get('uid')
    gid = request.POST.get('gid')
    gcount = request.POST.get('gcount')

    cart = CartInfo()
    cart.user_id = uid
    cart.goods_id = gid
    cart.count = gcount

    # cart.save()
    

