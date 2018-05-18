import re
import requests
import json
import time
from bs4 import BeautifulSoup

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_project.settings")
django.setup()

from information.models import Information


chrome_headers = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                   ' like Gecko) Chrome/64.0.3282.186 Safari/537.36'),
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
}

chrome_mobile_headers = {
    'User-Agent': ('Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.'
                  '132 Mobile Safari/537.36'),
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
}


def crawler_v2ex():
    url = 'https://www.v2ex.com/?tab=tech'
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    info_list = soup.find_all("div", {"class": "cell item"})
    for info in info_list:
        info_temp = info.find('span', {'class': 'item_title'}).a
        name = info_temp.text
        url = 'https://www.v2ex.com' + info_temp.get('href')
        info_temp = info.find('div', {'class': 'votes'})
        tag = 'v2ex'
        info_from = 'v2ex-'+info.find('a', {'class': 'node'}).text.strip()
        try:
            fav_nums = int(info_temp.text.strip())
        except ValueError:
            fav_nums = 0
        info_temp = info.find('a', {'class': 'count_livid'})
        if info_temp:
            read_nums = int(info_temp.text.strip())
        else:
            read_nums = 0
        print(name, url, fav_nums, read_nums, info_from)
        if read_nums >= 50:
            Information.objects.get_or_create(url=url,
                                              defaults={'name': name,
                                                        'tag': tag,
                                                        'info_from': info_from,
                                                        'fav_nums': fav_nums,
                                                        'read_nums': read_nums})


def crawler_kr_36():
    url = 'http://36kr.com/api/search-column/mainsite?per_page=20&page=1'
    response = requests.get(url, headers=chrome_headers)
    body_list = json.loads(response.text)['data']['items']
    for body in body_list:
        name = body['title']
        url = 'http://36kr.com/p/'+str(body['id'])+'.html'
        tag = '互联网'
        info_from = '36kr'+body['column_name']
        try:
            read_nums = body['favourite_num']
        except KeyError:
            read_nums = 0
        fav_nums = 0
        print(name, url, read_nums, info_from)
        if read_nums >= 50:
            Information.objects.get_or_create(url=url,
                                              defaults={'name': name,
                                                        'tag': tag,
                                                        'info_from': info_from,
                                                        'fav_nums': fav_nums,
                                                        'read_nums': read_nums})


def crawler_dgtle():
    url = 'http://www.dgtle.com/portal.php'
    response = requests.get(url, headers=chrome_mobile_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find('div', {'class': 'cl cr180article_list'})
    body_list = body.find_all('dl')
    for body in body_list:
        try:
            name = body.find('dt', {'class': 'zjj_title'}).text
            url = 'http://www.dgtle.com/'+body.find('dd', {'class': 'm'}).a.get('href')
            read_nums = int(body.find('span', {'class': 'cr_replies'}).text)
            fav_nums = int(body.find('span', {'class': 'cr_recommend_add'}).text)
            digital_list = ['手机', '平板', '笔电', '数码', '影音', '周边', '沙龙', '应用', '视频', '其它']
            wenqing_list = ['摄影', '旅行', '玩物', '文具', '生活']
            dgtle_tag = body.select('div[class="z"]')[0].a.text.strip()
            if dgtle_tag in digital_list:
                tag = '数码'
            elif dgtle_tag in wenqing_list:
                tag = '文青'
            info_from = '数字尾巴-'+dgtle_tag
            print(name, url, fav_nums, read_nums, info_from)
            if read_nums >= 20:
                Information.objects.get_or_create(url=url,
                                                  defaults={'name': name,
                                                            'tag': tag,
                                                            'info_from': info_from,
                                                            'fav_nums': fav_nums,
                                                            'read_nums': read_nums})
        except:
            pass


def crawler_oschina():
    url = 'https://www.oschina.net/action/ajax/get_more_news_list?newsType=&p=1'
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    info_list = soup.find_all("div", {"class": "main-info box-aw"})
    for info in info_list:
        name = info.find('span', {'class': 'text-ellipsis'}).text
        url= 'https://www.oschina.net'+info.find('a', {'class': 'title'}).get('href')
        read_nums = int(info.find_all('span', {'class': 'mr'})[1].text)
        fav_nums = 0
        tag = '技术干货'
        info_from = '开源中国'
        print(name, url, read_nums)
        if read_nums >=10 :
            Information.objects.get_or_create(url=url,
                                              defaults={'name': name,
                                                        'tag': tag,
                                                        'info_from': info_from,
                                                        'fav_nums': fav_nums,
                                                        'read_nums': read_nums})


def crawler_ssp():
    url = 'https://sspai.com/api/v1/articles?offset=0&limit=20&type=recommend_to_home&sort=recommend_to_home_at&include_total=false'
    response = requests.get(url, headers=chrome_headers)
    body_list = json.loads(response.text)['list']
    for body in body_list:
        name = body['title']
        url = 'https://sspai.com/post/' + str(body['id'])
        read_nums = body['all_comments_count']
        fav_nums = body['likes_count']
        tag = '数码'
        ssps_tag_list = body['tags']
        ssps_tag_list = [ssps_tag['title'] for ssps_tag in ssps_tag_list]
        info_from = '少数派[' + ', '.join(ssps_tag_list)+']'
        print(name, url , info_from)
        if read_nums + fav_nums >= 50:
            Information.objects.get_or_create(url=url,
                                              defaults={'name': name,
                                                        'tag': tag,
                                                        'info_from': info_from,
                                                        'fav_nums': fav_nums,
                                                        'read_nums': read_nums})