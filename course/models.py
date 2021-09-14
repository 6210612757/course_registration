from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model) :
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    std_id = models.IntegerField()

    def __str__(self):
        return f"user : {self.user.username} ID : {self.std_id} Name : {self.user.first_name} {self.user.last_name}"


class Course(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length = 64)
    semester = models.IntegerField()
    year = models.IntegerField()
    amount = models.IntegerField()
    status = models.BooleanField()
    registered = models.ManyToManyField(Student,blank = True)
    
    def count_student(self) :
        return self.registered.count()

    def isfull(self) :
        if self.registered.count() == self.amount :
            return True
        return False
        
    def __str__(self):
        return f"{self.name} ( {self.code} )"


class Temp_register(models.Model) :
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    register = models.ManyToManyField(Course,blank = True)
    def __str__(self) :
        return f"{self.user.username} registering {self.register.count()} courses"