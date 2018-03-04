from django.conf.urls import url
from .views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetUserView, ModifyPwdView, UserInfoView, \
    UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourse, MyFavOrgView, MyFavTeacherView, \
    MyFavCourseView, MymessageView, LogoutView


urlpatterns = [
    #用户注册登录改密码等uel
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>\w+)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>\w+)/$', ResetUserView.as_view(), name="user_reset"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    #个人中心,资料修改相关url
    url(r'^user/info/$', UserInfoView.as_view(), name="user_info"),
    url(r'^user/image/upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^user/update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    url(r'^user/send_email_code/$', SendEmailCodeView.as_view(), name="send_email_code"),
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    #个人中心，收藏相关
    url(r'^my_fav/org/$', MyFavOrgView.as_view(), name="my_fav_org"),
    url(r'^my_fav/teacher/$', MyFavTeacherView.as_view(), name="my_fav_teacher"),
    url(r'^my_fav/course/$', MyFavCourseView.as_view(), name="my_fav_course"),

    #个人中心其他相关url
    url(r'^my_course/$', MyCourse.as_view(), name="my_course"),
    url(r'^my_message/$', MymessageView.as_view(), name="my_message"),
]


