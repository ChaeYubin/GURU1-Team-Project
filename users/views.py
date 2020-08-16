from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from tkinter import messagebox

def login_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user= authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("users:login")

def signup_view(request):
    if request.method =="POST":
        if request.POST["password1"]==request.POST["password2"]:
            print(request.POST)
            nickname = request.POST["nickname"]
            username = request.POST["username"]
            password = request.POST["password1"]
            email =request.POST["email"]

            user=User.objects.create(username, email, password)
            user.nickname =nickname
            user.save()

            return redirect("users:login")
        else:
            messagebox.showinfo("warning", "패스워드가 서로 다릅니다.")
    return redirect("users:signup")


