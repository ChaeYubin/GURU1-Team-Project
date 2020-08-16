from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Post, Category, Comment
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tkinter import messagebox


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

    return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return redirect("blog:login")


def signup_view(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            print(request.POST)
            nickname = request.POST["nickname"]
            username = request.POST["username"]
            password = request.POST["password1"]
            email = request.POST["email"]

            user = User.objects.create(username, email, password)
            user.nickname = nickname
            user.save()

            return redirect("user:login")
        else:
            messagebox.showinfo("warning", "패스워드가 서로 다릅니다.")
    return render(request, "blog/signup.html")


class PostList(ListView):
    model = Post

    # 역순만들기
    def get_queryset(self):
        return Post.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
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


class PostListByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title']='blog - {}'.format(category.name)
        return context


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


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post

    if request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url() + '#comment-list')
    else:
        return redirect('/blog/')


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment
