from django.urls import path

from . import views

app_name = 'course'
urlpatterns = [path("", views.index, name="index"),
               path("<int:course_id>", views.course, name="course"),
               path("register", views.register, name="register"),
               path("register/<int:course_id>",
                    views.temp_register, name="temp_register"),
               path("deregister/<int:course_id>",
                    views.temp_deregister, name="deregister"),
               path("confirm_register", views.confirm_register, name="confirm_register"),
               path("mycourse", views.mycourse, name="mycourse"),
               ]
