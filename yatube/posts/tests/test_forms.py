import shutil
from http import HTTPStatus

from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import CommentForm, PostForm
from ..models import Comment, Post
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
        cls.post_form = PostForm()
        cls.comment_form = CommentForm()

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

    def test_create_comment(self):
        """ Тест отправки формы коммента со страницы Post Detail """
        Comment.objects.all().delete()
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'TestText',
        }
        response = self.authorized_client.post(
            reverse('posts:create_comment', args=(self.post.id,)),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     args=(self.post.id,)))
        test_comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertEqual(test_comment.text, form_data['text'])
        self.assertEqual(test_comment.author, self.user)
        self.assertEqual(test_comment.post, self.post)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_can_not_create_comment_guest(self):
        """ Неавторизированный пользователь не может комментировать"""
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Test',
        }
        self.client.post(
            reverse('posts:create_comment', args=(self.post.id,)),
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comment_count)

    def test_title_label_post_form(self):
        """ Тест labels PostForm"""
        labels_fields = (
            ('text', 'Введите текст'),
            ('group', 'Выберите группу'),
        )
        for label_field, desc in labels_fields:
            with self.subTest(label_field=label_field):
                self.assertEqual(
                    self.post_form.fields[label_field].label,
                    desc
                )

    def test_title_help_text_post_form(self):
        """ Тест help_text PostForm"""
        help_text_fields = (
            ('text', 'Текст поста'),
            ('group', 'Название группы'),
        )
        for help_text_field, desc in help_text_fields:
            with self.subTest(help_text_field=help_text_field):
                self.assertEqual(
                    self.post_form.fields[help_text_field].help_text,
                    desc
                )

    def test_title_label_comment_form(self):
        """ Тест labels CommentForm"""
        labels_fields = (
            ('text', 'Текст комментария'),
        )
        for label_field, desc in labels_fields:
            with self.subTest(label_field=label_field):
                self.assertEqual(
                    self.comment_form.fields[label_field].label,
                    desc
                )

    def test_title_help_text_comment_form(self):
        """ Тест help_text CommentForm"""
        help_text_fields = (
            ('text', 'Напишите что нибудь...'),
        )
        for help_text_field, desc in help_text_fields:
            with self.subTest(help_text_field=help_text_field):
                self.assertEqual(
                    self.comment_form.fields[help_text_field].help_text,
                    desc
                )
