from django.conf.urls import url
from goods import views

app_name = 'goods'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^goods/(?P<cat>\d+)/$', views.goods_list, name='list'),
    url(r'^goods/price/$', views.goods_price, name='price_list'),
    url(r'^goods/detail/(\d+)/$', views.detail, name='detail'),


    url(r'^dimg/$', views.dimg, name='dimg'),
    url(r'^upload/$', views.upload),
]
