from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView


class PostList(ListView):
    model = Post

    # 역순만들기
    def get_queryset(self):
        return Post.objects.order_by('-created')

class Postdetail(DetailView):
    model = Post