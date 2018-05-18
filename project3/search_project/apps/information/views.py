from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from .models import Information
from user.models import UserFav, UserTag, Tag


class InfoIndex(View):
    def get(self, request):
        r_info_list = []
        info_list = Information.objects.all()
        user_tag = UserTag.objects.filter(user=request.user)
        print(user_tag)
        tag_list = Tag.objects.all()
        tag = request.GET.get("tag", '')
        if tag:
            info_list = info_list.filter(tag=tag)
        info_type = request.GET.get('type', 'new')
        if info_type == 'new':
            info_list = info_list.order_by("-add_time")
        elif info_type == 'hot':
            info_list = info_list.order_by("-fav_nums", "-read_nums")

        for info in info_list:
            fav = False
            if UserFav.objects.filter(user_name=request.user, fav_id=int(info.id), type=3):
                fav = True
            info_dict = dict(fav=fav, info=info)
            r_info_list.append(info_dict)


        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(r_info_list, 10, request=request)
        info_list = p.page(page)

        return render(request, 'search/info.html', context={
                          'title': '资讯',
                          'info_list': info_list,
                          'type': info_type,
                          'tag_list': tag_list,
                          'tag': tag,
                          'user_tag': user_tag
                      })


class ReadView(View):
    def get(self, request, detail_id):
        detail = Information.objects.get(id=detail_id)
        detail.u_read_nums += 1
        detail.save()
        return HttpResponseRedirect(detail.url)

