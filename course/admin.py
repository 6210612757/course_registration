from django.contrib import admin

# Register your models here.

from .models import *

class CourseAdmin(admin.ModelAdmin) :
    list_display = ("id","code","name","semester","year","status","amount")

class StudentAdmin(admin.ModelAdmin) :
    list_display = ("id","user","std_id")

admin.site.register(Course,CourseAdmin)
admin.site.register(Student,StudentAdmin)
