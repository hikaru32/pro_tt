from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class GoodsCategory(models.Model):
    name = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GoodsInfo(models.Model):
    name = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='goods')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    click = models.IntegerField()
    unit = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)
    subtitle = models.CharField(max_length=200)
    kucun = models.IntegerField(default=100)
    content = HTMLField()
    category = models.ForeignKey(GoodsCategory)



class PicTest(models.Model):
    pic = models.ImageField(upload_to='tt/')