from django.db import models
from usercenter.models import TTSXUser
from goods.models import GoodsInfo


# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey(TTSXUser)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField(default=0)
