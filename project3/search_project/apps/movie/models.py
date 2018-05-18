from datetime import datetime

from django.db import models


class City(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CorD(models.Model):
    name = models.CharField(max_length=20, verbose_name="区县名")
    cord_city = models.ForeignKey(City, verbose_name="城市外键")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "区县"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Cinema(models.Model):
    name = models.CharField(max_length=50, verbose_name="电影院名")
    cinema_cord = models.ForeignKey(CorD, verbose_name="区县外键")
    Cinema_id = models.IntegerField(default=0, verbose_name="电影院id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影院"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=50, verbose_name="电影名")
    doubanid = models.IntegerField(default=0, verbose_name="豆瓣电影id")
    movie_score = models.CharField(max_length=10, verbose_name="电影评分")
    movie_image = models.ImageField(max_length=100, upload_to="static/image/movie/%Y/%m",
                                    default="static/image/movie/default.png",
                                    verbose_name="图片")
    movie_time = models.CharField(max_length=50, default="", verbose_name="片长")
    movie_info = models.CharField(max_length=1000, verbose_name="电影详情1", default="")
    movie_info1 = models.CharField(max_length=1000, verbose_name="电影详情2", default="")
    movie_detail = models.CharField(max_length=500, verbose_name="电影内容", default="")
    emotion_num = models.FloatField(default=0, verbose_name="情感分析数值")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CinemaMovie(models.Model):
    movie_name = models.CharField(max_length=50, verbose_name="电影名")
    cinema_name = models.CharField(max_length=50, verbose_name="电影院名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影与电影院绑定"
        verbose_name_plural = verbose_name


class MovieComment(models.Model):
    comment_author = models.CharField(max_length=20, verbose_name="豆瓣用户名", default="")
    comment_time = models.CharField(max_length=100, default="", verbose_name="豆瓣评论时间")
    comment_degree = models.CharField(max_length=20, default="", verbose_name="推荐等级")
    comment_like_nums = models.IntegerField(default=0, verbose_name="有用数量")
    movie_name = models.CharField(max_length=50, verbose_name="电影名")
    doubanid = models.IntegerField(default=0, verbose_name="豆瓣电影id")
    comment = models.CharField(max_length=200, verbose_name="电影评论")
    comment_type = models.CharField(max_length=6,
                                    choices=(("1", "豆瓣"), ("2", "用户")),
                                    default="豆瓣",
                                    verbose_name="评论类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.movie_name


class MovieTicketInfo(models.Model):
    ticket_cinema = models.CharField(max_length=50, verbose_name="影院", default="")
    ticket_movie = models.CharField(max_length=50, verbose_name="电影名", default="")
    ticket_type = models.CharField(max_length=50, verbose_name="类型", default="")
    ticket_s_time = models.CharField(max_length=50, verbose_name="开始时间", default="")
    ticket_e_time = models.CharField(max_length=50, verbose_name="结束时间", default="")
    ticket_lg = models.CharField(max_length=50, verbose_name="语言", default="")
    ticket_tn = models.CharField(max_length=50, verbose_name="厅", default="")
    ticket_np = models.CharField(max_length=50, verbose_name="新价格", default="")
    ticket_op = models.CharField(max_length=50, verbose_name="旧价格", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影票信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ticket_movie


class RMovieTicketInfo(models.Model):
    ticket_type = models.CharField(max_length=50, verbose_name="类型", default="")
    ticket_s_time = models.CharField(max_length=50, verbose_name="开始时间", default="")
    ticket_e_time = models.CharField(max_length=50, verbose_name="结束时间", default="")
    ticket_lg = models.CharField(max_length=50, verbose_name="语言", default="")
    ticket_tn = models.CharField(max_length=50, verbose_name="厅", default="")
    ticket_np = models.CharField(max_length=50, verbose_name="新价格", default="")
    ticket_op = models.CharField(max_length=50, verbose_name="旧价格", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "电影票信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ticket_type

