from .models import Comment, Post, Answer
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)

        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'nickname', ]  #username이 ID여서 일단 뺌
