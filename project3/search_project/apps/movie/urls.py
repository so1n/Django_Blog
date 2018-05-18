from django.conf.urls import url
from .views import MovieIndex, MovieInfo, MovieTicket

urlpatterns = [
    url(r'^$', MovieIndex.as_view(), name="movie_index"),
    url(r'^info/(?P<movie_id>\d+)/$', MovieInfo.as_view(), name="movie_info"),
    url(r'^ticket/(?P<movie_id>\d+)/$', MovieTicket.as_view(), name="movie_ticket")
]