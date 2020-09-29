from django import forms
from django.core.validators import RegexValidator

from bbs import models


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3,
                           max_length=20,
                           required=True,
                           label='用户名',
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           error_messages={
                               'min_length': '用户名最少3位',
                               'max_length': '用户名最多20位',
                               'required': '用户名必填'
                           }
                           )
    password = forms.CharField(min_length=8,
                               max_length=20,
                               required=True,
                               label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={
                                   'min_length': '密码最少8位',
                                   'max_length': '密码最多20位',
                                   'required': '密码必填'
                               },
                               validators=[RegexValidator(r'^[1-9A-Za-z]{8,}$', '密码必须数字母或数字组合，且8位以上')]
                               )
    confirm = forms.CharField(required=True,
                              label='确认密码',
                              error_messages={
                                  'required': '密码必填'
                              },
                              widget=forms.PasswordInput(attrs={'class': 'form-control'})
                              )

    email = forms.EmailField(required=True,
                             label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             error_messages={
                                 'required': '邮箱必填',
                                 'invalid': '邮箱格式不正确',
                             },
                             )

    # 校验用户名是否存在
    def clean_username(self):
        name_ = self.cleaned_data.get('username')
        is_exist = models.User.objects.filter(username=name_)
        if is_exist:
            # 用户已存在
            self.add_error('username', '用户名已存在')
        return name_

    # 校验两次密码是否一致
    def clean(self):
        password_ = self.cleaned_data.get('password')
        confirm_ = self.cleaned_data.get('confirm')
        if not (password_ == confirm_):
            self.add_error('confirm','两次密码不一致')
        return self.cleaned_data
