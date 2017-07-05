from django.conf.urls import url
from usercenter import views


app_name = 'usercenter'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^user(?P<tt_uid>\d+)/info/$', views.user_info, name='user_info'),
]