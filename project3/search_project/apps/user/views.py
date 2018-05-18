from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, UserFav, UserTag
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from house.models import HouseInfo
from movie.models import Movie
from information.models import Information


class Index(View):
    def get(self, request):
        return render(request, 'search/base.html', {
            'title': '首页'
        })


class CustomBackend(ModelBackend):
    """
    定义自己的验证类型：
    需在setting设置：
    AUTHENtICATION_BACKENDS = (
        'users.views.CustomBackend',
    )
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("user:index"))


class LoginView(View):
    """
    LoginForm验证数据(./forms.py)
    """

    def post(self, request):
        login_from = LoginForm(request.POST)
        if login_from.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            next_url = request.POST.get("next_url", "")
            user = authenticate(username=user_name, password=pass_word)
            if user:  # 用户是否存在
                if user.is_active:  # 用户是否处于激活状态
                    login(request, user)
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
                        return HttpResponseRedirect(reverse("user:index"))
                else:
                    return render(request, "search/login.html", {"msg": "请激活账户"})
            else:
                return render(request, "search/login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "search/login.html", {
                "login_form": login_from,
            })

    def get(self, request):
        next_url = request.GET.get("next", "")
        return render(request, "search/login.html", {
            "next_url": next_url,
            "title": '登录'
        })


class RegisterView(View):
    """
    注册视图类

    验证码使用Django Simple Captcha

    RegisterForm验证数据(./forms.py)
    """

    def get(self, request):
        """
        通过RegisterForm()获取验证码
        """
        register_form = RegisterForm()
        return render(request, "search/register.html", {
            'register_form': register_form,
            "title": '注册'}
                      )

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "search/register.html", {'msg': '该邮箱已经存在', 'register_form': register_form})
            else:
                pass_word = request.POST.get("password", "")
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()

                send_register_email.delay(user_name, 'register')
                return render(request, "search/register.html", {'msg': '请查收邮箱链接激活账户', 'register_form': register_form})
        else:
            return render(request, "search/register.html", {'register_form': register_form})


class ActiveUserView(View):
    """
    激活账户
    """

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'search/404.html')
        return render(request, "search/login.html", {
            'title': '登录'
        })


class ForgetPwdView(View):
    """找回密码"""

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "search/forgetpwd.html", {
            'forget_form': forget_form,
            "title": '忘记密码'
        })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email")
            send_register_email.delay(email, 'forget')
            return render(request, "search/forgetpwd.html", {'msg': '请从邮箱打开链接修改密码'})
        else:
            return render(request, "search/forgetpwd.html", {'forget_form': forget_form})


class ResetUserView(View):
    """
    找回密码页面(get)
    """

    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                return render(request, 'search/password_reset.html', {
                    'email': record.email,
                    "title": '登录'
                })
        else:
            return render(request, 'search/404.html')


class ModifyPwdView(View):
    """
    找回密码页面(post),未登录状态
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get("email", "")
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            if pwd1 != pwd2:
                return render(request, 'search/password_reset.html', {'email': email, 'msg': "密码不一致"})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'search/login.html', {'email': email, 'msg': "修改成功，请重新登录"})
        else:
            return render(request, "search/password_reset.html", {"email": email, 'msg': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        user = request.user
        return render(request, 'search/usercenter-info.html', {
            "title": '个人中心',
            "user": user
        })

    def post(self, request):
        user = request.user
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return render(request, 'search/usercenter-info.html', {
                "title": '个人中心',
                "user": user,
                "msg": '保存成功',
                "code": 1,
            })
        else:
            return render(request, 'search/usercenter-info.html', {
                "title": '个人中心',
                "user": user,
                "msg": '保存失败',
                "code": 0,
                'user_info_form': user_info_form
            })


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    使用models.form，要确保要获取的数据的html的id和自己定义的model名称要对应，不然clean_data取不了数据
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})


class UpdatePwdView(LoginRequiredMixin, View):
    """
    找回密码页面(post),登录状态
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            if pwd1 != pwd2:
                return JsonResponse({'status': 'success'})
            else:
                user = request.user
                user.password = make_password(pwd2)
                user.save()
                return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(modify_form.errors)


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'status': 'fail'})
        send_register_email.delay(email, "update_email", num=4)
        return JsonResponse({'status': 'success'})


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱表单的提交
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'email': '验证码出错'})


class MyFavHouseView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏-房源
    """

    def get(self, request):
        house_list = []
        fav_houses = UserFav.objects.filter(user=request.user, fav_type=1)
        house_append_temp = house_list.append
        for fav_house in fav_houses:
            house_id = fav_house.fav_id
            house = HouseInfo.objects.get(id=house_id)
            house_append_temp(house)
        return render(request, 'search/usercenter-fav-org.html', {
            'house_list': house_list
        })


class MyFavInfoView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏-资讯
    """

    def get(self, request):
        info_list = []
        fav_infos = UserFav.objects.filter(user=request.user, fav_type=3)
        info_append_temp = info_list.append
        for fav_info in fav_infos:
            info_id = fav_info.fav_id
            info = Information.objects.get(id=info_id)
            info_append_temp(info)
        return render(request, 'search/usercenter-fav-teacher.html', {
            'info_list': info_list
        })


class MyFavMovieView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏-电影
    """

    def get(self, request):
        movie_list = []
        fav_movies = UserFav.objects.filter(user=request.user, fav_type=2)
        movie_append_temp = movie_list.append
        for fav_movie in fav_movies:
            movie_id = fav_movie.fav_id
            movie = Movie.objects.get(id=movie_id)
            movie_append_temp(movie)
        return render(request, 'search/usercenter-fav-course.html', {
            'movie_list': movie_list
        })


def page_404(request):
    response = render_to_response('search/404.html', {})
    response.status_code = 404
    return response


class AddFavView(LoginRequiredMixin, View):
    """
    用户收藏以及取消
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        #判断用户是否登录
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})

        #判断收藏记录是否存在
        exist_records = UserFav.objects.filter(user_name=request.user, fav_id=int(fav_id), type=int(fav_type))
        if exist_records:
            exist_records.delete()
            # fav_nums 自减
            if int(fav_type) == 1:
                temp_object = HouseInfo.objects.filter(id=int(fav_id))[0]
            elif int(fav_type) == 2:
                temp_object = Movie.objects.filter(id=int(fav_id))[0]
            elif int(fav_type) == 3:
                temp_object = Information.objects.filter(id=int(fav_id))[0]
            if int(fav_type) == 3:
                temp_object.u_fav_nums -= 1
                if temp_object.u_fav_nums < 0:
                    temp_object.u_fav_nums = 0
                temp_object.save()
            else:
                temp_object.fav_nums -= 1
                if temp_object.fav_nums < 0:
                    temp_object.fav_nums = 0
                temp_object.save()

            return JsonResponse({'status': 'fail', 'msg': '取消成功'})
        else:
            user_fav = UserFav()
            if int(fav_id) > 0 and int(fav_id) > 0:
                user_fav.user_name = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.type = int(fav_type)
                user_fav.save()
                # fav_nums 自增
                if int(fav_type) == 1:
                    temp_object = HouseInfo.objects.filter(id=int(fav_id))[0]
                elif int(fav_type) == 2:
                    temp_object = Movie.objects.filter(id=int(fav_id))[0]
                elif int(fav_type) == 3:
                    temp_object = Information.objects.filter(id=int(fav_id))[0]
                if int(fav_type) == 3:
                    temp_object.u_fav_nums += 1
                    temp_object.save()
                else:
                    temp_object.fav_nums += 1
                    temp_object.save()
                return JsonResponse({'status': 'success', 'msg': '收藏成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})


class TagView(View):
    def post(self, request):
        check_box_list = request.POST.getlist('check_box_list')
        for check in check_box_list:
            try:
                UserTag.objects.get(user=request.user, name=check)
            except UserTag.DoesNotExist:
                UserTag.objects.create(user=request.user, name=check)
        all_tag = UserTag.objects.filter(user=request.user)
        for tag in all_tag:
            if tag.name not in check_box_list:
                tag.name = ''
                tag.save()
        return HttpResponseRedirect('/info/')
