import json
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

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operations.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course



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
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))



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
            if user:         #用户是否存在
                if user.is_active:           #用户是否处于激活状态
                    login(request, user)
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
                        return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "请激活账户"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {
                "login_form": login_from
            })

    def get(self, request):
        next_url = request.GET.get("next", "")
        return render(request, "login.html", {
            "next_url": next_url
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
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {'msg': '该邮箱已经存在', 'register_form':register_form})
            else:
                pass_word = request.POST.get("password", "")
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()

                #注册消息
                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = "欢迎注册"
                user_message.save()

                send_register_email.delay(user_name, 'register')
                return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form':register_form})


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
            return render(request, '404.html')


class ForgetPwdView(View):
    """找回密码"""
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email")
            send_register_email.delay(email, 'forget')
            return render(request, "forgetpwd.html", {'msg': '请从邮箱打开链接修改密码'})
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})


class ResetUserView(View):
    """
    找回密码页面(get)
    """
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                return render(request, 'password_reset.html', {'email': record.email})
        else:
            return render(request, '404.html')


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
                return render(request, 'password_reset.html', {'email': email, 'msg': "密码不一致"})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'login.html', {'email': email, 'msg': "修改成功，请重新登录"})
        else:
            return render(request, "password_reset.html", {"email": email, 'msg': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(user_info_form.errors)


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


class MyCourse(LoginRequiredMixin, View):
    """
    个人中心-我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏-机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        org_append_temp = org_list.append
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_append_temp(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏-讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_append_temp = teacher_list.append
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_append_temp(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏-课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        course_append_temp = course_list.append
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_append_temp(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list
        })


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_message = UserMessage.objects.filter(user_id=request.user.id)
        all_unread_message = UserMessage.objects.filter(user_id=request.user.id, has_read=False)
        for message in all_unread_message:
            message.has_read = True
            message.save()


        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #第二个的参数为每页显示多少数量
        p = Paginator(all_message, 10, request=request)
        all_message = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': all_message
        })


def page_404(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response