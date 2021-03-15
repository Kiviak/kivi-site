from django import forms

class SearchForm(forms.Form):
    keyword=forms.CharField(label='')

from django.core.exceptions import  ValidationError
from django.core import validators

class UserForm(forms.Form):
    username=forms.CharField(max_length=128,min_length=1,required=True,label='用户名')
    password=forms.CharField(max_length=128,min_length=8,required=True,label='密码',widget=forms.PasswordInput)
    
    username.widget.attrs.update({'id': 'username'})
    password.widget.attrs.update({'id': 'password'})
    
class ReviewForm(forms.Form):
    text=forms.CharField(required=True,min_length=1,widget=forms.Textarea,label='')
    text.widget.attrs.update({'id': 'text'})

class ChangePasswordForm(forms.Form):
    password=forms.CharField(max_length=128,min_length=8,required=True,label='密码',widget=forms.PasswordInput)
    newpassword=forms.CharField(max_length=128,min_length=8,required=True,label='新密码',
    widget=forms.PasswordInput,validators=[validators.RegexValidator('^[a-z0-9]+$','存在违规字符')])
    newpassword2=forms.CharField(max_length=128,min_length=8,required=True,label='新密码',widget=forms.PasswordInput)
   
    password.widget.attrs.update({'id': 'password'})
    newpassword.widget.attrs.update({'id': 'newpassword'})
    newpassword2.widget.attrs.update({'id': 'newpassword2'})

class SignUpForm(forms.Form):
    email=forms.EmailField(label='邮箱',required=True)
    username=forms.CharField(max_length=128,min_length=1,required=True,label='用户名',
        validators=[validators.RegexValidator('^[a-z][a-z0-9]+$','用户名不符合规定')])
    password=forms.CharField(max_length=128,min_length=8,required=True,label='密码',
        widget=forms.PasswordInput,validators=[validators.RegexValidator('^[a-z0-9]+$','存在违规字符')])
    
    email.widget.attrs.update({'id': 'email'})
    username.widget.attrs.update({'id': 'username'})
    password.widget.attrs.update({'id': 'password'})