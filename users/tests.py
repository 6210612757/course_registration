from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from course.models import *

# Create your tests here.
class Login_out(TestCase):

    def setUp(self):
        
        user = User.objects.create(username = "user1", password = make_password("1234"),email="user1@example.com")

    def test_index_not_authenticated(self):
        c = Client()
        
        response = c.get(reverse('users:index'))
        self.assertEqual(response.status_code, 302) #Using Redirect code 302

    def test_index_authenticated(self):
        user = User.objects.get(username = "user1")
        c = Client()
        c.force_login(user)
        response = c.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200) #Using Render code 200
        self.assertTemplateUsed(response, "users/index.html") #Load HTML

    def test_login_authenticated(self):
        user = User.objects.get(username = "user1")
        c = Client()
        c.force_login(user)
        response = c.get(reverse('users:login'))
        self.assertEqual(response.status_code, 302) 

    def test_login_success(self) :
        c = Client()
        response = c.post(reverse('users:login'),{'username' : 'user1','password':'1234'})
        self.assertEqual(response.status_code, 302) 

    def test_login_not_success(self) :
        c = Client()
        response = c.post(reverse('users:login'),{'username' : 'user1','password': ''})
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/login.html")
    
    def test_direct_login(self) :
        c = Client()
        response = c.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/login.html")

    def test_logout(self) :
        c = Client()
        response = c.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/login.html")

class Register(TestCase):
    def setUp(self):
        
        user = User.objects.create(username = "user1", password = make_password("1234"),email="user1@example.com")
        student = Student(user = user,std_id = '6200000000')
        student.save()

    def test_index_register(self) :
        c = Client()
        response = c.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_success(self) :
        c = Client()
        response = c.post(reverse('users:register'),{'username' : 'newuser',
                                                'password': '1234',
                                                're_password': '1234',
                                                'email': 'newuser@student.com',
                                                'first_name' : 'sawadee',
                                                'last_name' : 'tansamachick',
                                                'std_id' : '6200000001',
                                                })
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/login.html")

    def test_register_duplicate_username(self):
        c = Client()
        response = c.post(reverse('users:register'),{'username' : 'user1',
                                                'password': '1234',
                                                're_password': '1234',
                                                'email': 'newuser@student.com',
                                                'first_name' : 'sawadee',
                                                'last_name' : 'tansamachick',
                                                'std_id' : '6200000001',
                                                })
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_duplicate_std_id(self):
        c = Client()
        response = c.post(reverse('users:register'),{'username' : 'newuser',
                                                'password': '1234',
                                                're_password': '1234',
                                                'email': 'newuser@student.com',
                                                'first_name' : 'sawadee',
                                                'last_name' : 'tansamachick',
                                                'std_id' : '6200000000',
                                                })
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/register.html") 

    def test_register_check_valid_std_id(self):
        c = Client()
        response = c.post(reverse('users:register'),{'username' : 'newuser',
                                                'password': '1234',
                                                're_password': '1234',
                                                'email': 'newuser@student.com',
                                                'first_name' : 'sawadee',
                                                'last_name' : 'tansamachick',
                                                'std_id' : '6200000000111111',
                                                })
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_check_repassword(self):
        c = Client()
        response = c.post(reverse('users:register'),{'username' : 'newuser',
                                                'password': '12345',
                                                're_password': 'something',
                                                'email': 'newuser@student.com',
                                                'first_name' : 'sawadee',
                                                'last_name' : 'tansamachick',
                                                'std_id' : '6200000001',
                                                })
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "users/register.html")

    