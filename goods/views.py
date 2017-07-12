from django.shortcuts import render, get_object_or_404
from usercenter.models import TTSXUser
from goods.models import GoodsInfo, GoodsCategory, PicTest
from django.db.models import Sum
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from cart.models import CartInfo

# Create your views here.
goods_num_per_page = 3


def index(request):
    is_login = request.session.get('is_login', '0')
    if is_login == '1':
        user = get_object_or_404(TTSXUser, pk=request.session.get('login_id'))
        # 通过聚合函数，获取同一用户所有的商品数
        cart_amount = CartInfo.objects.filter(user=user).aggregate(Sum('count')).get('count__sum')
        context = {'title': '天天生鲜 - 首页', 'sectop': '0', 'user': user, 'cart_amount': cart_amount}
    else:
        context = {'title': '天天生鲜 - 首页', 'sectop': '0'}
    # 每一类商品：最新 + 点击最多
    goods_list = []
    for category in GoodsCategory.objects.all():
        new_list = category.goodsinfo_set.order_by('-id')[:4]
        click_list = category.goodsinfo_set.order_by('-click')[:3]
        goods_list.append({'new_list': new_list, 'click_list': click_list, 'cat_name': category.name})
    context['goods_list'] = goods_list
    return render(request, 'goods/index.html', context=context)


def goods_list(request, cat):
    is_login = request.session.get('is_login', '0')
    category = get_object_or_404(GoodsCategory, pk=cat)
    new_list = category.goodsinfo_set.order_by('-id')[:2]
    goods = category.goodsinfo_set.order_by('-id')[:goods_num_per_page]
    loop_num = (len(category.goodsinfo_set.order_by('-id')) - 1) // goods_num_per_page + 1
    # print(loop_num)
    # paginator = Paginator(goods, 4)
    # page = paginator.page(1)
    if is_login == '1':
        user = get_object_or_404(TTSXUser, pk=request.session.get('login_id'))
        # 通过聚合函数，获取同一用户所有的商品数
        cart_amount = CartInfo.objects.filter(user=user).aggregate(Sum('count')).get('count__sum')
        context = {'title': '天天生鲜 - 分类', 'sectop': '0', 'category': category, 'user': user,
                   'cart_amount': cart_amount, 'new_list': new_list, 'goods': goods, 'loop_num': loop_num}
    else:
        context = {'title': '天天生鲜 - 分类', 'sectop': '0', 'category': category,
                   'new_list': new_list, 'goods': goods, 'loop_num': loop_num}
    return render(request, 'goods/list.html', context=context)


def goods_order(request):
    pn = int(request.GET.get('pn'))
    cat_id = request.GET.get('cat')
    how = str(request.GET.get('how'))
    # print(pn, '=====', how, '=====')
    if how == '-1':
        price_qur = get_object_or_404(GoodsCategory, pk=int(cat_id)).goodsinfo_set.order_by('-price')[
                    goods_num_per_page * (pn - 1):goods_num_per_page * pn]
    elif how == '1':
        price_qur = get_object_or_404(GoodsCategory, pk=int(cat_id)).goodsinfo_set.order_by('price')[
                    goods_num_per_page * (pn - 1):goods_num_per_page * pn]
    elif how == 'default':
        price_qur = get_object_or_404(GoodsCategory, pk=int(cat_id)).goodsinfo_set.order_by('-id')[
                    goods_num_per_page * (pn - 1):goods_num_per_page * pn]
    else:
        price_qur = get_object_or_404(GoodsCategory, pk=int(cat_id)).goodsinfo_set.order_by('-click')[
                    goods_num_per_page * (pn - 1):goods_num_per_page * pn]
    price_list = []
    for price in price_qur:
        mdict = model_to_dict(price, fields=['id', 'name', 'price', 'pic', 'unit'])
        mdict['pic'] = mdict['pic'].url
        price_list.append(mdict)
    # print(price_list)
    return JsonResponse({'goods': price_list})


def detail(request, gid):
    is_login = request.session.get('is_login', '0')
    print(is_login,'is_login===='*6)
    goods = get_object_or_404(GoodsInfo, pk=int(gid))
    goods.click += 1
    goods.save()
    new_list = goods.category.goodsinfo_set.order_by('-id')[:2]
    if is_login == '1':
        user = get_object_or_404(TTSXUser, pk=request.session.get('login_id'))
        # 通过聚合函数，获取同一用户所有的商品数
        cart_amount = CartInfo.objects.filter(user=user).aggregate(Sum('count')).get('count__sum')
        context = {'title': '天天生鲜 - 分类', 'sectop': '0',
                   'user': user, 'cart_amount': cart_amount,
                   'goods': goods, 'new_list': new_list}
    else:
        context = {'title': '天天生鲜 - 分类', 'sectop': '0',
                   'goods': goods, 'new_list': new_list}
    response = render(request, 'goods/detail.html', context=context)
    wids_list = request.COOKIES.get('wids', '').split(',')
    if gid in wids_list:
        wids_list.remove(gid)
    wids_list.insert(0, gid)
    if len(wids_list) > 5:
        wids_list.pop()
    # print(wids_list, '=>>>' * 30)
    response.set_cookie('wids', ','.join(wids_list), max_age=60 * 60 * 24 * 7)
    return response



def dimg(request):
    return render(request, 'goods/upload.html')


def upload(request):
    pic = request.FILES.get('pic')

    path = '%s/tt/%s' % (settings.MEDIA_ROOT, pic.name)

    with open(path, 'wb') as f:
        for c in pic.chunks():
            f.write(c)

    p = PicTest()
    p.pic = '%s' % pic.name
    p.save()
    return HttpResponse("上传成功")
