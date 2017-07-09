from django.conf.urls import url
from goods import views

app_name = 'goods'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^goods/(?P<cat>\d+)/$', views.goods_list, name='list'),
    url(r'^goods/order/$', views.goods_order, name='order_list'),
    url(r'^goods/detail/(\d+)/$', views.detail, name='detail'),


    url(r'^dimg/$', views.dimg, name='dimg'),
    url(r'^upload/$', views.upload),
]
