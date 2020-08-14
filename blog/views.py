from django.shortcuts import render, redirect
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
    model = Post

    # 역순만들기
    def get_queryset(self):
        return Post.objects.order_by('-created')


class Postdetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Postdetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        return context


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


def new_comment(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
    else:
        return redirect('/blog/')