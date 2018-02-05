from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", "男"),("female", "女")), default="男", verbose_name="性别")
    address = models.CharField(max_length=100, verbose_name="地址", null=True, blank=True)
    mobile = models.CharField(max_length=11,null=True, blank=True, verbose_name="手机号码")
    user_image =models.ImageField(max_length=100, upload_to="image/%y/%m", default="image/default.png", verbose_name="用户头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta(AbstractUser.Meta):
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"),("forget", "找回密码")), max_length=10, verbose_name="发送类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name



class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(max_length=100, upload_to="banner/%y/%m", verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name