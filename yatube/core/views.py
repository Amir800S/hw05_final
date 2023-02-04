from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    """ Кастомная страница 404 Ошибки"""
    return render(
        request, '404.html',
        {'path': request.path},
        status=HTTPStatus.NOT_FOUND
    )


def csrf_failure(request, reason=''):
    """ Кастомная страница 403 Ошибки"""
    return render(request, '403.html')
