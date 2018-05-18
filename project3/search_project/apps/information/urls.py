from django.conf.urls import url
from .views import InfoIndex, ReadView

urlpatterns = [
    url(r'^$', InfoIndex.as_view(), name="Info_Index"),
    url(r'^read/(?P<detail_id>\d+)/$', ReadView.as_view(), name='read')
]