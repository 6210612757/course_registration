from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


# Create your views here.

from .models import *

def index(request) :
    if request.user.is_authenticated:
        return render(request, "course/index.html", {
            "courses": Course.objects.all()
        })
        
    else:
        return HttpResponseRedirect(reverse("users:login"))

def course(request,course_id) :
    this_course = Course.objects.get(id = course_id)
    
    return render(request,"course/course.html",{
        "course" : this_course,
    })

def register(request) :
    username = request.user.username
    open_course = []
    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    temp_registered = user_temp.register.all()
    for course in Course.objects.all():
        
        if course.status and (username not in [i.user.username for i in course.registered.all()]) and (course not in user_temp.register.all()):
            open_course.append(course)
    
    return render(request, "course/register.html", {
        "username" : username,
        "open_courses": open_course,
        "temp_registered" : temp_registered ,
    })


def temp_register(request,course_id) :

    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    this_course = Course.objects.get(id = course_id)
    
    user_temp.register.add(this_course)
    user_temp.save()
    return HttpResponseRedirect(reverse("course:register"))


def temp_deregister(request,course_id) :
    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    this_course = Course.objects.get(id = course_id)

    user_temp.register.remove(this_course)
    user_temp.save()
    return HttpResponseRedirect(reverse("course:register"))

def confirm_register(request) :
    user_student = Student.objects.get (user = request.user)
    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    
    for course in user_temp.register.all() :
        course.registered.add(user_student)
        if course.isfull() :
            course.status = False
        course.save()
    return HttpResponseRedirect(reverse("course:mycourse"))

def mycourse(request) :
    username = request.user.username
    registered_course = []
    for course in Course.objects.all() :
        for student in course.registered.all():
            if username == student.user.username:
                registered_course.append(course)

    return render(request, "course/mycourse.html", {
        "registered_courses": registered_course,
    })