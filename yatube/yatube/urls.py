from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('', include('posts.urls', namespace='posts')),
    path('auth/', include('django.contrib.auth.urls')),
]

# Кастомные страницы ошибок
handler404 = 'core.views.page_not_found'
handler403 = settings.CSRF_FAILURE_VIEW

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
