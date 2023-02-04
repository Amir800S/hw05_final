import shutil

from http import HTTPStatus

from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Post, User
from .fixtures import models


@override_settings(MEDIA_ROOT=models.TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.second_group = models.second_group()
        cls.post = models.post()
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(models.TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """ Тест отправки формы с картинкой со страницы Post Create """
        Post.objects.all().delete()
        post_count = Post.objects.count()
        form_data = {
            'text': 'TestText',
            'group': self.group.pk,
            'image': self.post.image,  # Картинка
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     args=(self.user.username,)))
        test_post = Post.objects.first()
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(test_post.text, form_data['text'])
        self.assertEqual(test_post.group.id, form_data['group'])
        self.assertEqual(test_post.author, self.user)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        """ Тест редактирования формы со страницы Post Edit """
        post_count = Post.objects.count()
        self.assertEqual(Post.objects.count(), 1)
        form_data = {
            'text': 'NewTestText',
            'group': self.second_group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(self.post.id,)),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     args=(self.post.id,)))

        edited_post = Post.objects.first()
        self.assertEqual(edited_post.author, self.post.author)
        self.assertEqual(edited_post.text, form_data['text'])
        self.assertEqual(edited_post.group.pk, form_data['group'])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_for_group = self.client.get(reverse('posts:group_list',
                                                     args=(self.group.slug,)))
        self.assertEqual(response_for_group.status_code, HTTPStatus.OK)
        self.assertNotIn(edited_post, response_for_group.context['page_obj'])
        self.assertEqual(Post.objects.count(), post_count)

    def test_can_not_create_post_guest(self):
        """ Неавторизированный пользователь не может создать пост"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Test',
            'group': self.group.pk,
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count)

    def test_title_label(self):
        """ Тест labels PostForm"""
        labels_fields = (
            ('text', 'Введите текст'),
            ('group', 'Выберите группу'),
        )
        for label_field, desc in labels_fields:
            with self.subTest(label_field=label_field):
                self.assertEqual(
                    self.form.fields[label_field].label,
                    desc
                )

    def test_title_help_text(self):
        """ Тест help_text PostForm"""
        help_text_fields = (
            ('text', 'Текст поста'),
            ('group', 'Название группы'),
        )
        for help_text_field, desc in help_text_fields:
            with self.subTest(help_text_field=help_text_field):
                self.assertEqual(
                    self.form.fields[help_text_field].help_text,
                    desc
                )

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
