import re
import requests
import json
import time
import urllib.parse
from fuzzywuzzy import process
from bs4 import BeautifulSoup

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_project.settings")
django.setup()

from movie.models import City, CorD, Cinema, Movie, MovieTicketInfo, RMovieTicketInfo
from user.models import Tag

chrome_headers = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                   ' like Gecko) Chrome/64.0.3282.186 Safari/537.36'),
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
}

# 广州: 440100 深圳:440300


def get_qx(city_id):
    url = 'https://dianying.taobao.com/cinemaList.htm?city={}'.format(city_id)
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    qx_list = soup.find("div",{"class":"select-tags"})
    qx_list = qx_list.find_all('a')
    my_qx_list = []
    for qx in qx_list[1:]:
        my_qx_list.append(qx.text)
    return my_qx_list


def get_movie_theater(city_name, city_id):
    url = 'https://dianying.taobao.com/ajaxCinemaList.htm?page=1&regionName={}&cinemaName=&pageSize=20&pageLength=8' \
          '&sortType=0&n_s=new&city={}'.format(city_name, city_id)
    response = requests.get(url,headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    theater_list = soup.find_all("div", {"class":"middle-hd"})
    movie_theater_list = []
    for theater in theater_list:
        href = theater.find('a').get('href')
        href = urllib.parse.urlparse(href).query
        href = urllib.parse.parse_qs(href)
        cinemaid = href['cinemaId'][0]
        temp = theater.text.replace('\n', '')
        temp = temp[:temp.find('（')]
        movie_theater_list.append([temp, cinemaid])
    return movie_theater_list

def get_movie_theater_main():
    """
    获取影城信息
    广州 1,440100
    深圳 2,440300
    :return: 
    """
    qx_list = CorD.objects.filter(cord_city=2)
    for qx in qx_list[1:]:
        movie_theater_list = get_movie_theater(qx.name, 440300)
        for movie_theater in movie_theater_list:
            Cinema.objects.update_or_create(name=movie_theater[0],
                                            defaults={'cinema_cord': qx,
                                                      'Cinema_id': movie_theater[1]
                                                      }
                                            )
        time.sleep(5)

# get_movie_theater_main()
def get_movie():
    url = 'https://dianying.taobao.com/showList.htm'
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    movie_list = soup.find_all('div', {'class': 'movie-card-wrap'})
    all_movie_list = Movie.objects.filter(emotion_num=1)[:10]
    all_movie_name_list = [movie.name for movie in all_movie_list]
    for movie in movie_list:
        name = movie.find('div', {'class': 'movie-card-name'}).text.replace('\n', '')
        href = movie.a.get('href')
        href = urllib.parse.urlparse(href).query
        href = urllib.parse.parse_qs(href)
        movie_id = href['showId'][0]
        fz_name_list = process.extract(name, all_movie_name_list)
        for fz_name in fz_name_list:
            if fz_name[1] > 40:
                cinema_list = Cinema.objects.all()
                for cinema in cinema_list:
                    get_ticket(movie_id, cinema.Cinema_id)
#get_movie()

def get_ticket(show_id, cinema_id):
    url = 'https://dianying.taobao.com/showDetailSchedule.htm?showId={}&cinemaId={}&date=2018-03-31&regionName=&n_s=new'.format(show_id, cinema_id)
    response = requests.get(url, headers=chrome_headers, proxies={"https": "110.73.7.27:8123"})
    soup = BeautifulSoup(response.text, "html.parser")
    ticket_list = soup.find_all('tr')
    print(soup)
    for ticket in ticket_list:
        print(ticket)
        temp_time = ticket.find('td', {'class': 'hall-time'})
        s_time = temp_time.find('em').text
        e_time = temp_time.text
        lg = ticket.find('td', {'class': 'hall-type'})
        tn = ticket.find('td', {'class': 'hall-name'})
        temp_price = ticket.find('td', {'class': 'hall-price'})
        n_price = temp_price.find('em', {'class': 'now'})
        o_price = temp_price.find('del', {'class': 'old'})
        url = ticket.find('td', {'class': 'hall-seat'})
        url = url.a.get('href')
        MovieTicketInfo.objects.create()
        print(s_time, e_time, lg, tn, n_price, o_price, url)


def abc():
    a_list = RMovieTicketInfo.objects.filter(ticket_type=2)
    for a in a_list:
        RMovieTicketInfo.objects.create(ticket_type=4,
                                       ticket_s_time=a.ticket_s_time,
                                       ticket_e_time=a.ticket_e_time,
                                       ticket_lg=a.ticket_lg,
                                       ticket_tn=a.ticket_tn,
                                       ticket_np=40,
                                       ticket_op=60)

abc()




