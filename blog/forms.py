from .models import Comment, Answer
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
