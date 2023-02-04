from django.contrib import admin

from .models import Comment, Group, Post


class PostAdmin(admin.ModelAdmin):  # Администрирование постов
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )  # Отображаемые поля поста
    list_editable = ('group',)
    search_fields = ('text',)  # Поиск по тексту
    list_filter = ('pub_date',)  # Фильтрация по дате публикации
    empty_value_display = '-пусто-'  # Если поле пустое


class GroupAdmin(admin.ModelAdmin):  # Администрирование групп
    list_display = (
        'title',
        'slug',
    )  # Отображаемые поля групп
    search_fields = ('title',)  # Поиск по заголовку
    list_filter = ('title',)  # Фильтрация по заголовку


class CommentAdmin(admin.ModelAdmin):  # Администирование Комментариев
    list_display = (
        'author',
        'text',
        'post',
        'pub_date'
    )  # Отображаемые поля комментариев
    list_filter = ('pub_date',)  # Фильтрация по дате публикации
    search_fields = (
        'author',
        'text',
        'pub_date'
    )  # Поиск по автору, тексту и дате публикации


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
