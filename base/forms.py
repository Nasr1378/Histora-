from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User,File


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['host' ]


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name','file','file_type']
       




class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio','qualification']