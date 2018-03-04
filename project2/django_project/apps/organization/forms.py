import re

from django import forms

from operations.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''
        验证手机号码
        错误时要抛出forms.ValidationError异常
        '''
        mobile = self.cleaned_data['mobile']
        mobile_re = "^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$"
        p = re.compile(mobile_re)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
