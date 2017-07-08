from django.conf.urls import url
from goods import views

app_name = 'goods'
urlpatterns = [
    url(r'^$', views.index, name='index'),


    url(r'^dimg/$', views.dimg, name='dimg'),
    url(r'^upload/$', views.upload),
]
