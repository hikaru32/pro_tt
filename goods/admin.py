from django.contrib import admin
from goods.models import GoodsInfo, GoodsCategory, PicTest


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_deleted']


class InfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'click', 'kucun']


admin.site.register(GoodsCategory, CategoryAdmin)
admin.site.register(GoodsInfo, InfoAdmin)
admin.site.register(PicTest)
