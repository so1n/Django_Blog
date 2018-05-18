from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name="标签名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta(AbstractUser.Meta):
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserTag(models.Model):
    name = models.CharField(max_length=20, verbose_name="标签名")
    user = models.CharField(default="", max_length=50, verbose_name="用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta(AbstractUser.Meta):
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="男", verbose_name="性别")
    address = models.CharField(max_length=100, verbose_name="地址", null=True, blank=True)
    mobile = models.CharField(max_length=11,null=True, blank=True, verbose_name="手机号码")
    user_image = models.ImageField(max_length=100, upload_to="static/image/user/%Y/%m",
                                   default="static/image/user/default.png", verbose_name="用户头像")
    user_tag = models.ManyToManyField(Tag, verbose_name="用户标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta(AbstractUser.Meta):
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码"), ("update_email", "修改邮箱")),
                                 max_length=30, verbose_name="发送类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name


class UserFav(models.Model):
    """
    储存用户收藏
    """
    fav_id = models.CharField(max_length=50, verbose_name="收藏的id")
    user_name = models.CharField(max_length=20, verbose_name="用户名")
    type = models.CharField(max_length=6, choices=(("house", "房源"), ("movie", "电影"), ("information", "资讯")), default="房源", verbose_name="类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta(AbstractUser.Meta):
        verbose_name = "用户与收藏"
        verbose_name_plural = verbose_name


class HousePush(models.Model):
    """
    储存用户房源地址与价格的权重
    """
    house_address = models.CharField(max_length=50, verbose_name="地址")
    house_price = models.CharField(max_length=20, verbose_name="价格")
    user_name = models.CharField(max_length=20, verbose_name="用户名")

    class Meta(AbstractUser.Meta):
        verbose_name = "用户house表单"
        verbose_name_plural = verbose_name
