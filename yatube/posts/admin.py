from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    """ Админ Постов """
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    """ Админ Групп """
    list_display = (
        'title',
        'slug',
    )
    search_fields = ('title',)
    list_filter = ('title',)


class CommentAdmin(admin.ModelAdmin):
    """ Админ Комментов """
    list_display = (
        'author',
        'text',
        'post',
        'pub_date'
    )
    list_filter = ('pub_date',)
    search_fields = (
        'author',
        'text',
        'pub_date'
    )


class FollowAdmin(admin.ModelAdmin):
    """ Админ Подписок """
    list_display = (
        'author',
        'user',
    )
    search_fields = (
        'author',
        'user',
    )


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Follow, FollowAdmin)
