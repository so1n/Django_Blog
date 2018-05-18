from datetime import datetime

from django.db import models


class Information(models.Model):
    name = models.CharField(max_length=100, verbose_name="资讯名")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    read_nums = models.IntegerField(default=0, verbose_name="阅读数")
    u_fav_nums = models.IntegerField(default=0, verbose_name="用户收藏数")
    u_read_nums = models.IntegerField(default=0, verbose_name="用户阅读数")
    url = models.CharField(max_length=200, verbose_name="url", default="")
    info_from = models.CharField(max_length=50, verbose_name="来源")
    tag = models.CharField(max_length=20, verbose_name="标签", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "资讯"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
