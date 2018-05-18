import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from movie.models import RMovieTicketInfo


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
    site_title = "后台管理系统"
    site_footer = ""
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['email', 'code', 'send_type', 'send_time']
    search_fields = ['email', 'code', 'send_type']
    list_filter = ['email', 'code', 'send_type', 'send_time']


class RMovieTicketAdmin(object):
    list_disply = ['ticket_s_time', 'ticket_e_time', 'ticket_type'
                    , 'ticket_lg', 'ticket_tn', 'ticket_np', 'ticket_op', 'add_time']
    search_fields = ['ticket_s_time', 'ticket_e_time'
                    , 'ticket_lg', 'ticket_tn', 'ticket_np', 'ticket_op', 'add_time']
    list_filter = ['ticket_s_time', 'ticket_e_time'
                    , 'ticket_lg', 'ticket_tn', 'ticket_np', 'ticket_op', 'add_time']



xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(RMovieTicketInfo, RMovieTicketAdmin)
xadmin.site.register(views.BaseAdminView, BaseMyAdminView)
xadmin.site.register(views.CommAdminView, GlobalSettings)