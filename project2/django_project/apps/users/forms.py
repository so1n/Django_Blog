from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    '''
    表单数据检查
    '''
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空'},min_length=10)


class RegisterForm(forms.Form):
    '''
    邮箱注册数据检查
    '''
    email = forms.EmailField(required=True,error_messages={'required': '邮箱不能为空'})
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空'}, min_length=10)
    captcha = CaptchaField(required=True, error_messages={'required': '验证码不能为空', 'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    '''
    找回密码数据检查
    '''
    email = forms.EmailField(required=True,error_messages={'required': '邮箱不能为空'})
    captcha = CaptchaField(required=True, error_messages={'required': '验证码不能为空', 'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    '''
    修改密码数据检查
    '''
    password1 = forms.CharField(required=True, error_messages={'required': '密码不能为空'}, min_length=10)
    password2 = forms.CharField(required=True, error_messages={'required': '密码不能为空'}, min_length=10)