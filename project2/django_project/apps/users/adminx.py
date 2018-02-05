import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseMyAdminView(object):
    '''
    enable_themes 启动更改主题
    use_bootswatch 启用网上主题
    '''
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    '''
    site_title 左上角名称
    site_footer 底部名称
    menu_style 更改左边样式
    '''
    site_title = "学习网后台管理系统"
    site_footer = "学习网"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['email', 'code', 'send_type', 'send_time']
    search_fields = ['email', 'code', 'send_type']
    list_filter = ['email', 'code', 'send_type', 'send_time']


class BannerAdmin(object):
    list_disply = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseMyAdminView)
xadmin.site.register(views.CommAdminView, GlobalSettings)