import requests
import time
import re
from bs4 import BeautifulSoup
from snownlp import SnowNLP
from datetime import datetime

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_project.settings")
django.setup()

from movie.models import Movie, MovieComment


chrome_headers = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                   ' like Gecko) Chrome/64.0.3282.186 Safari/537.36'),
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
}


def dowloadPic(imageUrl,filePath):
    r = requests.get(imageUrl)
    with open(filePath, "wb") as code:
        code.write(r.content)


def movie_comment(movie_id, movie_name):
    #短评
    page = 1
    while page < 120:
        url1 = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P'\
                .format(movie_id, page)
        response1 = requests.get(url1, headers=chrome_headers)
        soup1 = BeautifulSoup(response1.text, "html.parser")
        review1_list = soup1.find_all("div", {"class": "comment-item"})
        for review1 in review1_list:
            try:
                review_author = review1.find("div", {"class": "avatar"}).find("a").get('title')
                review_time = review1.find("span", {"class": "comment-time "}).get('title')
                review = review1.find('div', {"class": "comment"}).find("p").text.strip()
                comment_like_nums = review1.find('span', {"class": "votes"}).text
                comment_degree = review1.find('span', {"class": "allstar40 rating"}).get('title')
                print(review_author, review_time, review, comment_like_nums, comment_degree)
                print('------')
                try:
                    obj = MovieComment.objects.get(comment_author=review_author)
                    obj.comment_like_nums=comment_like_nums
                    print(obj)
                    obj.save()
                except MovieComment.DoesNotExist:
                    MovieComment.objects.create(movie_name=movie_name,
                                                comment_author=review_author,
                                                doubanid=movie_id,
                                                comment=review,
                                                comment_like_nums=comment_like_nums,
                                                comment_degree=comment_degree,
                                                comment_time=review_time,
                                                comment_type=1)
            except:
                pass
        page += 20
        time.sleep(1)


def movie_detail(movie_id, movie_time):
    """
    根据电影id返回页面数据，评论另外url处理，每次递增20,跟review_page_all可以计算总页面
    详细的评论可以从一条jsURL获得，而且获得的是一个页面。。。
    """
    url = 'https://movie.douban.com/subject/{}/?from=playing_poster'.format(movie_id)
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    movie_title = soup.find("span", {"property": "v:itemreviewed"}).text
    movie_year = soup.find("span", {"class": "year"}).text
    movie_score = soup.find("strong", {"class": "ll rating_num"}).text
    movie_img = soup.find("img", {"rel": "v:image"}).get('src')
    movie_info = soup.find("div", {"id": "info"}).text.split('\n')[1:-1]
    movie_related_info = soup.find("span", {"property": "v:summary"}).text.replace('\n', '').replace(' ', '')
    print(movie_title, movie_year, movie_score,
          movie_img, movie_info, movie_related_info)
    print('------')
    Movie.objects.create(doubanid=movie_id,
                         name=movie_title,
                         movie_score=movie_score,
                         movie_image="static/image/movie/movie_image_{}".format(movie_id),
                         movie_info='|'.join(movie_info[:4]),
                         movie_info1='|'.join(movie_info[4:]),
                         movie_time=movie_time,
                         movie_detail=movie_related_info)


#广州id=118281深圳id=118282
def douban_movie_hot_list():
    """
    执行douban_movie_info()
    返回25723583 英伦对决 https://movie.douban.com/subject/25723583/?from=playing_poster
    依次为id 电影名 对应详情页
    """
    url = 'https://movie.douban.com/cinema/nowplaying/guangzhou/'
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    movie_info_list = soup.find_all("li", {"class": "list-item"})
    for movie_info in movie_info_list:
        movie_id = movie_info.get('id')
        movie_image_url = movie_info.find("img", {"rel": "nofollow"}).get('src')
        movie_name = movie_info.get('data-title')
        movie_time = movie_info.get('data-duration')
        path = "../static/image/movie/movie_image_"+movie_id
        dowloadPic(movie_image_url, path)
        print(movie_time, movie_id, movie_name)
        try:
            #movie_comment(movie_id, movie_name)
            movie_detail(movie_id, movie_time)
            time.sleep(1)
        except:
            pass


def crawler_movie_info():
    douban_movie_hot_list()

#crawler_movie_info()


def movie_emotion_num():
    """
    模型有点问题，大多数都在0.9之上更多的是1，保存结果有0,1
    :return: 
    """
    now_movie_list = []
    all_movie_list = Movie.objects.all()
    for movie in all_movie_list:
        if movie.add_time.strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'):
            movie_all_comment = MovieComment.objects.filter(doubanid=movie.doubanid)
            comment_list = [comment.comment for comment in movie_all_comment]
            if comment_list:
                s = SnowNLP("".join(comment_list))
                print(movie.name, s.sentiments)
                movie.emotion_num = s.sentiments
                movie.save()



movie_emotion_num()
