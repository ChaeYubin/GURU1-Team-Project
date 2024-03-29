"""my_site_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .import views

app_name = "blog"

urlpatterns = [
    path('', views.PostList.as_view()),
    path('tag/<str:slug>/', views.PostListByTag.as_view()),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('delete_post/<int:pk>/', views.delete_post),
    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('create/', views.PostCreate.as_view()),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('edit_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup_view, name='signup'),
    path('challenge', views.user_info),
    path('QnA', views.question, name='QnA'),
    path('QnA/create', views.QuestionCreate.as_view()),
    path('QnA/<int:pk>/update/', views.QuestionUpdate.as_view()),
    path('QnA/<int:pk>/', views.QuestionDetail.as_view()),
    path('QnA/<int:pk>/new_comment/', views.answer),
    path('', views.MainPage, name='main'),
    path('update', views.update_user, name='update'),
    path('delete', views.delete_user, name='delete'),
    path('password/', views.password, name='password'),
    path('mypage', views.mypage, name='mypage'),
    path('mychallenge', views.mychallenge_view, name='mychallenge'),
    path('giveup', views.giveup, name='giveup'),
    path('about', views.about, name='about')
]
