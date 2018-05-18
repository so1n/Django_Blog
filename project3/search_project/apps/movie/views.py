from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, PageNotAnInteger

from .models import Movie, MovieComment
from movie.models import City, CorD, Cinema, RMovieTicketInfo


class MovieIndex(View):
    def get(self, request):
        now_movie_list = []
        all_movie_list = Movie.objects.filter(emotion_num=1)
        for all_movie in all_movie_list:
            if all_movie.add_time.strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'):
                now_movie_list.append(all_movie)
        return render(request, 'search/movie.html', {
            'movie_list': now_movie_list,
            'title': '电影'
        })


class MovieInfo(View):
    def get(self, request, movie_id):
        movie_info = Movie.objects.filter(doubanid=movie_id)[0]
        comment_list = MovieComment.objects.filter(doubanid=movie_id)
        comment_num = comment_list.count()
        now_movie_list = []
        all_movie_list = Movie.objects.all()
        for all_movie in all_movie_list:
            if all_movie.add_time.strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'):
                now_movie_list.append(all_movie)
        now_movie_list = now_movie_list[:10]

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #第二个的参数为每页显示多少数量
        p = Paginator(comment_list, 10, request=request)
        comment_list = p.page(page)

        return render(request, 'search/movie_info.html', {
            'movie_info': movie_info,
            'all_movie_list': now_movie_list,
            'comment_list': comment_list,
            'title': movie_info.name,
            'comment_num': comment_num
        })


class MovieTicket(View):
    def get(self, request, movie_id):
        qx_list = []
        cinema_list = []
        tpp_list = []
        time_list = []
        qx_id = ''
        cinema_id = ''
        movie_info = Movie.objects.filter(doubanid=movie_id)[0]
        all_movie_list = Movie.objects.all()[:7]
        city_list = City.objects.all()
        city_id = request.GET.get('city', '')
        if city_id:
            qx_list = CorD.objects.filter(cord_city=city_id)
            qx_id = request.GET.get('qx', '')
            if qx_id:
                cinema_list = Cinema.objects.filter(cinema_cord=qx_id)
                cinema_id = request.GET.get('cinema', '')
                if cinema_id:
                    tpp_list = RMovieTicketInfo.objects.filter(ticket_type=1)
                    time_list = RMovieTicketInfo.objects.filter(ticket_type=3)

        return render(request, 'search/movie_ticket.html', {
            'movie_info': movie_info,
            'all_movie_list': all_movie_list,
            'title': movie_info.name,
            'city_list': city_list,
            'qx_list': qx_list,
            'cinema_list': cinema_list,
            'city_id': city_id,
            'qx_id': qx_id,
            'cinema_id': cinema_id,
            'tpp_list': tpp_list,
            'time_list': time_list
        })
