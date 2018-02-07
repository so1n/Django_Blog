from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email

# Create your views here.
class CustomBackend(ModelBackend):
    '''
    定义自己的验证类型：
    需在setting设置：
    AUTHENtICATION_BACKENDS = (
        'users.views.CustomBackend',
    )
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    '''
    LoginForm验证数据(./forms.py)
    '''
    def post(self, request):
        login_from = LoginForm(request.POST)
        if login_from.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user:         #用户是否存在
                if user.is_active:           #用户是否处于激活状态
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "请激活账户"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_from})

    def get(self, request):
        return render(request, "login.html", {})


class RegisterView(View):
    '''
    注册视图类
    
    验证码使用Django Simple Captcha
    
    RegisterForm验证数据(./forms.py)
    '''
    def get(self, request):
        '''
        通过RegisterForm()获取验证码
        '''
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
                send_register_email(user_name, 'register')
                return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form':register_form})


class ActiveUserView(View):
    '''
    激活账户
    '''
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
    '''找回密码'''
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email")
            send_register_email(email, 'forget')
            return render(request, "forgetpwd.html", {'msg': '请从邮箱打开链接修改密码'})
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})


class ResetUserView(View):
    '''
    找回密码页面(get)
    '''
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                return render(request, 'password_reset.html', {'email': record.email})
        else:
            return render(request, '404.html')


class ModifyPwdView(View):
    '''
    找回密码页面(post)
    '''
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

