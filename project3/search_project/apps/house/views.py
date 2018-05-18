from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from .models import HouseInfo
from user.models import UserFav
from utils.mixin_utils import LoginRequiredMixin


class MapView(LoginRequiredMixin, View):
    def get(self, request):
        city_request_code = request.GET.get("city", "")
        if city_request_code == 'gz':
            city = '广州'
            city_code = "'广州'"
            location = '[113.260724,23.1176]'
            city_id = '1'
        elif city_request_code == 'sz':
            city = '深圳'
            city_code = "'深圳'"
            location = '[114.091565,22.544242]'
            city_id = '2'
        else:
            city = '广州'
            city_code = "'广州'"
            location = '[113.260724,23.1176]'
            city_id = '1'
        return render(request, 'search/map.html', context={
                          'title': '房源',
                          'city_code': city_code,
                          'city': city,
                          'location': location,
                          'error_msg': '',
                          'city_num': city_id
                      })


class MapJsonView(View):
    def get(self, request):
        house_type = request.GET.get('house_type', "1")
        price = request.GET.get('price', "0_2000")
        house_price_list = price.split('_')
        house_city = request.POST.get('city_num', "1")
        all_house = HouseInfo.objects.filter(house_city=house_city,
                                             house_type=house_type,
                                             house_price__gte=int(house_price_list[0]),
                                             house_price__lte=int(house_price_list[1])
                                             )
        data = []
        for row in all_house:
            #if int(row.house_price) > int(house_price_list[0]) and int(row.house_price) < int( house_price_list[1]):
            data.append({"info_title": row.name, "address": row.house_address, "house_url": row.house_url,
                         "price": row.house_price, "room_info": row.house_detail, "city_name": house_city,
                         "house_image": row.house_image_url, "id": row.id})

        return JsonResponse(data, safe=False)


class MapJsonUserView(LoginRequiredMixin, View):
    def get(self, request):
        house_city = request.POST.get('city_num', "1")
        #取出用户收藏的房源
        user_fav_house_list = UserFav.objects.filter(user_name=request.user, type=1)
        if user_fav_house_list:
            #取出所有收藏该房源的列表
            fav_house_list = []
            for user_fav_house in user_fav_house_list:
                fav_house_list.extend(UserFav.objects.filter(fav_id=user_fav_house.fav_id, type=1))
            #取出用户
            for fav_house in fav_house_list:
                fav_user_list = list(set([fav_house.user_name for fav_house in fav_house_list]))
            #取出用户关注的房源
            all_fav_house_list = []
            for fav_user in fav_user_list:
                all_fav_house_list.extend(UserFav.objects.filter(user_name=fav_user, type=1))
            #取出房源
            all_house = []
            for all_fav_house in all_fav_house_list:
                all_house.extend(HouseInfo.objects.filter(id=all_fav_house.fav_id).order_by('-fav_nums'))
            all_house = all_house[:10]

        else:
            all_house = []
        data = []
        for row in all_house:
            #if int(row.house_price) > int(house_price_list[0]) and int(row.house_price) < int( house_price_list[1]):
            data.append({"info_title": row.name, "address": row.house_address, "house_url": row.house_url,
                         "price": row.house_price, "room_info": row.house_detail, "city_name": house_city,
                         "house_image": row.house_image_url, "id": row.id})

        return JsonResponse(data, safe=False)

