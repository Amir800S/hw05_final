from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.core.cache import cache

from .fixtures import models
from ..forms import PostForm
from ..models import Follow, Post


class TaskPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()
        cls.second_group = models.second_group()
        cls.comment = models.comment()
        cls.second_user = models.second_user()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_second_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_second_client.force_login(self.second_user)

    def what_is_in_context(self, request, args, get_cont=False):
        """ Функция проверки контекста View"""
        if get_cont:
            response = self.authorized_client.get(reverse(request, args=args))
            post = response.context['onepost']
            # Проверяем коммент к посту
            comment = response.context['comments'][0]
            self.assertEqual(
                comment.text, self.comment.text)
            self.assertEqual(
                comment.author, self.comment.author)
            self.assertEqual(
                comment.post, self.post)
        else:
            response = self.authorized_client.get(reverse(request, args=args))
            post = response.context['page_obj'][0]
        self.assertEqual(
            post.author, self.post.author)
        self.assertEqual(
            post.group, self.post.group)
        self.assertEqual(
            post.text, self.post.text)
        self.assertEqual(
            post.pub_date, self.post.pub_date)
        # Картинка есть в контексте Views
        self.assertEqual(
            post.image, self.post.image)

    def test_index_show_correct_context(self):
        """ Проверка Index"""
        self.what_is_in_context('posts:index', None)

    def test_group_list_show_correct_context(self):
        """ Проверка Group List"""
        self.what_is_in_context('posts:group_list', (self.group.slug,))
        # Проверка доп.контекста 'group'
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,)))
        self.assertEqual(self.group, response.context['group'])

    def test_profile_show_correct_context(self):
        """ Проверка Profile"""
        self.what_is_in_context('posts:profile', (self.user.username,))
        # Проверка доп.контекста 'usermodel', 'post_list'
        response = self.authorized_client.get(
            reverse('posts:profile', args=(self.user.username,)))
        self.assertEqual(self.user, response.context['usermodel'])
        # Проверка количества постов пользователя
        post_list = response.context['post_list']
        self.assertEqual(
            post_list.count(), Post.objects.filter(author=self.user).count())

    def test_post_detail_show_correct_context(self):
        """ Проверка Post Detail"""
        self.what_is_in_context('posts:post_detail', (self.post.id,), True)

    def test_create_and_edit_posts(self):
        """ Проверка Create Post и Edit Post """
        edit_and_create_test = (
            ('posts:post_edit', (self.post.id,)),
            ('posts:post_create', None)
        )
        for rev_name, args in edit_and_create_test:
            with self.subTest(rev_name=rev_name, args=args):
                response = self.authorized_client.get(
                    reverse(rev_name, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(
                    response.context['form'],
                    PostForm
                )
                # Проверка полей формы
                self.assertIsInstance(response.context.get(
                    'form').fields.get('text'), forms.fields.CharField)
                self.assertIsInstance(response.context.get(
                    'form').fields.get('group'), forms.fields.ChoiceField)
                self.assertIsInstance(response.context.get(
                    'form').fields.get('image'), forms.fields.ImageField)

    def test_in_intended_group(self):
        """ Тест пост попал в нужную группу """
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.second_group.slug,))
        )
        self.assertEqual(len(response.context.get('page_obj').object_list), 0)
        post = Post.objects.first()
        self.assertTrue(post.group)
        response_to_group = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,))
        )
        self.assertIn(
            post, response_to_group.context['page_obj'].object_list
        )

    def test_cache(self):
        """ Тест кэширования страницы Index """
        first_response = self.authorized_client.get(
            reverse('posts:index')
        )  # Первый запрос
        first_context = first_response.content
        Post.objects.all().delete()  # Удаление всех постов
        second_response = self.authorized_client.get(
            reverse('posts:index')
        )  # Второй запрос
        second_context = second_response.content
        self.assertEqual(first_context, second_context)
        cache.clear()  # Чистим Кэш
        third_response = self.authorized_client.get(
            reverse('posts:index')
        )  # Третий запрос
        third_context = third_response.content
        self.assertNotEqual(third_context, second_context)

    def test_user_can_follow(self):
        """ Проверка пользователь может подписаться """
        count = Follow.objects.all().count()
        self.authorized_client.post(
            reverse('posts:profile_follow', args=(self.second_user,)),
        )
        self.assertEqual(count, count + 1)

    def test_user_can_unfollow(self):
        """ Проверка пользователь может оmписаться """
        count = Follow.objects.all().count()
        self.authorized_client.post(
            reverse('posts:profile_unfollow', args=(self.second_user,)),
        )
        self.assertEqual(count, count - 1)

    def test_if_post_in_favourites(self):
        """ Запись в ленте избранных """
        models.follow()
        post_by_author = models.second_post()
        response = self.authorized_client.get(
            reverse('posts:follow_index'),
        )
        self.assertIn(post_by_author, response.context['page_obj'].object_list)

    def test_if_post_not_in_favourites(self):
        """ Нет записи в ленте избранных """
        post_by_author = models.second_post()
        response = self.authorized_client.get(
            reverse('posts:follow_index'),
        )
        self.assertNotIn(post_by_author, response.context['page_obj'].object_list)
