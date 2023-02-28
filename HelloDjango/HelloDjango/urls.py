from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve


urlpatterns = [
    path('', include('pages.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),

    re_path('robots.txt', TemplateView.as_view(template_name="pages/robots.txt", content_type='text/plain')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)