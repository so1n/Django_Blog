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


from django.views.static import serve
from django_project.settings import MEDIA_ROOT
from django.conf.urls import url, include
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    #users.view相关url
    url(r'', include('users.urls')),
    #课程首页相关url
    url(r'^org/', include('organization.urls', namespace="org")),
    #课程相关url
    url(r'^course/', include('courses.urls', namespace="course")),

    url('^$', TemplateView.as_view(template_name="index.html"), name="index")
]

handler404 = 'users.views.page_404'