from django.shortcuts import render, get_object_or_404
from usercenter.models import TTSXUser
from goods.models import GoodsInfo, GoodsCategory, PicTest
from django.conf import settings
from django.http import HttpResponse


# Create your views here.
def index(request):
    context = {'title': '天天生鲜 - 首页', 'sectop': '0', 'is_login': request.session.get('is_login', '0'),
               'user': get_object_or_404(TTSXUser, pk=request.session.get('login_id'))}
    # 每一类商品：最新 + 点击最多
    goods_list = []
    for category in GoodsCategory.objects.all():
        new_list = category.goodsinfo_set.order_by('-id')[:4]
        click_list = category.goodsinfo_set.order_by('-click')[:3]
        goods_list.append({'new_list': new_list, 'click_list': click_list, 'cat_name': category.name})
    context['goods_list'] = goods_list
    return render(request, 'goods/index.html', context=context)


def goods_list(request):
    context = {}
    return render(request, 'goods/list.html', context=context)



def dimg(request):
    return render(request, 'goods/upload.html')

def upload(request):
    pic = request.FILES.get('pic')

    path = '%s/tt/%s' %(settings.MEDIA_ROOT, pic.name)


    with open(path, 'wb') as f:
        for c in pic.chunks():
            f.write(c)

    p = PicTest()
    p.pic = '%s' %pic.name
    p.save()
    return HttpResponse("上传成功")