from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
import sys
sys.path.append('../')
from course.models import *

def index(request):
    if request.user.is_authenticated:
        return render(request, "users/index.html")
    else:
        return HttpResponseRedirect(reverse("users:login"))

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:index"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {"fail": "Invalid credential"})
    return render(request, "users/login.html")
    
    

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return render(request, "users/login.html", {
        "messages": messages.get_messages(request)
    })


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        re_password = request.POST["re_password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        std_id = request.POST["std_id"]
        if password != re_password:
            return render(request, "users/register.html", {"message": "Invalid Re-Password"})
        add_user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
        bond_id = Student(user = add_user,std_id = std_id)
        add_user.set_password(password)
        
        add_user.save()
        bond_id.save()
        return render(request, "users/login.html")
    return render(request, "users/register.html")