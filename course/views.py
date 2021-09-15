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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    this_course = Course.objects.get(id = course_id)
    
    return render(request,"course/course.html",{
        "course" : this_course,
    })


def register(request) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    username = request.user.username
    open_course = []
    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    temp_registered = user_temp.register.all()
    registered_course = []
    for course in Course.objects.all() :
        for student in course.registered.all():
            if request.user == student.user:
                registered_course.append(course)

    for course in Course.objects.all():
       
        if  (course not in user_temp.register.all()) :
            open_course.append((course,course.registered.count(),course.isfull()))

    return render(request, "course/register.html", {
        "username" : username,
        "open_courses": open_course,
        "temp_registered" : temp_registered ,
        "registered_course" : registered_course,
    })


def temp_register(request,course_id) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    this_course = Course.objects.get(id = course_id)
    
    user_temp.register.add(this_course)
    user_temp.save()
    return HttpResponseRedirect(reverse("course:register"))


def temp_deregister(request,course_id) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    this_course = Course.objects.get(id = course_id)

    user_temp.register.remove(this_course)
    user_temp.save()
    return HttpResponseRedirect(reverse("course:register"))
    

def confirm_register(request) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    user_student = Student.objects.get (user = request.user)
    user_temp = Temp_register.objects.get_or_create(user = request.user)[0]
    
    registered_course = []
    for course in Course.objects.all() :
        for student in course.registered.all():
            if request.user == student.user:
                registered_course.append(course)
    for course in registered_course :
        course.registered.remove(user_student)
        course.save()
    for course in user_temp.register.all() :
        if user_student not in course.registered.all() :
            course.registered.add(user_student)
        if course.isfull():
            course.status = False
        else :
            course.status = True
        course.save()
    return HttpResponseRedirect(reverse("course:mycourse"))


def mycourse(request) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
        
    username = request.user.username
    registered_courses = []
    for course in Course.objects.all() :
        for student in course.registered.all():
            if username == student.user.username:
                registered_courses.append(course)

    return render(request, "course/mycourse.html", {
        "registered_courses": registered_courses,
    })