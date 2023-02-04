from django.conf import settings
from django.core.paginator import Paginator


def paginator(request, post_list):
    """ Paginator для приложения Posts"""
    paginator_get = Paginator(post_list, settings.POSTS_ON_MAIN)
    page_number = request.GET.get('page')
    page_obj = paginator_get.get_page(page_number)

    return page_obj
