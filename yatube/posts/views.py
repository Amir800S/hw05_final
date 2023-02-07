from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .models import Follow, Group, Post, User
from .forms import CommentForm, PostForm
from .utils import paginator


def index(request):
    """ Главная страница """
    post_list = Post.objects.select_related('author', 'group').all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """ Страница группы """
    group_with_slug = get_object_or_404(Group, slug=slug)
    post_list = group_with_slug.posts.select_related('author').all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
        'group': group_with_slug,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """ Страница автора поста """
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group').all()
    page_obj = paginator(request, post_list)
    following = request.user.is_authenticated and author.following.filter(
        user=request.user).exists()
    context = {
        'page_obj': page_obj,
        'usermodel': author,
        'post_list': post_list,
        'following': following
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """ Подробное чтение поста """
    get_post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related(
            'comments__author'), id=post_id)
    comment_form = CommentForm()
    context = {
        'onepost': get_post,
        'comments': get_post.comments.all(),
        'comment_form': comment_form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """ Функция создания поста """
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """ Редактирование поста """
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def create_comment(request, post_id):
    """ Добавление комментария """
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """ Все подписки пользователя """
    post_list = Post.objects.select_related(
        'author', 'group'
    ).filter(
        author__following__user=request.user
    )
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """ View подписки на автора """
    follow_author = get_object_or_404(User, username=username)
    if follow_author != request.user:
        Follow.objects.get_or_create(
            user=request.user,
            author=follow_author
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """ View отписки на автора """
    get_object_or_404(Follow,
                      author__username=username,
                      ).delete()
    return redirect('posts:profile', username=username)
