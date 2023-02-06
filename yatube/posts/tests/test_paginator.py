from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from .fixtures import models


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = models.user()
        cls.second_user = models.second_user()
        cls.group = models.group()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.second_authorized_client = Client()
        self.second_authorized_client.force_login(self.second_user)
        models.follow()
        models.bulk_post()

    def test_paginator(self):
        """ Проверка Paginator """
        adresses_and_args = (
            ('posts:index', None),
            ('posts:group_list', (self.group.slug,)),
            ('posts:profile', (self.user.username,)),
            ('posts:follow_index', None)
        )
        pages_for_test = (
            (models.FIRST_PAGE, settings.POSTS_ON_MAIN),
            (models.SECOND_PAGE, models.TEST_RANGE)
        )
        for name, args in adresses_and_args:
            if name == 'posts:follow_index':
                models.second_bulk_post()
            for page, count in pages_for_test:
                with self.subTest(name=name, page=page):
                    response = self.authorized_client.get(
                        reverse(name, args=args), {'page': page}
                    )
                    self.assertEqual(
                        len(response.context.get('page_obj').object_list),
                        count)
