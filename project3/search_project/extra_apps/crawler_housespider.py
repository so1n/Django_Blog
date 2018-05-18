import re
import requests
import time
import logging
from bs4 import BeautifulSoup

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_project.settings")
django.setup()
from house.models import HouseInfo
from movie.models import City

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

def pinpaigongyu_58city(db_id, city):
    """
    数据来自58品牌公寓
    url由于是移动端提取的，所以拼接为电脑端（我网页只运行为电脑端）
    address+info_title后期拼接后，高德能找到对应的位置，准确率提高到99%
    """
    url = "http://m.58.com/{}/pinpaigongyu/pn1/?segment=true".format(city)
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text,"html.parser")
    house_info_list = soup.find_all("li",{"class":"item"})
    pattern_58city = re.compile(r'{}(.+)'.format(city))
    for house_info in house_info_list:
        house_url = house_info.find("a").get('href')
        house_url = 'http://{}.58.com'.format(city)+re.findall(pattern_58city, house_url)[0]
        info_title = house_info.find("dt", {"class": "info-title"}).text.split("|")[1].split("-")[0].split("(")[0].strip()
        address = house_info.find("em").text.strip()+info_title
        price = house_info.find("span", {"class": "info-line2-price"}).text.strip()
        price = re.findall(re.compile(r'\d+'), price)[0]
        room_info = house_info.find("dd", {"class": "room_icon"}).text.split("\n")[1:-2]
        room_info = ",".join(room_info)
        image_url = "http:" + house_info.find("img", {"class": "item-thumb"}).get('src')
        print(house_url, '|', address, '|', info_title, '|', price, '|', room_info, '|', image_url)
        print('--------')
        HouseInfo.objects.get_or_create(house_url=house_url,
                                        defaults={'house_city': City.objects.filter(id=db_id)[0],
                                                  'name': info_title,
                                                  'house_price': int(price),
                                                  'house_detail': room_info,
                                                  'house_image_url': image_url,
                                                  'house_address': address,
                                                  'house_type': 1})


def anjuke(db_id, city):
    url = 'https://{}.zu.anjuke.com/fangyuan/p1'.format(city)
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    house_info_list = soup.find_all("div", {"class": "zu-itemmod"})
    for house_info in house_info_list:
        house_url = house_info.get('link')
        address_info_title = house_info.find("address", {"class": "details-item"}).text.split("\n")
        image_url = house_info.find("img").get('src')
        info_title = address_info_title[1].strip()
        address = info_title + address_info_title[2].strip().split(" ")[1]
        price = house_info.find("strong").text
        room_info = house_info.find("p", {"class": "details-item tag"}).text.split("|")
        room_info = ",".join(room_info).strip()
        print(house_url, '|', address, '|', info_title, '|', price, '|', room_info, '|', image_url)
        print('--------')
        HouseInfo.objects.get_or_create(house_url=house_url,
                                        defaults={'house_city': City.objects.filter(id=db_id)[0],
                                                  'name': info_title,
                                                  'house_price': int(price),
                                                  'house_detail': room_info,
                                                  'house_image_url': image_url,
                                                  'house_address': address,
                                                  'house_type': 2})


def fangtianxia(db_id, city):
    url = 'http://zu.{}.fang.com/house/i31'.format(city)
    response = requests.get(url, headers=chrome_headers)
    soup = BeautifulSoup(response.text, "html.parser")
    house_info_list = soup.find_all("dl", {"class": "list hiddenMap rel"})
    for house_info in house_info_list:
        # 跳掉带有二维码的组件
        try:
            house_url = 'http://zu.{}.fang.com'.format(city)+house_info.find("a", {"target": "_blank"}).get('href')
        except:
            continue
        address = house_info.find("p", {"class": "gray6 mt20"}).text.strip()
        image_url = house_info.find("img", {"class": "b-lazy"}).get('data-src')
        info_title = address.split("-")[-1].strip()
        price = house_info.find("span", {"class": "price"}).text
        try:
            room_info = (house_info.find("span", {"class": "note colorGreen"}).
                         text+house_info.find("span", {"class": "note colorBlue"}).
                         text+house_info.find("span", {"class": "note colorRed"}).text).strip()
        except:
            room_info = '没有房间具体信息'
        print(house_url, '|', address, '|', info_title,  '|', price, '|', room_info, '|', image_url)
        print('--------')
        HouseInfo.objects.get_or_create(house_url=house_url,
                                        defaults={'house_city': City.objects.filter(id=db_id)[0],
                                                  'name': info_title,
                                                  'house_price': int(price),
                                                  'house_detail': room_info,
                                                  'house_image_url': image_url,
                                                  'house_address': address,
                                                  'house_type': 3})


def run(db_id, city):
    pinpaigongyu_58city(db_id, city)
    try:
        anjuke(db_id, city)
    except:
        logging.info('跳过')
    fangtianxia(db_id, city)


def crawler_house():
    run(1, 'gz')
    run(2, 'sz')

