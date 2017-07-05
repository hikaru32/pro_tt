from django.db import models


# Create your models here.
class TTSXUser(models.Model):
    uname = models.CharField(max_length=20)  # 用户名
    upasswd = models.CharField(max_length=40)  # 密码
    uemail = models.CharField(max_length=30)  # 邮箱
    uphone = models.CharField(max_length=11, blank=True)  # 手机
    ucode = models.CharField(max_length=6, blank=True)  # 邮编
    uaddress = models.CharField(max_length=100, blank=True)  # 收件地址
    ushou = models.CharField(max_length=20, blank=True)  # 收件人姓名
