from django.test import TestCase

from .fixtures import models


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.group = models.group()
        cls.post = models.post()
        cls.comment = models.comment()

    def test_post_have_correct_object_names(self):
        """ Модель Post отображается правильно """
        self.assertEqual(self.post.text[:15], str(self.post))

    def test_group_have_correct_object_names(self):
        """ Модель Group отображается правильно """
        self.assertEqual(self.group.title, str(self.group))

    def test_verbose_names_post(self):
        """ Проверка verbose Post"""
        fields = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for verbose_field, desc in fields.items():
            with self.subTest(verbose_field=verbose_field):
                self.assertEqual(
                    self.post._meta.get_field(
                        verbose_field).verbose_name, desc
                )

    def test_verbose_names_group(self):
        """ Проверка verbose Group"""
        fields = (
            ('title', 'Название группы'),
            ('slug', 'URL адрес'),
            ('description', 'Описание группы'),
        )
        for verbose_field, desc in fields:
            with self.subTest(verbose_field=verbose_field):
                self.assertEqual(
                    self.group._meta.get_field(
                        verbose_field).verbose_name, desc
                )

    def test_verbose_names_comment(self):
        """ Проверка verbose Comment"""
        fields = (
            ('author', 'Автор'),
            ('text', 'Текст комментария'),
        )
        for verbose_field, desc in fields:
            with self.subTest(verbose_field=verbose_field):
                self.assertEqual(
                    self.comment._meta.get_field(
                        verbose_field).verbose_name, desc
                )

    def test_help_texts_post(self):
        """ Проверка help_text Post"""
        fields = (
            ('text', 'Напишите что нибудь...'),
            ('group', 'Группа поста')
        )
        for fields, desc in fields:
            with self.subTest(fields=fields):
                self.assertEqual(
                    self.post._meta.get_field(fields).help_text, desc)

    def test_help_texts_group(self):
        """ Проверка help_text Group"""
        fields = (
            ('title', 'Дайте название группе'),
            ('description', 'Описание для группы')
        )
        for fields, desc in fields:
            with self.subTest(fields=fields):
                self.assertEqual(
                    self.group._meta.get_field(fields).help_text, desc)

    def test_help_texts_comment(self):
        """ Проверка help_text Comment"""
        fields = (
            ('text', 'Напишите что нибудь...'),
        )
        for fields, desc in fields:
            with self.subTest(fields=fields):
                self.assertEqual(
                    self.comment._meta.get_field(fields).help_text, desc)
