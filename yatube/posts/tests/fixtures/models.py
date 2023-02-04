import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import Comment, Follow, Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(
    dir=settings.MEDIA_ROOT
)  # Директория для медиа-файлов
TEST_RANGE = 5  # Число постов на второй странице Paginator
FIRST_PAGE = 1  # Первая страница Paginator
SECOND_PAGE = 2  # Вторая страница Paginator


def user():
    """ Модель User """
    return User.objects.create_user(username='TestUser')


def second_user():
    """ Модель Second User """
    return User.objects.create_user(username='SecondTestUser')


def group():
    """ Модель Group """
    return Group.objects.create(
        title='TestGroup',
        slug='TestSlug',
        description='TestDesc',
    )


def second_group():
    """ Модель Второй Group для Post Edit """
    return Group.objects.create(
        title='TestGroup2',
        slug='TestSlug2',
        description='TestDesc2',
    )


def post():
    """ Модель Post """
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00'
        b'\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
        b'\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile(
        name='small.gif',
        content=small_gif,
        content_type='image/gif'
    )
    return Post.objects.create(
        author=User.objects.get(username='TestUser'),
        text='TestTextTestTextTestTextTestText',
        group=Group.objects.get(slug='TestSlug'),
        image=uploaded
    )


def bulk_post():
    """ Модель Post Bulk Create """
    return Post.objects.bulk_create(
        [Post(text='Test',
              author=User.objects.get(username='TestUser'),
              group=Group.objects.get(slug='TestSlug')
              ) for objs in range(
            TEST_RANGE + settings.POSTS_ON_MAIN)])


def comment():
    """ Модель Comment """
    return Comment.objects.create(
        text='Test',
        author=User.objects.get(username='TestUser'),
        post=Post.objects.first()
    )


def follow():
    return Follow.objects.create(
        user=User.objects.get(username='TestUser'),
        author=User.objects.get(username='SecondTestUser'),
    )


def second_post():
    """ Модель Second Post """
    return Post.objects.create(author=User.objects.get(
        username='SecondTestUser'),
        text='TestText'
    )
