from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy
from .models import Post, Gallery, FriendLinks, Persons


class PostDetailSitemap(Sitemap):

    def items(self):
        return Post.objects.all()

    def location(self, item):
        return reverse_lazy('pages:view_post', args=[item.pk])


class GalleryDetailSitemap(Sitemap):

    def items(self):
        return Gallery.objects.all()

    def location(self, item):
        return reverse_lazy('pages:image_gallery', args=[item.pk])


class FriendDetailSitemap(Sitemap):

    def items(self):
        return FriendLinks.objects.all()

    def location(self, item):
        return reverse_lazy('pages:friend', args=[item.pk])


class PersonaDetailSitemap(Sitemap):

    def items(self):
        return Persons.objects.all()

    def location(self, item):
        return reverse_lazy('pages:persona', args=[item.pk])


class StaticSitemap(Sitemap):

    def items(self):
        return [
            'pages:posts',
            'pages:psy_gallery',
            'pages:dictionary_list',
            'pages:links',
            'pages:friends',
            'pages:polls',
            'pages:persons',
                    ]

    def location(self, item):
        return reverse_lazy(item)
