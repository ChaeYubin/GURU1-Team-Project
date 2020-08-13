from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin



class PostList(ListView):
    model = Post

    # 역순만들기
    def get_queryset(self):
        return Post.objects.order_by('-created')

class Postdetail(DetailView):
    model = Post

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'content', 'head_image'
    ]

    def form_valid(self, form):
        current_user= self.request.user
        if current_user.in_authenticated:
            form.instance.author = self.request.user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(UpdateView):
    model = Post
    fields = [
        'title', 'content', 'head_image',
    ]