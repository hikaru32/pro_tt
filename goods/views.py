from django.shortcuts import render, get_object_or_404
from usercenter.models import TTSXUser
from goods.models import GoodsInfo, GoodsCategory, PicTest
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


# Create your views here.
def index(request):
    context = {'title': '天天生鲜 - 首页', 'sectop': '0',
               'user': get_object_or_404(TTSXUser, pk=request.session.get('login_id'))}
    # 每一类商品：最新 + 点击最多
    goods_list = []
    for category in GoodsCategory.objects.all():
        new_list = category.goodsinfo_set.order_by('-id')[:4]
        click_list = category.goodsinfo_set.order_by('-click')[:3]
        goods_list.append({'new_list': new_list, 'click_list': click_list, 'cat_name': category.name})
    context['goods_list'] = goods_list
    return render(request, 'goods/index.html', context=context)


def goods_list(request, cat):
    category = get_object_or_404(GoodsCategory, pk=cat)
    new_list = category.goodsinfo_set.order_by('-id')[:2]
    goods = category.goodsinfo_set.all()
    paginator = Paginator(goods, 3)
    page = paginator.page(1)
    context = {'title': '天天生鲜 - 分类', 'sectop': '0',
               'user': get_object_or_404(TTSXUser, pk=request.session.get('login_id')), 'category': category,
               'new_list': new_list, 'goods': page}
    return render(request, 'goods/list.html', context=context)


def goods_price(request):
    price_qur = get_object_or_404(GoodsCategory, pk=int(request.GET.get('cat'))).goodsinfo_set.order_by('-price')
    price_list = []
    for price in price_qur:
        mdict = model_to_dict(price, fields=['name', 'price', 'pic', 'unit'])
        mdict['pic'] = mdict['pic'].url
        price_list.append(mdict)
    return JsonResponse({'goods': price_list})


def detail(request, gid):
    context = {'title': '天天生鲜 - 分类', 'sectop': '0',
               'user': get_object_or_404(TTSXUser, pk=request.session.get('login_id'))}
    return render(request, 'goods/detail.html', context=context)


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
