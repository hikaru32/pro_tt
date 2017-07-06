from django.conf.urls import url
from usercenter import views


app_name = 'usercenter'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^user/(?P<tt_site>info|order|addr)/$', views.user_center, name='user_center'),
    # url(r'^user(?P<tt_uid>\d+)/info/$', views.user_info, name='user_info'),
    # url(r'^user(?P<tt_uid>\d+)/order/$', views.user_order, name='user_order'),
    # url(r'^user(?P<tt_uid>\d+)/addr/$', views.user_addr, name='user_addr'),

]