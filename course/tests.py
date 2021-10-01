from django.test import Client, TestCase

# Create your tests here.
from .models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.hashers import make_password


class CourseTestCase(TestCase):

    def setUp(self):

        passwordss = make_password('1234')
        user = User.objects.create(
            username='user1', password=passwordss, email='user1@exp.com')

        student = Student.objects.create(user=user, std_id='1234567890')

        course = Course.objects.create(code='1', name='English',
                                       semester=1, year=2000, amount=2, status=True)
        Course.objects.create(code='2', name='Thai',
                              semester=1, year=2000, amount=3, status=True)

        Course.objects.create(code='3', name='Math',
                              semester=1, year=2000, amount=3, status=False)
        course2 = Course.objects.create(code='3', name='Math',
                                        semester=1, year=2000, amount=1, status=True)
        course.registered.add(student)
        course.save()
        course2.registered.add(student)
        course2.save()

        tmp = Temp_register.objects.create(user=user)
        tmp.register.add(course)
        tmp.register.add(course2)
        tmp.save()

    def test_index_view_with_authen(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:index'))
        self.assertEqual(responses.status_code, 200)

    def test_index_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:index'))
        self.assertEqual(responses.status_code, 302)

    def test_course_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:course', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_course_view_render(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:course', args=(1,)))
        self.assertEqual(responses.status_code, 200)

    def test_register_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:register'))
        self.assertEqual(responses.status_code, 302)

    def test_register_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:register'))
        self.assertEqual(responses.status_code, 200)

    def test_temp_register_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:temp_register', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_temp_register_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:temp_register', args=(2,)))
        self.assertEqual(responses.status_code, 302)

    def test_temp_deregister_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:deregister', args=(1,)))
        self.assertEqual(responses.status_code, 302)

    def test_temp_deregister_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:deregister', args=(2,)))
        self.assertEqual(responses.status_code, 302)

    def test_confirm_register_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:confirm_register'))
        self.assertEqual(responses.status_code, 302)

    def test_confirm_register_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:confirm_register'))
        self.assertEqual(responses.status_code, 302)

    def test_mycourse_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:mycourse'))
        self.assertEqual(responses.status_code, 302)

    def test_mycourse_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:mycourse'))
        self.assertEqual(responses.status_code, 200)

    def test_status_view_without_authen(self):
        c = Client()
        responses = c.get(reverse('course:status', args=(3,)))
        self.assertEqual(responses.status_code, 302)

    def test_status_view(self):
        c = Client()
        user = User.objects.get(username='user1', email='user1@exp.com')
        c.force_login(user)
        responses = c.get(reverse('course:status', args=(3,)))
        self.assertEqual(responses.status_code, 302)

    def test_model(self):
        user = User.objects.get(username='user1', email='user1@exp.com')
        student = Student.objects.get(user=user)
        tmp = Temp_register.objects.get(user=user)
        print(student)
        print(tmp)
