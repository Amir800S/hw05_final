from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """ Форма создание поста """

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Введите текст',
            'group': 'Выберите группу'
        }
        help_texts = {
            'text': 'Текст поста',
            'group': 'Название группы',
        }


class CommentForm(forms.ModelForm):
    """ Форма создание комментария """
    class Meta:
        model = Comment
        fields = ('text', )
    labels = {
        'text': 'Введите текст',
    }
    help_texts = {
        'text': 'Текст комментария',
    }
