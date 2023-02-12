from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('', include('pages.urls')),
    path('psy_wings/', include('psywings.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('admin/', admin.site.urls),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)