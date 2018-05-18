from django.conf.urls import url
from .views import MapView, MapJsonView, MapJsonUserView

urlpatterns = [
    url(r'^map/$', MapView.as_view(), name='map'),
    url(r'^map_json/$', MapJsonView.as_view(), name='map_json'),
    url(r'^map_json_user/$', MapJsonUserView.as_view(), name='map_json_user'),
]