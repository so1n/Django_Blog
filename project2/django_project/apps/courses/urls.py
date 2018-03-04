from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddComentsView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comment"),
    url(r'^add_comment/$', AddComentsView.as_view(), name="course_add_comment")
]