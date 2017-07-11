from django.conf.urls import url
from cart import views


app_name = 'cart'
urlpatterns = [
    url(r'^add_cart/$', views.add_cart, name='add_cart'),
]