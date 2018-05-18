from datetime import datetime

from django.db import models
from movie.models import City


class HouseInfo(models.Model):
    house_city = models.ForeignKey(City, verbose_name="城市外键")
    name = models.CharField(max_length=20, verbose_name="房名")
    house_price = models.IntegerField(default=0, verbose_name="价格")
    house_detail = models.CharField(max_length=50, default="", verbose_name="信息")
    house_image = models.ImageField(max_length=100, upload_to="static/image/house/%Y/%m",
                                    default="static/image/house/default.png",
                                    verbose_name="图片")
    house_image_url = models.CharField(max_length=200, verbose_name="图片url")
    house_url = models.CharField(max_length=200, verbose_name="url", default="")
    house_address = models.CharField(max_length=50, verbose_name="地址")
    house_type = models.CharField(max_length=6,
                                  choices=(("1", "58同城"), ("2", "anjuke"), ("3", "fangtianxia")),
                                  default="58同城",
                                  verbose_name="类型")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "房源信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





