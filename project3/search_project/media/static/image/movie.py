import re
import requests
import json
import time
import pymysql
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
"""
这是一份很随意的代码～～～～
爬取的有淘票票，糯米，时光网
由于不是同一天写的，所以部分参数有些不同，但结果是差不多的
百度糯米电影只有手机版。。。。
由于生成的列表不长，所以没用生成器，如果列表过长，则改为生成器
如下
def get_movie_info_tpp():
	'''
	从淘票票从的正在上映获取电影的showid和电影名
	执行
	for i in get_movie_info_tpp():
	    print(i)
	返回字典{'name': '猩球崛起3：终极之战', 'id': ['179611']}
	'''
	url = 'https://dianying.taobao.com/showList.htm'
	response = requests.get(url)
	soup = BeautifulSoup(response.text,"html.parser")
	showId_href_list = soup.find_all("a",{"class":"movie-card"})
	pattern_id = re.compile(r'\d+')
	for showId_href in showId_href_list:
		movie_card_href = showId_href.get('href')
		get_showId = re.findall(pattern_id, movie_card_href)
		pattern_name = re.compile(r'.+')
		get_movie_name = re.findall(pattern_name, showId_href.text)
		movie_tpp_dict = dict(id=get_showId, name=get_movie_name[0])
		yield movie_tpp_dict
"""


"""
更改链接和列表下标获取对应的县区名或者电影院名，使用tpp的名字来进行统一标准
def get_movie_info_tpp1():
	url = 'https://dianying.taobao.com/showDetailSchedule.htm?showId=199280&cinemaId=36366&date=2017-10-10&regionName=&ts=1507645795470&n_s=new&city=440300'
	response = requests.get(url)
	soup = BeautifulSoup(response.text,"html.parser")
	movie_theater_list = soup.find_all("a",{"href":"javascript:;"})
	movie_list = []
	for movie_theater in movie_theater_list[1:12]:
		movie_list.append(movie_theater.text)
	print(movie_list)
get_movie_info_tpp1()

"""

#广州县区名
gz_xq_name_list = ['白云区', '从化区', '番禺区', '海珠区,' '花都区', '黄埔区', '荔湾区', '萝岗区', '南沙区', '天河区', '越秀区', '增城区']
#广州电影院
gz_theater_list = ['粤骏电影城广州店', '广州江高数字影院', '广州中影凤凰国际影城同和店', '横店电影城（庆丰店）', '哈艺时尚影城（白云YH城店）', '广州中影凤凰影城龙归店', '广州左岸国际影城石井店', '广州乐天影城', '广州左岸影城', '广州百老汇LUXE影城（凯德店）', '广州金逸影城百信店', '中影聚丰国际影城广州店', '广州中影峰华国际影城', '【钟港】中影JAJ24小时咖啡·影院(钟港大厦店)', '大地影院广州新市天地店', '哈艺时尚影城（同德围店）', '广州金逸影城太阳城IMAX店', '广州雅纳国际影城', 'IDC国际影城白云尚城店', '【嘉禾】中影JAJ24小时咖啡·影院（嘉汇广场店）', '广州越界思哲影城（黄石店）', '哈艺时尚影城（白云东平店）', '广州展映龙骏影城', '江高巨幕国际影城', '龙影国际影城（平沙店）', '广州保利影院同德店', '广州华影梅花园影城', '星美国际影商城广州人和店', '佳映国际影城（广州江夏店）', '广州白云万达电影城', '橙天嘉禾影城（白云店）', '百德新光影城', '从化影天下国际影城', '盛世诚丰影城从化店', '尚上国际影城', '星河影城番禺南村店', '金逸影城IMAX（光美番禺沙湾店）', '广州泛洋国际影城IMAX', '大地影院-番禺大石店', '中影南方韦邦国际影城', 'CGV星聚汇影城（广州永旺店）', '番禺中影火山湖影城', '化龙海印国际电影城', '番禺市桥文化中心', '期遇·UUE影城（广州番禺店）', '金逸影城IMAX（光美番禺大石店）', 'IDC星梦影城', '星美国际影商城广州番禺店', '广州番禺万达电影城', '烽禾影城（南村剑桥郡店）', '中影佰纳国际影城（番禺店）', '烽禾影城（钟村祈福店）', '【市桥】中影JAJ24小时影院·影吧（易发街店）', '中影星海国际影城', '金逸珠江国际影城广州大学城店', '喜洋时代影城（洛溪奥园店）', '大地影院-番禺百德店', '【大石】中影JAJ24小时咖啡.影院(科宝商城店)', '大地影院-番禺西丽店', '大地影院-番禺潮流汇店', '广东科学中心巨幕影院', '星城时代电影城', '广州金逸电影空中会所影城', '广州市第二工人文化宫', '金逸海珠城IMAX店', '广州太古仓电影库', '广州映联万和南丰汇影城', '广州万胜围万达影城', '广州海珠万达影城', '广州金逸影城达镖店', '星美国际影商城广州新都荟店', '五一影城广州四季天地店', 'SFC上影影城（广州海珠燕汇店）', '广州飞扬影城-乐峰店', '哈艺时尚影城（海珠赤岗店）\u3000', '卢米埃广州合生广场IMAX影城', '广州UME国际影城', '星美国际影商城广州花都店', '金逸影城（光美花都狮岭店）', '喜盟国际影城（花都DMAX店）', '广州花都太子电影城', '中影佰纳国际影城花都店', '佳兆业国际影城（花都狮岭店）', '横店电影城（花都店）', '喜洋时代影城（花都星光汇店）', '大地影院-沙步领好店', '广州金逸影城惠润店', '大地影院-东区商业城店', '金逸院线汇赢影城', '广州新影汇国际影院（芳村店）', '华影万晟国际影城', '广州金逸影城和业店', '广州UA西城都荟电影城', '广州金逸珠江华盛影城', '平安大戏院', '广州金逸影城西村店', '华影星美国际影城', '博亚国际影城南岸路店', '广州萝岗万达电影城', '烽禾影城（萝岗科学城店）', '中数华昇巨幕影城广州萝岗店', '横店电影城（南沙店）', '广州南沙万达电影城', '广州思哲国际影城', '广州思哲影城鱼窝头店', '哈艺时尚影城（天河科韵店）', '广州飞扬影城-高德店', '广州UA IMAX花城汇电影城', '广州飞扬影城-天河城店', '广州飞扬影城-正佳IMAX店', '中影乐佳影城', '中影佰纳（飞影）电影城天河店', '星美国际影商城广州天河店（原天影影城）', '广州百丽宫LUXE影城（天环店）', '广州百丽宫影城猎德igc店', '大地影院-广州员宫店', '大地影院-奥体高德店', '横店电影城（长兴店）', '广州金逸影城维家思店', '中影国际影城广州天河太阳新天地店', '天娱广场天河电影城', '车陂国际影城', '喜洋时代影城（东圃四季荟店）', '哈艺时尚影城（合生骏景店）', '龙影国际影城（棠下店）', '东圃摩登电影城', '中影环球国际影院（珠村店）', '中影南方WE影城', '华影青宫电影城', '广州蓓蕾剧院', '广东工人电影院', '广州电影院', '中影凡力影城', '中华广场电影城', '市一宫影院', '保利国际影城-广州中环店', '广州金逸国际影城二沙岛店', '永汉电影院', '广州星汇电影院', '广州五月花电影城', '广州增城万达电影城', '广州耀莱成龙国际影城（增城新塘店）', '中影佰纳国际影城（新塘店）', '中影佰纳（飞影）电影城凤凰城店', '增城1978影院', '广州大地影院增城挂绿店', '时代凤凰国际影院增城店']
#深圳县区名
sz_xq_name_list = ['宝安区', '大鹏新区', '福田区', '光明新区', '龙岗区', '龙华区', '龙华新区', '罗湖区', '南山区', '坪山新区', '盐田区']
#深圳电影院
sz_theater_list = ['中影星美明星国际影城','中影ul城市影院万荟城店（巨幕）', '中影德金影城西乡店', '深圳百线影城', '深圳东影南国国际影城（唐美店）', 'CMC文创影城（金海华府荟悦城店）', '百誉影城上域店', '百誉影城公明店', '深圳星晨国际影城（松岗店）', '深圳金逸国际影城沙井店', '深圳宝影影城', '深影华纳影城（翻身店）', '中影国际影城深圳宝安港隆城店', '非凡数字影城', '大地影院深圳观澜店', '大地影院深圳宝安宏发大世界', '深圳中影星悦影城', '美视国际影城（4K 沉浸音）', '中影ul城市影院宝安店', '中影W影城（宝安店）', '环球国际影城（福永店）', '中影ul城市影院乐尚店', '凤凰国际影城西乡店', '深圳光明正佳影院', '环星电影院（新安店）', '中影金影星汇影城', '深圳金逸国际影城观澜店', '百盛国际影城', '中影国际影城深圳龙华九方店', '深圳金逸国际影城嘉域店', '德信影城深圳沙井联诚店', '百川国际影城（民治优城店）', '中影影派影城（长圳店）', '星美国际影商城深圳福永店', 'CGV星聚汇影城（深圳壹方城店）', '集鸿发中影国际影城（后亭店）', '深圳金逸国际影城建安店', '深圳东海国际影城', '百川影城IMAX新沙天虹店', '中影星趴影城（宝安万科生活广场店）', '大地影院深圳沙井裕客隆', '深圳金逸国际影城龙华店', '米高梅巨幕影城（田寮店）', '深圳横店电影城', '益田国际影城（福永店）', '宝影国际影城（公明店）', '新华银兴国际影城（深圳店）', '传奇影城（后瑞店）', '深圳嘉熙业国际影城', '影尊国际影城', '中影星河电影城松岗店', '深圳嘉乐影城固戍店', '橙天嘉禾影城（中洲店）', '中影德金影城和平店', '云幕国际影院', '中影ul城市影院福永店', '华夏星光国际影城沙井店', '深圳金逸国际影城民治店', '中影DY影城（沙井店）', '大地影院深圳宝安时代城', '完美世界影城沙井店（原17.5影城）', '中影ul城市影院黄田店', '集鸿发中影国际影城（田寮店）', '万厅国际影城公明店', '深圳中影星美国际影城', '深圳幕森影城福永店', '中影德金影城福永店', '大地影院深圳佐阾香颂影城', '中影100都市影城彩虹城店', '中影飞尚百誉国际影城', '万厅国际影城石岩店', '深圳金逸国际影城碧海城店', '深圳万达电影城海雅店', '太平洋影城（深圳同泰时代广场店）', '深圳易时代影城', '中影UL城市影院宝立方店', '时代凤凰国际影城（松岗店）', '卡思国际影城', '万众国际影城（NEO店）', '深圳金逸国际影城中心城店', '保利国际影城-深圳大中华店', '纵横国际影城（石厦店）', '百汇国际影城（红岭店）', '深圳博纳国际影城皇庭店', '中影ul城市影院彩田店', '深影国际影城佐阾虹湾店', '中影万国国际影城（益田村店）', '星美国际影商城深圳福体店', '卢米埃深圳华强北九方IMAX影城', '深圳百老汇影城cocopark店', '深圳盛唐时代国际影城（皇岗店）', '深圳星联影城（园岭店）', '中影国际影城福田中信广场店（新南国店）', '深影国际嘉之华中心影城', '中影世纪星晖影城', '橙天嘉禾影城（卓悦汇店）', '星美国际影商城深圳京基IMAX店', '中影国际影城深圳深国投店', '太平洋影城（深圳东海店）', '期遇·UUE巨幕影城（公明店）', '中影南方国际影城万汇城店', '米高梅国际影城（横岗店）', '深圳聚星国际影城（华南第一巨幕店）', '深圳百汇银河影城', '百汇国际影城（南岭店）', '深圳星烨南岭国际影城', '深圳万达坂田雅园店', '深圳中影易禾影城', '深圳金域世纪电影城', '深圳君胜国际影城同乐店', '中影JAJ24小时咖啡影院（平湖店）', '天誉国际影城（樟树布店）', '深圳博纳国际影城龙岗店', '深影五洲国际影城', '深圳达梦国际影城', '万众国际影城（横岗店）', 'ZCV布吉影城', '百誉影城龙岗店', '逸达国际影城（荷坳店）', '汉鼎宇佑影城（华夏Le店）', '万达影城龙盛新天地店', '中影Face电影城（平湖店）', '华夏君盛影城平湖店', '深圳中影百纳国际影城', '深圳时代金球影城', '纵横国际影城ZMAX巨幕（天安云谷店）', '佳兆业国际影城布吉店', '橙天嘉禾影城（摩尔城店）', '太平洋影城（深圳新城汇店）', '中影ul城市影院坪地店', '深圳华夏君盛影城坪地店', '深圳宝能影城（龙岗店）', '深圳嘉年华国际影城', '博亚影城五和店', '麦希中影南方布吉店', '万明影城坪山店', '德信影城深圳世纪广场店（原盛达国际影城）', '南国艺恒国际影城坂田店', '中影百川影城（布吉店）', '万达影城布吉万科红店', '中影泰得影城龙岗店', '深圳一帆影城', '星美国际影商城深圳龙岗店', '中影星河影城大浪店', '华纳万都影院龙华店', '橙天嘉禾影城（观澜湖店）', '华夏国际影城观澜店', '中影W影城（龙华店）', '中影熙腾影院（观澜店）', '深圳新耀客国际影城', '中影德金影城龙华店', '深圳金逸新新影城', '中影南方激光影城', '深影华纳影城(民乐店)', '百誉影城大浪店', '深圳万达影城汇海广场店', '万成国际影城', '深圳时空国际影城（观澜章阁店）', '中影南方影城观澜店', '中影熙腾影城（龙华店）', '希恩国际影城（观澜巨幕店）', '华夏太古国际影城（龙华金銮店）', '橙天欢乐影城（大浪店）', '华夏星越·杜比全景声·民治店', '博亚影城民治店', '中影4K国际影城民治店', '深圳中影雅图城市影院龙华店', '太平洋影城（深圳八号仓店）', '嘉乐国际影城（鸿翔店）', '深圳戏院影城', '百誉影城东门店', '百誉影城钻石店', '中影ul城市影院布心店', '中影ul城市影院莲塘店', '太阳数码影城', '南国影城金光华店', '深影国际凤凰影城', '百誉影城草埔店', '深圳红石影城(东门店)', '深圳UA影城', '深圳MCL洲立影城（喜荟城中心）', '橙天嘉禾影城（深圳万象城店）', '华影信和影城', '中影UL城市影院西丽店', '卢米埃深圳汇港IMAX影城', '百汇国际影城（南山亿利达店）', '纵横国际影城深圳湾店', '华夏君盛影城', '百川国际影城（南山欢乐颂店）', '中影ul城市影院前海店', '中影ul城市影院龙珠店', '中影德金影城南山店', '中影国际影城深圳益田假日广场店', '中影星趴影城海上世界店', '中影国际影城深圳南山欢乐海岸店', '汉鼎宇佑影城（星海名城店）', '深圳海岸影城', '深圳蛇口影剧院', '深圳华夏星光国际影城', '麦希中影南方深大店', '华纳万都影城（深圳前海店）', '华谊兄弟影院深圳太古城店', '深圳MCL洲立影城（花园城中心）', '中影ul城市影院海雅店', '保利国际影城-深圳南山店', '深圳中影荟星激光影城（西丽店）', '中影4KMAX国际影城（西丽店）', '深圳百丽宫影城（南山来福士广场店）', '太平洋影城（深圳天利名城店）', '太平洋影城（深圳京基百纳店）', '华夏艺术中心数码影院', '深圳泛海影城', '深圳星际银河影城坪山店', '中影ul城市影院坪山店', '橙天国际影城（嘉邻中心店）', '深圳星际银河影城坑梓店', '冷杉欢腾影城', '深圳时代凤凰影城（盐田店）']

#图片下载
def dowloadPic(imageUrl,filePath):
    r = requests.get(imageUrl)
    with open(filePath, "wb") as code:
        code.write(r.content)

#淘票票票价
"""
get_movie_info_tpp()函数直接执行可以返回电影名字和电影的id
get_movie_theater_tpp()函数需要自己附带城市id，之后返回该城市的影院列表
get_movie_tpp(）函数返回对应条件的排片信息。需要的信息多，返回信息精确
"""
def get_movie_info_tpp():
	'''
	从淘票票从的正在上映获取电影的showid和电影名
	执行print(get_movie_info_tpp())
	返回字典{'name': '猩球崛起3：终极之战', 'id': ['179611']}
	'''
	url = 'https://dianying.taobao.com/showList.htm'
	response = requests.get(url)
	soup = BeautifulSoup(response.text,"html.parser")
	showId_href_list = soup.find_all("a",{"class":"movie-card"})
	pattern_id = re.compile(r'\d+')
	movie_tpp_list = []
	for showId_href in showId_href_list:
		movie_card_href = showId_href.get('href')
		get_showId = re.findall(pattern_id, movie_card_href)
		pattern_name = re.compile(r'.+')
		get_movie_name = re.findall(pattern_name, showId_href.text)
		movie_tpp_dict = dict(id=get_showId, name=get_movie_name[0])
		movie_tpp_list.append(movie_tpp_dict)
	return movie_tpp_list
#print(get_movie_info_tpp())

def get_movie_theater_tpp(movieId,movie_theater_ionName):
	'''
	从淘票票上面获取影城的信息
	链接的city正确后输入区才有效，city=440100为广州，city=440300为深圳
	执行
	print(get_movie_theater_tpp('179611','天河区'))
	可以查看返回信息，其中movieId为电影的id，movie_theater为区
	返回列表，列表里面是字典
	{'movie_theater_name': '哈艺时尚影城（天河科韵店）', 'movie_theater_cinemaId': ['28932'], 'movie_theater_ionName': ['天河区']}
	'''
	url = 'https://dianying.taobao.com/showDetailSchedule.htm?showId='+movieId+'&regionName='+movie_theater_ionName+'&city=440100'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	movie_theater_list = soup.find_all("a",{"href":"javascript:;"})
	movie_theater_info_list = []
	for movie_theater in movie_theater_list[13:33]:
		movie_theater_name = movie_theater.text
		#上面是获取影城名字，下面分别是获取影城id和所在的区
		movie_theater_info = movie_theater.get('data-param')
		pattern_cinemaId = re.compile(r'cinemaId=(\d+)')
		movie_theater_cinemaId = re.findall(pattern_cinemaId, movie_theater_info)
		pattern_ionName = re.compile(r'ionName=(\w+)')
		movie_theater_ionName = re.findall(pattern_ionName, movie_theater_info)
		movie_theater_dict = dict(movie_theater_name=movie_theater_name, movie_theater_ionName=movie_theater_ionName, movie_theater_Id=movie_theater_cinemaId)
		movie_theater_info_list.append(movie_theater_dict)
	return movie_theater_info_list
#print(get_movie_theater_tpp('179611','天河区'))


def get_movie_tpp(showId, time, movie_theater_ionName, movie_theater_cinemaId):
	'''
	从淘票票获取票信息和购买链接
	执行
	print(get_movie_tpp('179611', '2017-09-27', '天河区', '28932'))
	分别是电影id，时间，影城所在的区/县，影城id
	返回一个列表，列表里是字典，字典里面里面包含的信息是该影院对某电影在某天的排片信息
	{'movie_end_time': '预计17:46散场', 'movie_new_price': '39.00', 'movie_name': '5号厅', 'movie_old_price': '70.00', 'movie_start_time': '15:50', 'movie_id': 1, 'mpvie_buy_url': 'https://dianying.taobao.com/seatOrder.htm?scheduleId=449782642&n_s=new', 'movie_for': '淘票票', 'movie_type': '英语 3D'}
	'''
	url = 'https://dianying.taobao.com/showDetailSchedule.htm?showId='+showId+'&date='+time+'&n_s=new&regionName='+movie_theater_ionName+'&cinemaId='+movie_theater_cinemaId+'&ts=1505383125470'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	movie_theater_time_list = soup.find_all("td",{"class":"hall-time"})
	movie_theater_type_list = soup.find_all("td",{"class":"hall-type"})
	movie_theater_flow_list = soup.find_all("td",{"class":"hall-flow"})
	movie_theater_price_list = soup.find_all("td",{"class":"hall-price"})
	movie_theater_name_list = soup.find_all("td",{"class":"hall-name"})
	movie_theater_movie_buy_url_list = soup.find_all("a",{"class":"seat-btn"})
	tpp_movie_info_list = []
	for i in range(len(movie_theater_time_list)):
		tpp_movie_id = i+1
		tpp_movie_time_list = list(movie_theater_time_list[i].text.split(" "))
		tpp_movie_flow = list(movie_theater_flow_list[i].text.split(" "))[1]
		tpp_movie_price = list(movie_theater_price_list[i].text.strip().split("\n"))
		tpp_movie_start_time = tpp_movie_time_list[0].strip()
		tpp_movie_end_time = tpp_movie_time_list[1].strip()
		tpp_movie_type = movie_theater_type_list[i].text.strip()
		tpp_movie_name = movie_theater_name_list[i].text.strip()
		tpp_movie_new_price = tpp_movie_price[0]
		tpp_movie_old_price = tpp_movie_price[1]
		tpp_mpvie_buy_url = movie_theater_movie_buy_url_list[i].get('href')
		tpp_movie_info_dict = dict(movie_id=tpp_movie_id,
			                       movie_start_time=tpp_movie_start_time,
			                       movie_end_time=tpp_movie_end_time,
			                       movie_name=tpp_movie_name,
			                       movie_type=tpp_movie_type,
			                       movie_new_price=tpp_movie_new_price,
			                       movie_old_price=tpp_movie_old_price,
			                       mpvie_buy_url=tpp_mpvie_buy_url,
			                       movie_for="淘票票")
		tpp_movie_info_list.append(tpp_movie_info_dict)
	return tpp_movie_info_list
#print(get_movie_tpp('199280', '2017-10-11', '天河区', '28932'))
#时光网票价
"""
get_movie_info_time()函数需要城市id并返回电影id。信息
get_movie_theater_time()是直接提取的json文件，直接得到电影院的信息
get_movie_time()返回的是该影院对电影的排片，精确度略低，但量多
"""
def get_movie_theater_time():
	'''
	获取影城信息，链接为选取影城时提取的，直接copyjson数据,进行数据清理
	就是很烦他不是直接返回json要自己处理，还好影城数量不会经常变动
	广州代码为365，深圳为366
	返回的结果为：
	{'name': '广州星汇电影城', 'stringId': 'China_Guangdong_Province_Guangzhou_Yuexiu', 'cinemaId': 4135, 'districtId': 1407}
	依次为影城名，所在行政区，电影院id，区，县id 
	'''
	url = 'http://service.theater.mtime.com/Cinema.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Cinema.Services&Ajax_CallBackMethod=GetOnlineTheatersInCity&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Ftheater.mtime.com%2FChina_Guangdong_Province_Guangzhou%2F&t=2017915025266609&Ajax_CallBackArgument0=365&Ajax_CallBackArgument1=true'
	#返回区县名
	url_json = '''
	{ "value":{"districts":[{"districtId":1401,"name":"番禺区"},{"districtId":1403,"name":"海珠区"},{"districtId":1404,"name":"花都区"},{"districtId":1405,"name":"荔湾区"},{"districtId":1406,"name":"天河区"},{"districtId":1407,"name":"越秀区"},{"districtId":3388,"name":"白云区"},{"districtId":3389,"name":"黄埔区"},{"districtId":3390,"name":"南沙区"},{"districtId":3391,"name":"萝岗区"},{"districtId":3392,"name":"增城区"},{"districtId":3393,"name":"从化区"},{"districtId":4778,"name":"新塘镇区"}],"favCinemas":[],"cinemas":[{"cinemaId":4135,"name":"广州星汇电影城","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":4327,"name":"飞扬影城（乐峰店）","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":3594,"name":"中影国际影城广州天河太阳新天地店","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":1097,"name":"广东五月花电影城","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":3102,"name":"广州华影万晟国际影城","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":8590,"name":"CGV星聚汇影城广州永旺店","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":2470,"name":"SFC上影影城（广州海珠燕汇店）","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":4552,"name":"广州 IDC国际影城（番禺店）","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":4733,"name":"金逸影城IMAX（光美番禺大石店）","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":2492,"name":"广州太古仓电影库","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":3222,"name":"广州华影梅花园影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":4712,"name":"金逸影城IMAX（光美番禺沙湾店）","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":9555,"name":"哈艺时尚影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":2430,"name":"华影星美国际影城","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":4405,"name":"哈艺时尚影城-海珠赤岗店","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":9546,"name":"江高巨幕国际影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":4567,"name":"金逸影城（光美花都狮岭店）","districtId":1404,"stringId":"China_Guangdong_Province_Guangzhou_Huadu"},{"cinemaId":7125,"name":"哈艺时尚影城-白云YH城店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":9746,"name":"广东工人电影院","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":8973,"name":"中影南方WE影城","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":5678,"name":"中影凤凰影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":5766,"name":"广州泛洋国际影城","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":3251,"name":"保利国际影城广州中环店","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":7523,"name":"五一影城广州四季天地店","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":4370,"name":"星美国际影城广州南沙店","districtId":3390,"stringId":"China_Guangdong_Province_Guangzhou_NaShaQu"},{"cinemaId":3216,"name":"中影佰纳（飞影）电影城天河店","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":2869,"name":"橙天嘉禾影城广州白云店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":2347,"name":"金逸广州太阳城店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":6457,"name":"映联万和广州南丰汇影城","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":1099,"name":"华影青宫电影城","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":2523,"name":"广州耀莱成龙国际影城（增城新塘店）","districtId":4778,"stringId":"China_Guangdong_Province_Guangzhou_xintangzhenqu"},{"cinemaId":1096,"name":"广州飞扬影城-正佳IMAX店","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":3280,"name":"广州UA IMAX花城汇电影城","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":1094,"name":"中华广场电影城","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":2642,"name":"广州白云万达广场店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":1073,"name":"飞扬国际影城天河城店","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":1098,"name":"广州UME国际影城","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":8324,"name":"金逸影城（广州海珠城IMAX店）","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":3727,"name":"广州UA西城都荟电影城","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":6216,"name":"中影佰纳国际影城花都店","districtId":1404,"stringId":"China_Guangdong_Province_Guangzhou_Huadu"},{"cinemaId":1071,"name":"市一宫影城","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":1424,"name":"大地数字影院-广州员宫影院","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":2884,"name":"星美国际影城广州花都店","districtId":1404,"stringId":"China_Guangdong_Province_Guangzhou_Huadu"},{"cinemaId":3264,"name":"中影乐佳影城","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":1095,"name":"金逸广州维家思店","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":3285,"name":"金逸影城（广州达镖店）","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":3120,"name":"横店电影城（广州店）","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":7167,"name":"广州萝岗万达影院","districtId":3391,"stringId":"China_Guangdong_Province_Guangzhou_LuoGangQu"},{"cinemaId":6391,"name":"广州番禺万达广场店","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":9081,"name":"广州百丽宫影城猎德igc店","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":1372,"name":"喜洋时代（东圃四季荟店）","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":4099,"name":"金逸电影空中会所影城","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":2476,"name":"金逸广州黄埔惠润店","districtId":3389,"stringId":"China_Guangdong_Province_Guangzhou_HuangBuQu"},{"cinemaId":6987,"name":"广州高德飞扬影城","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":4457,"name":"广州思哲国际影城","districtId":3390,"stringId":"China_Guangdong_Province_Guangzhou_NaShaQu"},{"cinemaId":2273,"name":"金逸广州百信店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":7039,"name":"中影峰华国际影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":2880,"name":"金逸广州芳村森多利店","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":3601,"name":"大地数字影院-广州人和店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":5818,"name":"广州增城万达广场店","districtId":3392,"stringId":"China_Guangdong_Province_Guangzhou_ZengChengShi"},{"cinemaId":3711,"name":"星美国际影城广州新都荟店","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":8085,"name":"广州南沙万达影城","districtId":3390,"stringId":"China_Guangdong_Province_Guangzhou_NaShaQu"},{"cinemaId":2690,"name":"金逸广州和业店","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":9082,"name":"广州百丽宫影城天环店","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":8308,"name":"横店电影城（广州花都店）","districtId":1404,"stringId":"China_Guangdong_Province_Guangzhou_Huadu"},{"cinemaId":2300,"name":"大地数字影院-广州番禺大石城","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":9372,"name":"广州万达万胜围店","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":2722,"name":"大地数字影院-东圃奥体高德","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":2113,"name":"番禺市桥文化中心","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":4217,"name":"广州金逸西村影城","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":8232,"name":"中影凤凰影城同和店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":9476,"name":"广州百老汇影城凯德店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":4824,"name":"大地数字影院--广州增城东汇城","districtId":3392,"stringId":"China_Guangdong_Province_Guangzhou_ZengChengShi"},{"cinemaId":2506,"name":"广州江高数字影院","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":4844,"name":"大地数字影院--广州沙步领好广场","districtId":3389,"stringId":"China_Guangdong_Province_Guangzhou_HuangBuQu"},{"cinemaId":6104,"name":"横店电影城（广州南沙店）","districtId":3390,"stringId":"China_Guangdong_Province_Guangzhou_NaShaQu"},{"cinemaId":4575,"name":"广州展映龙骏影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":8920,"name":"龙影国际影城（棠下店）","districtId":1406,"stringId":"China_Guangdong_Province_Guangzhou_Tianhe"},{"cinemaId":6004,"name":"横店电影城(广州庆丰店)","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":3919,"name":"广州金逸国际影城二沙岛店","districtId":1407,"stringId":"China_Guangdong_Province_Guangzhou_Yuexiu"},{"cinemaId":3323,"name":"番禺中影火山湖影城","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":1953,"name":"大地影院-增城挂绿广场影院","districtId":3392,"stringId":"China_Guangdong_Province_Guangzhou_ZengChengShi"},{"cinemaId":4842,"name":"大地数字影院--广州黄埔东区商业城","districtId":3389,"stringId":"China_Guangdong_Province_Guangzhou_HuangBuQu"},{"cinemaId":7611,"name":"中影JAJ24小时咖啡·影院（易发街店）","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":3910,"name":"番禺星美国际影城","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":9670,"name":"广州市盛世诚丰影城从化店","districtId":3393,"stringId":"China_Guangdong_Province_Guangzhou_CongHuaShi"},{"cinemaId":7317,"name":"大地影院--广州白云新市天地店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":9429,"name":"佳兆业国际影城（花都狮岭店）","districtId":1404,"stringId":"China_Guangdong_Province_Guangzhou_Huadu"},{"cinemaId":10040,"name":"广州佳映国际影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":1102,"name":"平安大戏院","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":8992,"name":"万达影城（海珠店）","districtId":1403,"stringId":"China_Guangdong_Province_Guangzhou_Haizhu"},{"cinemaId":10039,"name":"喜盟国际影城花都MDAX店","districtId":1404,"stringId":"China_Guangdong_Province_Guangzhou_Huadu"},{"cinemaId":5711,"name":"大地数字影院-番禺西丽广场店","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":2937,"name":"番禺沙湾数字电影院","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":4711,"name":"金逸院线汇赢影城","districtId":3391,"stringId":"China_Guangdong_Province_Guangzhou_LuoGangQu"},{"cinemaId":8879,"name":"中影JAJ24小时咖啡影院（科宝商城店）","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":4404,"name":"金逸珠江华盛影城","districtId":1405,"stringId":"China_Guangdong_Province_Guangzhou_Liwan"},{"cinemaId":7112,"name":"星梦影城白云店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":7340,"name":"星美国际影城广州钟村店","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":9195,"name":"粤骏电影城","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":9109,"name":"龙影国际影城平沙店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":7069,"name":"星美国际影城广州人和店","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":9368,"name":"广州1978影城","districtId":3392,"stringId":"China_Guangdong_Province_Guangzhou_ZengChengShi"},{"cinemaId":5710,"name":"大地数字影院-番禺潮流汇店","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":8898,"name":"广东越界思哲影城（黄石店）","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"},{"cinemaId":4849,"name":"大地数字影院--番禺百德商业中心","districtId":1401,"stringId":"China_Guangdong_Province_Guangzhou_Panyu"},{"cinemaId":8740,"name":"中影JAJ24小时咖啡•影院（嘉汇广场店）","districtId":3388,"stringId":"China_Guangdong_Province_Guangzhou_BaiYunQu"}],"lowestPrice":23},"error":null}
	'''
	url_json1 = """{ "value":{"districts":[{"districtId":1433,"name":"宝安区"},{"districtId":1434,"name":"福田区"},{"districtId":1435,"name":"龙岗区"},{"districtId":1436,"name":"罗湖区"},{"districtId":1437,"name":"南山区"},{"districtId":3403,"name":"盐田区"},{"districtId":4990,"name":"龙华区"},{"districtId":5024,"name":"光明新区"}],"favCinemas":[],"cinemas":[{"cinemaId":1297,"name":"深圳百老汇影城cocopark店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":4663,"name":"深圳博纳国际影城（皇庭店）","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":2202,"name":"太平洋影城（深圳京基百纳店）","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":3843,"name":"汉鼎宇佑影城（星海名城店）","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":6257,"name":"深圳博纳国际影城（龙华店）","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":4072,"name":"深圳万众国际影城（NEO店）","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":3774,"name":"深圳博纳国际影城（龙岗店）","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":5778,"name":"百川国际影城","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":1485,"name":"中影国际影城深圳宝安港隆城店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":4250,"name":"ZCV布吉影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":5878,"name":"华夏君盛影城","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":4749,"name":"德信影城深圳世纪广场店（原盛达国际影城）","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":8519,"name":"深圳嘉乐国际影城（鸿翔店）","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":9674,"name":"华夏星越影城","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":3115,"name":"深圳戏院影城","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":4770,"name":"中影DY影城（沙井店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":2472,"name":"深圳博纳国际影城（华强店）","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":5919,"name":"华纳万都影城（深圳龙华店）","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":9200,"name":"中影德金影城南山店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":9882,"name":"太平洋影城（深圳同泰时代广场店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":6324,"name":"太平洋影城（深圳8号仓店）","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":1314,"name":"太平洋影城（深圳东海店）","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":3291,"name":"深圳太平洋影城（天利名城店）","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":1287,"name":"南国影城金光华店","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":3613,"name":"深圳华夏星光国际影城","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":3572,"name":"深圳万达海雅广场店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":4416,"name":"保利国际影城深圳大中华店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":8273,"name":"卢米埃影城深圳华强北九方IMAX","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":3100,"name":"中影国际影城深圳南山欢乐海岸店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":1285,"name":"深圳橙天嘉禾影城","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":3201,"name":"金逸深圳碧海店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3821,"name":"深圳万达影城布吉万科红店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":6319,"name":"百汇国际影城（南岭店）","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":2702,"name":"华夏太古国际影城（金銮时代店）","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":4773,"name":"华影信和影城","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":2700,"name":"金逸深圳建安店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3747,"name":"深圳一帆影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":2352,"name":"环星电影城（新安店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":8976,"name":"米高梅巨幕影城（田寮店）","districtId":5024,"stringId":"China_Guangdong_Province_Shenzen_guangmingxinqu"},{"cinemaId":1900,"name":"保利国际影城深圳南山店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":2655,"name":"深圳UA影院","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":1790,"name":"金逸深圳中心城店 ","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":2167,"name":"中影国际影城深圳益田假日广场店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":1213,"name":"深圳MCL洲立影城（花园城中心）","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":2627,"name":"横店电影城（深圳店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":2049,"name":"深圳海岸影城","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":5950,"name":"中影国际影城深圳龙华九方店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":2701,"name":"深影国际嘉之华中心影城","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":3578,"name":"华谊兄弟深圳影院","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":5881,"name":"星美国际影城龙岗万科广场店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":2907,"name":"深圳MCL洲立影城（喜荟城中心）","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":8941,"name":"橙天嘉禾影城深圳卓悦汇店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":2337,"name":"大地数字影院-深圳宝安宏发大世界","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3458,"name":"中影UL城市影院（福永店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":5706,"name":"中影UL城市影院（坪山店）","districtId":0,"stringId":"China_Guangdong_Province_Shenzen"},{"cinemaId":3883,"name":"中影UL城市影院（宝安店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":6669,"name":"中影UL城市影院龙珠店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":4514,"name":"中影飞尚百誉国际影城（S）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":6563,"name":"深圳万达影城汇海广场店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":6771,"name":"深圳纵横国际影城石厦店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":8280,"name":"深圳纵横国际影城天安云谷店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":2988,"name":"深圳完美世界影城沙井店（原17.5影城）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":8638,"name":"星美国际影商城京基IMAX店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":6106,"name":"中影UL城市影院莲塘店","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":6667,"name":"中影UL城市影院彩田店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":3403,"name":"深圳时代金球影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":6307,"name":"中影UL城市影院前海店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":8241,"name":"橙天嘉禾影城深圳观澜湖店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":3867,"name":"太平洋影城（深圳新城汇店）","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":6489,"name":"深圳时空国际影城（观澜章阁店）","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":4830,"name":"百汇国际影城（红岭店）","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":1286,"name":"中影国际影城深圳福田中信广场店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":4185,"name":"深圳聚星国际影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":3748,"name":"华夏嘉熙业国际影城","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":7286,"name":"华夏君盛影城平湖店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":6681,"name":"深圳东影南国国际影城（唐美店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3099,"name":"深圳中影雅图城市影院龙华店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":9881,"name":"深影国际影城佐阾虹湾店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":1271,"name":"南国艺恒国际影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":6951,"name":"深圳万众国际影城横岗店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":9807,"name":"中影南方国际影院（万汇城店）","districtId":5024,"stringId":"China_Guangdong_Province_Shenzen_guangmingxinqu"},{"cinemaId":8572,"name":"麦希中影南方深大店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":7019,"name":"中影UL城市影院布心店","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":7307,"name":"冷杉欢腾影城（深圳店）","districtId":3403,"stringId":"China_Guangdong_Province_Shenzen_YanTianQu"},{"cinemaId":5691,"name":"中影UL城市影院乐尚店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3420,"name":"金逸深圳龙华东环店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":3826,"name":"大地数字影院-深圳观澜店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":1291,"name":"太阳数码影城","districtId":1436,"stringId":"China_Guangdong_Province_Shenzen_Luohu"},{"cinemaId":7206,"name":"麦希中影南方布吉店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":4380,"name":"深圳嘉乐影城（固戍店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3421,"name":"深圳金逸电影城民治店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":2540,"name":"深圳雅图数字影院（梅林店）","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":7022,"name":"星美国际影城深圳布吉三联店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":7040,"name":"云幕国际影城","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":6149,"name":"深圳中影易禾影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":3561,"name":"新华银兴国际影城（深圳店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3156,"name":"金逸深圳观澜店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":6694,"name":"德信影城深圳沙井联诚店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":9173,"name":"中影星联影城（园岭店）","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":5108,"name":"深圳中影100都市影城彩虹城店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":4199,"name":"大地数字影院--深圳佐阾香颂影城","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":7474,"name":"华夏星光影城（宝安店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":8197,"name":"中影UL城市影院（黄田店）","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3806,"name":"深圳观澜星美国际影城","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":9302,"name":"百汇国际影城（南山店）","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":8676,"name":"深圳中影百川影城（布吉店）","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":3682,"name":"金逸深圳沙井店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":8933,"name":"橙天嘉禾影城深圳中洲店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":9007,"name":"中影熙腾国际影城龙华店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":6368,"name":"中影UL城市影院坪地店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":9404,"name":"深圳传奇影城后瑞店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":5904,"name":"橙天嘉禾影城深圳摩尔城店","districtId":0,"stringId":"China_Guangdong_Province_Shenzen"},{"cinemaId":9553,"name":"中影星趴影院海上世界店","districtId":1437,"stringId":"China_Guangdong_Province_Shenzen_Nanshan"},{"cinemaId":9705,"name":"中影UUE巨幕影城","districtId":5024,"stringId":"China_Guangdong_Province_Shenzen_guangmingxinqu"},{"cinemaId":8822,"name":"百川国际影城龙华店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":6134,"name":"星美国际影城福永店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":3188,"name":"大地数字影院-深圳沙井裕客隆","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":8436,"name":"星美国际影商城福体店","districtId":1434,"stringId":"China_Guangdong_Province_Shenzen_Futian"},{"cinemaId":9774,"name":"影尊国际影城","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":6587,"name":"星美国际影城深圳布吉昌宏店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":6502,"name":"深圳百汇银河影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":7263,"name":"深圳万达影城龙盛新天地店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":9376,"name":"环球国际影城福永店","districtId":1433,"stringId":"China_Guangdong_Province_Shenzen_Baoan"},{"cinemaId":9513,"name":"华夏君盛影城坪地店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":9694,"name":"深圳金逸影城（公明嘉域店）","districtId":5024,"stringId":"China_Guangdong_Province_Shenzen_guangmingxinqu"},{"cinemaId":6370,"name":"星美国际影城深圳君盛店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":9135,"name":"深圳市天誉影城","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"},{"cinemaId":8678,"name":"万成国际影城","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":7343,"name":"中影南方影城观澜店","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":9086,"name":"深圳市新耀客国际影城","districtId":4990,"stringId":"China_Guangdong_Province_Shenzen_Longhuaqu"},{"cinemaId":10081,"name":"深圳万达影城坂田店","districtId":1435,"stringId":"China_Guangdong_Province_Shenzen_Longgang"}],"lowestPrice":23},"error":null}
"""
	movie_theater_list = json.loads(url_json)['value']['cinemas']
	movie_theater_ionName_list = json.loads(url_json)['value']['districts']
	for movie_theater in movie_theater_ionName_list:
		movie_theater_id = movie_theater['districtId']
		movie_theater_ionName = movie_theater['name']
		print(movie_theater_id, movie_theater_ionName)
	#返回电影院名
	for movie_theater in movie_theater_list:
		print(movie_theater)

#get_movie_theater_time()

def get_movie_time(stringId,cinemaID):
	'''
	获取电影售票的信息
	执行get_movie_time('China_Guangdong_Province_Guangzhou_Yuexiu','4135')获取到该影院最近的排片信息
	返回2017-09-30 246526 4135 6号厅 True 中文版 102 39 02:10 3 52 2D
	依次是日期，影院id，电影id，哪个厅，是否有票，语言，原始票价，打折后票价，播放时间，结束时间(自己换算的没有:)，2或者3d,最后还返回一个自己生成的url 显示时光网自己的内容，有购票的，并不是直达到购票的链接
	'''
	url = 'http://m.mtime.cn/Service/callback-ticket.mi/cinema/showtime.api?cinemaId='+cinemaID
	response = requests.get(url)
	movie_theater_showtime_list = json.loads(response.text)['data']['showtimes']
	for movie_theater_showtimes in movie_theater_showtime_list:
		moviekey = movie_theater_showtimes['moviekey'].split("_")
		time = moviekey[1]
		movieId = movie_theater_showtimes['movieId']
		for movie_theater_showtime in movie_theater_showtimes['list']:
			cinemaPrice = movie_theater_showtime['cinemaPrice']
			hall = movie_theater_showtime['hall']
			isTicket = movie_theater_showtime['isTicket']
			language = movie_theater_showtime['language']
			length = movie_theater_showtime['length']
			price = movie_theater_showtime['price']
			showDay = movie_theater_showtime['showDay']
			start_time_datetime = datetime.utcfromtimestamp(showDay)
			start_time = start_time_datetime.strftime('%H:%M')
			time_house = int(length/60)
			time_m = length%60
			endtime_house = int(start_time_datetime.strftime('%H'))+time_house
			endtime_m = int(start_time_datetime.strftime('%M'))+time_m
			versionDesc = movie_theater_showtime['versionDesc']
			url = 'http://theater.mtime.com/'+stringId+'/'+cinemaID
			print(time, movieId, cinemaID, hall, isTicket, language, length, price, start_time, endtime_house, endtime_m, versionDesc,url)

#get_movie_time('China_Guangdong_Province_Guangzhou_Yuexiu','4135')

def get_movie_info_time(locationId):
	'''
	获取电影的id和名字
	执行get_movie_info_time('365') 数字为城市id 广州365.深圳366
	返回218546 猩球崛起3：终极之战
	一个是电影id 一个是电影名
	'''
	url = 'https://api-m.mtime.cn/Showtime/LocationMovies.api?locationId='+locationId
	response = requests.get(url)
	movie_info_list = json.loads(response.text)['ms']
	for movie_info in movie_info_list:
		movie_id = movie_info['id']
		movie_name = movie_info['t']
		print(movie_id, movie_name)
#get_movie_info_time('365')



#猫眼
"""
爬取成本偏高。
"""
def get_movie_info_maoyan():
	'''
	获取猫眼影院信息，根据ip加载本地的影院
	'''
	url = 'http://m.mtime.cn/#!/citylist/'
	response = requests.get(url)
	print(response.text)

#百度糯米
#城市id 广州257，深圳340 url https://mdianying.baidu.com/city/choose?sfrom=wise_shoubai&from=webapp&sub_channel=&source=&c=257&cc=&kehuduan=
"""
同上但
movie_info_nuomi返回的是该影院这几天的有上映的排片，所以数据多，精确率偏低
"""
def get_movie_info_nuomi():
	"""
	执行get_movie_info_nuomi()
	获取电影id和电影名
	百度糯米设置为不是浏览器打开时displat为none所以用了selenium来加载，然后有没加载的多了hide，所以分两部分提取，hide里面id又分两部分。。。就采用try来区分开
	"""
	driver = webdriver.Chrome()
	driver.get("https://mdianying.baidu.com/?page=movie")
	soup = BeautifulSoup(driver.page_source, "html.parser")
	nuomi_movie_info_list = soup.find_all("div",{"class":"touching movie-list-item border border-top "})
	for nuomi_movie_info in nuomi_movie_info_list:
		movie_id = nuomi_movie_info.find("div",{"class":"poster-show video"}).get("data-movieid")
		movie_name = nuomi_movie_info.find("h4",{"class":"movie-name-text"}).text
		print(movie_id,movie_name)
	nuomi_movie_info_hide_list = soup.find_all("div",{"class":"touching movie-list-item border border-top hide"})
	for nuomi_movie_info_hide in nuomi_movie_info_hide_list:
		try:
			movie_id = nuomi_movie_info_hide.find("div",{"class":"poster-show video"}).get("data-movieid")
			movie_name = nuomi_movie_info_hide.find("h4",{"class":"movie-name-text"}).text
		except:
			movie_id = nuomi_movie_info_hide.find("div",{"class":"poster-show"}).get("data-movieid")
			movie_name = nuomi_movie_info_hide.find("h4",{"class":"movie-name-text"}).text
		print(movie_id,movie_name)

def get_movie_theater_nuomi(city, movie_id, movie_theater_ionName_id):
	"""
	执行get_movie_theater_nuomi("257", "94865", "1587")
	依次是城市id电影id影院所在区/县id
	最后返回影院id影院名
	其中url返回一个json,JSON里面是html代码
	但翻页到没有数据时，movie_theater_list为空(Flase)，退出循环
	"""
	i=0
	movie_theater_list = True
	while movie_theater_list:
		url = 'https://mdianying.baidu.com/movie/schedule?sfrom=wise_shoubai&c='+city+'&cc='+city+'kehuduan=&movie_id='+movie_id+'&from=webapp&pn='+str(i)+'&areaId='+movie_theater_ionName_id+'&isAjax=1'
		response = requests.get(url)
		json_html = json.loads(response.text)['data']
		soup = BeautifulSoup(json_html, "html.parser")
		movie_theater_list = soup.find_all("a",{"class":"schedule-info touching border border-bottom"})
		for movie_theater in movie_theater_list:
			movie_theater_id = movie_theater.find("div",{"class":"cinema-info"}).get("data-uid")
			movie_theater_name = movie_theater.find("div",{"class":"name"}).text.split("(")[0]
			print(movie_theater_id,movie_theater_name)

#get_movie_theater_nuomi("257", "94865", "1587")

def get_movie_nuomi_movie_theater_ionName(city):
	"""
	执行get_movie_nuomi_movie_theater_ionName('257')
	返回区/县id和名字
	"""
	url = 'https://mdianying.baidu.com/movie/cinema?sfrom=wise_shoubai&c='+city+'&cc='+city
	response = requests.get(url)
	movie_theater_ionName_list = json.loads(response.text)['data']['filterData'][0]['children'][0]['children'][1:-1]
	for movie_theater_ionName_info in movie_theater_ionName_list:
		movie_theater_id = movie_theater_ionName_info['id']
		movie_theater_ionName = movie_theater_ionName_info['name']+'区'
		print(movie_theater_id,movie_theater_ionName)
		cursor.execute('insert into movie_xq (xq_name, db_id, city_name_id) values ( %s,%s,%s)', [movie_theater_ionName_name, movie_theater_ionName_id, '1'])
		#cursor.execute('update movie_xq set nuo_id=%s where xq_name=%s', [movie_theater_id, movie_theater_ionName])
		conn.commit()

#get_movie_nuomi_movie_theater_ionName('257')

def movie_info_nuomi(movie_theater_id, city):
	url = 'https://mdianying.baidu.com/cinema/detail?cinemaId='+movie_theater_id+'&sfrom=wise_shoubai&from=webapp&sub_channel=&source=&c='+city+'&cc='+city+'&kehuduan=#showing'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	all_movie_info_list = soup.find_all("div", {"class":"daily-schedule-list"})
	for all_movie_info in all_movie_info_list:
		try:
			day_time = all_movie_info.find("div",{"class":"daily-schedule touching "}).get("data-date")
			#百度给的时间是timestamp然后还多了3个0所以先转为str用list取出正确的时间戳，然后再转换为int再转换为当前的日期。。。
			int_day_time = int(str(day_time)[:-3])
			data_time = datetime.fromtimestamp(int_day_time)
			moon_day_time = data_time.strftime("%m-%d")  
		except:
			moon_day_time = "没有排片信息"
		print(moon_day_time)
		movie_list = all_movie_info.find_all("div",{"class":"daily-schedule touching "})
		for movie_info in movie_list:
			start_time = movie_info.find("div",{"class":"start"}).text
			end_time = movie_info.find("div",{"class":"end"}).text
			language = movie_info.find("div",{"class":"lan"}).text
			theater= movie_info.find_all("div",{"class":"theater"})
			theater_num = theater[0].text
			theater_info = theater[1].text
			price = movie_info.find("div",{"class":"price"}).text.strip()
			old_price = price[1:3]
			new_price = price[3:]
			seqNo = movie_info.get("data-seq-no")
			movie_id = movie_info.get("data-movie-id")
			buy_url = 'https://mdianying.baidu.com/ticket/select?kehuduan=&sfrom=wise_shoubai&sub_channel=&from=webapp&source=&c='+city+'&cc='+city+'&movieId='+movie_id+'&cinemaId='+movie_theater_id+'&seqNo='+seqNo+'&date='+day_time
			print(start_time, end_time, language, theater_num, theater_info ,new_price, old_price, seqNo, buy_url)
		print('---------------------')

#movie_info_nuomi('576','257')

#豆瓣
#由于豆瓣还是作为电影信息的内容，所以多点东西
#广州id=118281深圳id=118282 
def douban_movie_hot_info():
	"""
	执行douban_movie_info()
	返回25723583 英伦对决 https://movie.douban.com/subject/25723583/?from=playing_poster
	依次为id 电影名 对应详情页
	"""
	url='https://movie.douban.com/cinema/nowplaying/guangzhou/'
	response=requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	movie_info_list = soup.find_all("li",{"class":"list-item"})
	for movie_info in movie_info_list:
	    movie_id =  movie_info.get('id')
	    movie_image_url = movie_info.find("img",{"rel":"nofollow"}).get('src')
	    movie_name = movie_info.get('data-title')
	    #movie_url = movie_info.find("a",{"data-psource":"poster"}).get('href')
	    movie_time = movie_info.get('data-duration')
	    path = "./movie/movie_image_"+movie_name
	    dowloadPic(movie_image_url,path)
	    print(movie_time,movie_id,movie_name)
	    cursor.execute('insert into movie_go (movie_name,movie_time,movie_id) values ( %s, %s, %s)', [movie_name,movie_time,movie_id])
	    conn.commit()
	    conn.close()
#douban_movie_hot_info()

def movie_subject():
	"""
	根据电影id返回页面数据，评论另外url处理，每次递增20,跟review_page_all可以计算总页面
	详细的评论可以从一条jsURL获得，而且获得的是一个页面。。。

	"""
	url='https://movie.douban.com/subject/24753477/?from=playing_poster'
	response=requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	movie_title = soup.find("span",{"property":"v:itemreviewed"}).text
	movie_year = soup.find("span",{"class":"year"}).text
	movie_score = soup.find("strong",{"class":"ll rating_num"}).text
	movie_score_all_num = soup.find("span",{"property":"v:votes"}).text
	movie_score_about = soup.find("div",{"class":"rating_betterthan"}).text.replace(' ','').split('\n')[1:3]
	movie_score_about = ','.join(movie_score_about)
	movie_img = soup.find("img",{"rel":"v:image"}).get('src')
	movie_info = soup.find("div",{"id":"info"}).text.split('\n')[1:-1]
	movie_related_info = soup.find("span",{"property":"v:summary"}).text.replace('\n','').replace(' ','')
	review_page_all = soup.find("a",{"href":"reviews"}).text
	pattern = re.compile(r'\d+')
	review_page_all = re.findall(pattern, review_page_all)
	print(movie_title, movie_year, movie_score, movie_score_all_num,
		  movie_score_about, movie_img, movie_info, movie_related_info, review_page_all)
	print('------')
	#短评
	url1='https://movie.douban.com/subject/24753477/comments?sort=new_score&status=P'
	response1=requests.get(url1)
	soup1 = BeautifulSoup(response1.text, "html.parser")
	review1_list =soup1.find_all("div",{"class":"comment-item"})
	for review1 in review1_list:
		review_author = review1.find("div",{"class":"avatar"}).find("a").get('title')
		review_time = review1.find("span",{"class":"comment-time "}).get('title')
		review = review1.find('div',{"class":"comment"}).find("p").text.strip()
		print(review_author, review_time, review)
		print('------')

    #长评(由于进行数据处理，耗时较长)
	url2='https://movie.douban.com/subject/24753477/reviews?start=0'
	response2=requests.get(url2)
	soup2 = BeautifulSoup(response2.text, "html.parser")
	review_list =soup2.find_all("div",{"class":"main review-item"})
	for review in review_list:
		review_id = review.get('id')
		review_header = review.find("a",{"class":"title-link"}).text
		review_author = review.find("a",{"class":"author"}).text.strip()
		review_author_url = review.find("a",{"class":"author"}).get('href')
		review_short = review.find("div",{"class":"short-content"}).text.replace('\n','').split('(')[0].split('>')[0].strip()
		review_full_url = 'https://movie.douban.com/review/'+str(review_id)
		review_full_json_url = 'https://movie.douban.com/j/review/'+str(review_id)+'/full'
		response_json = requests.get(review_full_json_url)
		print(review_id, review_header, review_author, review_author_url, 
			  review_short ,review_full_url, review_full_json_url)
		print('------')
		json_html = json.loads(response_json.text)['body']

movie_subject()

def douban_movie_theater_ionName():
	"""
	获取区/县 的id和名字
	s_id电影id，loc_id城市id
[{'douban_ionName_id': '130277', 'douban_ionName_name': '从化'}, {'douban_ionName_id': '130266', 'douban_ionName_name': '荔湾区'}, {'douban_ionName_id': '130267', 'douban_ionName_name': '越秀区'}, {'douban_ionName_id': '130268', 'douban_ionName_name': '海珠区'}, {'douban_ionName_id': '130269', 'douban_ionName_name': '天河区'}, {'douban_ionName_id': '130270', 'douban_ionName_name': '白云区'}, {'douban_ionName_id': '130271', 'douban_ionName_name': '黄埔区'}, {'douban_ionName_id': '130272', 'douban_ionName_name': '番禺区'}, {'douban_ionName_id': '130273', 'douban_ionName_name': '花都区'}, {'douban_ionName_id': '130274', 'douban_ionName_name': '南沙区'}, {'douban_ionName_id': '130275', 'douban_ionName_name': '萝岗区'}, {'douban_ionName_id': '130276', 'douban_ionName_name': '增城'}]	"""
	url = 'https://movie.douban.com/ticket/pop_up?s_id=25723583&loc_id=118281&from=undefined'
	response = requests.get(url) 
	soup = BeautifulSoup(response.text, "html.parser")
	movie_theater_ionName_list = soup.find_all("a",{"class":"district-item"})[:-1]
	doubao_movie_theater_ionName_list = []
	for movie_theater_ionName in movie_theater_ionName_list:
		movie_theater_ionName_id = movie_theater_ionName.get('id')
		movie_theater_ionName_name = movie_theater_ionName.text
		movie_theater_ionName_dict = dict(douban_ionName_id=movie_theater_ionName_id, douban_ionName_name=movie_theater_ionName_name)
		doubao_movie_theater_ionName_list.append(movie_theater_ionName_dict)
		print(doubao_movie_theater_ionName_list)
#douban_movie_theater_ionName()

def douban_movie_theater(city_id, ionName_id):
	"""
	需要城市id 区名id
	返回影院id和影院名
	"""
	url = 'https://movie.douban.com/j/cinema/cinemas/?city_id='+city_id+'&district_id='+ionName_id
	response = requests.get(url)
	json_html = json.loads(response.text)
	movie_theater_list = []
	for movie_theater_info in json_html:
		movie_theater_id = movie_theater_info['site_id']
		movie_theater_name = movie_theater_info['name']
		movie_theater_dict = dict(movie_theater_id=movie_theater_id, movie_theater_name=movie_theater_name,movie_theater_ionName_id=ionName_id)
		movie_theater_list.append(movie_theater_dict)
	print(movie_theater_list)
#douban_movie_theater('118281','130277')
def douban_movie_info():
	url = 'https://movie.douban.com/j/cinema/schedules?date=2017-10-12&s_id=25723583&site_id=274933'
	response = requests.get(url)
	json_html = json.loads(response.text)
	movie_info_list = []
	for movie_info in json_html:
		movie_version = movie_info['version']
		movie_price = movie_info['price']
		movie_language = movie_info['language']
		movie_start_time = movie_info['time']
		movie_buy_url = movie_info['ticket_url']
		movie_info_dict = dict(movie_version=movie_version, movie_price=movie_price,
			                   movie_language=movie_language, movie_start_time=movie_start_time, movie_buy_url=movie_buy_url)
		movie_info_list.append(movie_info_dict)
	print(movie_info_list)
#douban_movie_info()
"""
if __name__ == '__main__':
	#pinpaigongyu_58city(1)
	conn = pymysql.connect(user='root', password='password', database='Django_bysj_mysql_movie', charset='utf8')
	cursor = conn.cursor() 
	try:
		douban_movie_info()
	finally:
		conn.close()
"""