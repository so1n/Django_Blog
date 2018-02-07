"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin


from django.conf.urls import url, include
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetUserView, ModifyPwdView

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),

    url('^login/$', LoginView.as_view(), name="login"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url('^active/(?P<active_code>\w+)/$', ActiveUserView.as_view(), name="user_active"),
    url('^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url('^reset/(?P<reset_code>\w+)/$', ResetUserView.as_view(), name="user_reset"),
    url('^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url('^$', TemplateView.as_view(template_name="index.html"), name="index")
]
