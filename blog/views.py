from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, Post, Category, Comment, Tag, Question, Answer
from .forms import CommentForm, CustomUserChangeForm, AnswerForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from tkinter import messagebox
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "blog/post_list+css.html")
        else:
            messagebox.showinfo("warning", "ID 또는 비밀번호가 올바르지 않습니다.")

    return render(request, "blog/login+css.html")


def logout_view(request):
    logout(request)
    return redirect("blog:login")


def signup_view(request):
    if request.method == "POST":
        # 아이디 중복될경우 오류메세지 띄어야함.
        if request.POST["password1"] == request.POST["password2"]:
            print(request.POST)
            nickname = request.POST["nickname"]
            username = request.POST["username"]
            password = request.POST["password1"]
            email = request.POST["email"]

            user = User.objects.create_user(username, email, password)
            user.nickname = nickname
            user.save()

            return redirect("blog:login")
        else:
            messagebox.showinfo("warning", "패스워드가 서로 다릅니다.")
    return render(request, "blog/signup+css.html")


@login_required
def update_user(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('blog:login')

    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        model = Post
        users = User.objects.all()
        achieve_rates = {}
        for user in users:
            achieve_rates[user] = Post.objects.filter(category=1, author=user).count() * 10
        user_rates = achieve_rates[request.user]
    return render(request, 'blog/manage.html', {'user_change_form': user_change_form})


@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('blog:login')
    return render(request, 'blog/탈퇴.html')


@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)

        # 키워드인자명을 함께 써줘도 가능
        # password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            return redirect('blog:login', request.user.username)

    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'blog/password.html', {'password_change_form': password_change_form})


def MainPage(request):
    model = Post
    tags = Tag.objects.all()
    return render(request, 'blog/post_list+css.html', {'tags': tags, })


class PostList(ListView):
    model = Post
    paginate_by = 5

    # 역순만들기
    def get_queryset(self):
        return Post.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        users = User.objects.all()
        achieve_rates = {}
        group_rates = 0
        for user in users:
            achieve_rates[user] = Post.objects.filter(category=1, author=user).count() * 10
            group_rates += achieve_rates[user]
        group_rates //= len(achieve_rates)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        context['users'] = users
        context['achieve_rates'] = achieve_rates
        context['group_rates'] = group_rates

        return context


class PostListByTag(ListView):
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=tag_slug)

        return tag.post_set.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        tag_slug = self.kwargs['slug']
        context['tag'] = Tag.objects.get(slug=tag_slug)

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        users = User.objects.all()
        achieve_rates = {}
        group_rates = 0
        for user in users:
            achieve_rates[user] = Post.objects.filter(category=1, author=user).count() * 10
            group_rates += achieve_rates[user]
        group_rates //= len(achieve_rates)

        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()
        context['users'] = users
        context['achieve_rates'] = achieve_rates
        context['group_rates'] = group_rates

        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
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
        raise PermissionError('Comment 삭제 권한이 없습니다.')


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment


def user_info(request):
    users = User.objects.all()
    achieve_rates = {}

    for user in users:
        achieve_rates[user] = Post.objects.filter(category=1, author=user).count() * 10

    context = {'users': users, 'achieve_rates': achieve_rates}

    return render(request, 'blog/post_list.html', context)


def question(request):
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'blog/01-faq.html', context)


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    fields = [
        'title', 'content'
    ]

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/blog/QnA')


class QuestionUpdate(UpdateView):
    model = Question
    fields = [
        'title', 'content',
    ]


class QuestionDetail(DetailView):
    model = Question

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['answer_form'] = AnswerForm()

        return context


def answer(request, pk):
    question = Question.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = AnswerForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.author = request.user
            comment.question = question
            comment.save()
            return redirect(comment.get_absolute_url())
    else:
        return redirect('/blog/QnA')


class AnswerUpdate(UpdateView):
    model = Answer
    form_class = AnswerForm

    def get_object(self, queryset=None):
        answer = super(AnswerUpdate, self).get_object()
        if answer.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return answer

def mypage(request):
    return render(request, "blog/회원관리페이지메뉴.html")


def mychallenge_view(request):
    users = User.objects.all()
    achieve_rates = {}
    for user in users:
        achieve_rates[user] = Post.objects.filter(category=1, author=user).count() * 10
    user_rates = achieve_rates[request.user]
    return render(request, 'blog/mychallenge.html', {'achieve_rates': achieve_rates,'user_rates': user_rates})

def giveup(request):
    return render(request, 'blog/목표 그만두기.html')

