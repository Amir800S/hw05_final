from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class TaskCreateFormTests(TestCase):

    def test_user_created_after_signup(self):
        """ Новый User создался через форму на SignUp"""
        users_count = User.objects.count()
        self.client.post(
            reverse('users:signup'),
            data={
                'username': 'UserNameForTest',
                'email': 'testuser123@email.com',
                'password1': 'PaSSword123123',
                'password2': 'PaSSword123123'
            },
            follow=True
        )
        self.assertEqual(User.objects.count(), users_count + 1)
