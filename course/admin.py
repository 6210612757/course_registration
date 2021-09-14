from django.contrib import admin

# Register your models here.

from .models import *

class CourseAdmin(admin.ModelAdmin) :
    filter_horizontal = ("registered",)

class StudentAdmin(admin.ModelAdmin) :
    list_display = ("id","user","std_id")

admin.site.register(Course,CourseAdmin)
admin.site.register(Student,StudentAdmin)
